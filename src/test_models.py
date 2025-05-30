import json
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from peft import PeftModel
import torch

def load_questions_from_json(file_path):
    """Naloži vprašanja iz JSON datoteke"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [item['question'] for item in data]

def test_base_model():
    print("=== TESTIRANJE BASE MODELA ===")
    
    # Base model brez fine-tuninga
    model = AutoModelForCausalLM.from_pretrained(
        "cjvt/GaMS-1B", 
        device_map="auto", 
        torch_dtype=torch.float16
    )
    tokenizer = AutoTokenizer.from_pretrained("cjvt/GaMS-1B")
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    
    # Uporabi prvo vprašanje iz JSON
    questions = load_questions_from_json("../questions.json")
    test_question = questions[0]
    
    print(f"TEST VPRAŠANJE: {test_question}")
    result = pipe(test_question, max_new_tokens=50, pad_token_id=tokenizer.eos_token_id)
    print("BASE MODEL ODGOVOR:")
    print(result[0]['generated_text'][len(test_question):])
    print("\n" + "="*60 + "\n")

def test_finetuned_model():
    print("=== TESTIRANJE FINE-TUNED MODELA ===")
    
    # Fine-tuned model
    base_model = AutoModelForCausalLM.from_pretrained(
        "cjvt/GaMS-1B",
        device_map="auto",
        torch_dtype=torch.float16
    )
    
    model = PeftModel.from_pretrained(base_model, "outputs/checkpoint-1875")
    tokenizer = AutoTokenizer.from_pretrained("cjvt/GaMS-1B")
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    
    # Uporabi prva 3 vprašanja iz JSON z Graph-RAG formatom
    questions = load_questions_from_json("../questions.json")
    
    # Simuliramo Graph-RAG format za testiranje
    test_cases = [
        f"Odgovori na vprašanje na podlagi podanih podatkov.\n\nPodatki: <primer_podatki>\n\nVprašanje: {questions[0]}\n\n",
        f"Odgovori na vprašanje na podlagi podanih podatkov.\n\nPodatki: <primer_podatki>\n\nVprašanje: {questions[1]}\n\n",
        f"Odgovori na vprašanje na podlagi podanih podatkov.\n\nPodatki: <primer_podatki>\n\nVprašanje: {questions[2]}\n\n"
    ]
    
    for i, test_prompt in enumerate(test_cases, 1):
        print(f"\n--- FINE-TUNED TEST {i} ---")
        print("PROMPT:")
        print(test_prompt)
        
        result = pipe(test_prompt, max_new_tokens=50, do_sample=False, pad_token_id=tokenizer.eos_token_id)
        response = result[0]['generated_text'][len(test_prompt):].strip()
        
        print("ODGOVOR:")
        print(response)
        print("-" * 50)

def test_knowledge_integration():
    print("=== TESTIRANJE KNOWLEDGE INTEGRATION (LoRA FINE-TUNING) ===")
    
    # LoRA fine-tuned model
    base_model = AutoModelForCausalLM.from_pretrained(
        "cjvt/GaMS-1B",
        device_map="auto",
        torch_dtype=torch.float16
    )
    
    model = PeftModel.from_pretrained(base_model, "outputs/checkpoint-1875")
    tokenizer = AutoTokenizer.from_pretrained("cjvt/GaMS-1B")
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    
    # Uporabi prva 8 vprašanj iz JSON - BREZ podatkov v promptu
    questions = load_questions_from_json("../questions.json")
    knowledge_tests = questions[:8]
    
    for i, question in enumerate(knowledge_tests, 1):
        print(f"\n--- KNOWLEDGE TEST {i} ---")
        print(f"VPRAŠANJE: {question}")
        
        result = pipe(question, max_new_tokens=30, do_sample=False, pad_token_id=tokenizer.eos_token_id)
        response = result[0]['generated_text'][len(question):].strip()
        
        print(f"ODGOVOR: {response}")
        print("-" * 50)

def test_base_vs_knowledge_comparison():
    print("=== PRIMERJAVA: BASE vs KNOWLEDGE INTEGRATION ===")
    
    # Base model
    base_model = AutoModelForCausalLM.from_pretrained(
        "cjvt/GaMS-1B", 
        device_map="auto", 
        torch_dtype=torch.float16
    )
    base_tokenizer = AutoTokenizer.from_pretrained("cjvt/GaMS-1B")
    base_pipe = pipeline("text-generation", model=base_model, tokenizer=base_tokenizer)
    
    # Knowledge integration model
    knowledge_model = PeftModel.from_pretrained(base_model, "outputs/checkpoint-1875")
    knowledge_pipe = pipeline("text-generation", model=knowledge_model, tokenizer=base_tokenizer)
    
    # Uporabi prva 3 vprašanja iz JSON
    questions = load_questions_from_json("../questions.json")
    test_questions = questions[:3]
    
    for question in test_questions:
        print(f"\nVPRAŠANJE: {question}")
        
        # Base model odgovor
        base_result = base_pipe(question, max_new_tokens=30, pad_token_id=base_tokenizer.eos_token_id)
        base_response = base_result[0]['generated_text'][len(question):].strip()
        
        # Knowledge integration model odgovor
        knowledge_result = knowledge_pipe(question, max_new_tokens=30, do_sample=False, pad_token_id=base_tokenizer.eos_token_id)
        knowledge_response = knowledge_result[0]['generated_text'][len(question):].strip()
        
        print(f"BASE MODEL: {base_response}")
        print(f"KNOWLEDGE MODEL: {knowledge_response}")
        print("-" * 60)

def test_knowledge_integration_with_json():
    print("=== TESTIRANJE KNOWLEDGE INTEGRATION Z JSON VPRAŠANJI ===")
    
    # LoRA fine-tuned model
    base_model = AutoModelForCausalLM.from_pretrained(
        "cjvt/GaMS-1B",
        device_map="auto",
        torch_dtype=torch.float16
    )
    
    model = PeftModel.from_pretrained(base_model, "outputs/checkpoint-1875")
    tokenizer = AutoTokenizer.from_pretrained("cjvt/GaMS-1B")
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    
    # Naloži vprašanja iz JSON
    questions = load_questions_from_json("../questions.json")
    
    # Testiraj z npr. prvimi 20 vprašanji
    test_questions = questions[:20]
    
    correct_count = 0
    total_count = len(test_questions)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n--- TEST {i}/{total_count} ---")
        print(f"VPRAŠANJE: {question}")
        
        result = pipe(question, max_new_tokens=50, do_sample=False, pad_token_id=tokenizer.eos_token_id)
        response = result[0]['generated_text'][len(question):].strip()
        
        print(f"ODGOVOR: {response}")
        
        # Ročno ovrednotenje
        evaluation = input("Je odgovor pravilen? (da/ne/delno): ").lower()
        if evaluation in ['da', 'y', 'yes']:
            correct_count += 1
        elif evaluation in ['delno', 'partial']:
            correct_count += 0.5
            
        print("-" * 60)
    
    accuracy = (correct_count / total_count) * 100
    print(f"\n=== REZULTATI ===")
    print(f"Pravilni odgovori: {correct_count}/{total_count}")
    print(f"Natančnost: {accuracy:.1f}%")

def test_base_vs_knowledge_with_json():
    print("=== PRIMERJAVA BASE vs KNOWLEDGE Z JSON VPRAŠANJI ===")
    
    # Base model
    base_model = AutoModelForCausalLM.from_pretrained(
        "cjvt/GaMS-1B", 
        device_map="auto", 
        torch_dtype=torch.float16
    )
    base_tokenizer = AutoTokenizer.from_pretrained("cjvt/GaMS-1B")
    base_pipe = pipeline("text-generation", model=base_model, tokenizer=base_tokenizer)
    
    # Knowledge integration model
    knowledge_model = PeftModel.from_pretrained(base_model, "outputs/checkpoint-1875")
    knowledge_pipe = pipeline("text-generation", model=knowledge_model, tokenizer=base_tokenizer)
    
    # Naloži vprašanja
    questions = load_questions_from_json("../questions.json")
    test_questions = questions[:10]  # Prvih 10 za primerjavo
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n--- PRIMERJAVA {i} ---")
        print(f"VPRAŠANJE: {question}")
        
        # Base model odgovor
        base_result = base_pipe(question, max_new_tokens=30, pad_token_id=base_tokenizer.eos_token_id)
        base_response = base_result[0]['generated_text'][len(question):].strip()
        
        # Knowledge integration model odgovor
        knowledge_result = knowledge_pipe(question, max_new_tokens=30, do_sample=False, pad_token_id=base_tokenizer.eos_token_id)
        knowledge_response = knowledge_result[0]['generated_text'][len(question):].strip()
        
        print(f"BASE MODEL: {base_response}")
        print(f"KNOWLEDGE MODEL: {knowledge_response}")
        print("-" * 60)

# Dodajte v __main__ blok:
if __name__ == "__main__":
    test_base_model()
    test_finetuned_model()
    test_knowledge_integration()
    test_base_vs_knowledge_comparison()
    
    # TESTI Z JSON VPRAŠANJI
    test_knowledge_integration_with_json()
    test_base_vs_knowledge_with_json()