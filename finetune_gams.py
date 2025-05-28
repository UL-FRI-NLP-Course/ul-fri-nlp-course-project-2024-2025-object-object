from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq
)
from datasets import load_dataset
import torch
import os

# === CONFIGURATION ===
MODEL_ID = "cjvt/t5-sl-small"
DATA_PATH = "data/finetune_data.json"
OUTPUT_DIR = "finetuned-t5"
BATCH_SIZE = 4
EPOCHS = 3
MAX_LENGTH = 128

# === LOAD TOKENIZER AND MODEL ===
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
model = model.cuda()

# === LOAD DATA ===
raw_dataset = load_dataset("json", data_files={"train": DATA_PATH})["train"]

def tokenize(example):
    input_text = f"translate Slovenian to Slovenian: {example['prompt']}"
    target_text = example['response']
    model_inputs = tokenizer(input_text, truncation=True, padding="max_length", max_length=MAX_LENGTH)
    labels = tokenizer(target_text, truncation=True, padding="max_length", max_length=MAX_LENGTH)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_dataset = raw_dataset.map(tokenize, remove_columns=raw_dataset.column_names)

# === TRAINING ARGUMENTS ===
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=EPOCHS,
    logging_dir=os.path.join(OUTPUT_DIR, "logs"),
    logging_steps=10,
    save_strategy="epoch",
    save_total_limit=2,
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=2,
    fp16=False,
    bf16=False,
    dataloader_pin_memory=False,
    deepspeed=None,
    ddp_find_unused_parameters=False,
    lr_scheduler_type="cosine",
    warmup_steps=5,
    learning_rate=5e-5,
    report_to="none",
    optim="adamw_torch",
    use_cpu=True
)

# === DATA COLLATOR ===
data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

# === TRAINER ===
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# === START TRAINING ===
trainer.train()

# === SAVE MODEL ===
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"Fine-tuning zaključen. Model je shranjen v: {OUTPUT_DIR}", flush=True)
