from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import get_peft_model, LoraConfig, TaskType, prepare_model_for_kbit_training
from datasets import load_dataset
import torch

model_id = "cjvt/GaMS-1B"

# 1. Naloži tokenizer & model
tokenizer = AutoTokenizer.from_pretrained(model_id)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    load_in_4bit=True,
    torch_dtype=torch.float16
)

# 2. Pripravi za 4-bit treniranje
model = prepare_model_for_kbit_training(model)

# 3. Konfiguracija za LoRA
peft_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, peft_config)

# 4. Naloži podatke - SPREMENI TO VRSTICO!
dataset = load_dataset("json", data_files="../data/slovenian_knowledge_training.jsonl")["train"]

def format_example(example):
    """Kombinira input in output v en tekst"""
    text = f"{example['input']}\n\n{example['output']}"
    return {"text": text}

def tokenize(example):
    """Tokenizira formatirane podatke"""
    return tokenizer(example["text"], truncation=True, padding="max_length", max_length=512)

# 5. Formatiraj in tokeniziraj podatke
formatted_dataset = dataset.map(format_example, batched=False)
tokenized_dataset = formatted_dataset.map(tokenize, batched=True)

# 6. Argumenti treninga
training_args = TrainingArguments(
    output_dir="outputs",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    logging_dir="./logs",
    logging_steps=10,
    num_train_epochs=3,
    save_total_limit=2,
    save_strategy="epoch",
    learning_rate=2e-4,
    fp16=True,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
)

trainer.train()
