from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset
import torch
import os

# === CONFIGURATION ===
MODEL_ID = "cjvt/GaMS-9B"
DATA_PATH = "data/finetune_data.json"
OUTPUT_DIR = "finetuned-gams9b"
BATCH_SIZE = 1
EPOCHS = 3
MAX_LENGTH = 512

# === LOAD TOKENIZER AND MODEL ===
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)

raw_dataset = load_dataset("json", data_files={"train": DATA_PATH})["train"]

def tokenize(example):
    prompt = f"### Vprašanje:\n{example['prompt']}\n### Odgovor:\n{example['response']}"
    encoded = tokenizer(prompt, truncation=True, padding="max_length", max_length=MAX_LENGTH)
    encoded["labels"] = encoded["input_ids"].copy()
    return encoded


tokenized_dataset = raw_dataset.map(tokenize)

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=4,
    num_train_epochs=EPOCHS,
    logging_dir=os.path.join(OUTPUT_DIR, "logs"),
    logging_steps=10,
    save_strategy="epoch",
    evaluation_strategy="no",
    save_total_limit=2,
    fp16=True,
    gradient_checkpointing=True,
    report_to="none"
)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

trainer.train()

trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)