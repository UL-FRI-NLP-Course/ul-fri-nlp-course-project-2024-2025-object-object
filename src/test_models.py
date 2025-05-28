from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from peft import PeftModel
import torch

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
    
    test_prompt = """Odgovori na vprašanje na podlagi podanih podatkov.

Podatki: <Občina Ljubljana> <se_nahaja_v> <osrednjeslovenska statistična regija>.

Vprašanje: V kateri regiji se nahaja občina Ljubljana?

"""
    
    result = pipe(test_prompt, max_new_tokens=50, pad_token_id=tokenizer.eos_token_id)
    print("BASE MODEL ODGOVOR:")
    print(result[0]['generated_text'][len(test_prompt):])
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
    
    test_cases = [
        """Odgovori na vprašanje na podlagi podanih podatkov.

Podatki: <Občina Ljubljana> <se_nahaja_v> <osrednjeslovenska statistična regija>. <Občina Ljubljana> <ima_populacijo> <294113>.

Vprašanje: V kateri regiji se nahaja občina Ljubljana?

""",
        """Odgovori na vprašanje na podlagi podanih podatkov.

Podatki: <Triglav> <ima_višino> <2864.0>. <Triglav> <se_nahaja_v> <Občina Kranjska Gora>.

Vprašanje: Kakšna je višina Triglava?

""",
        """Odgovori na vprašanje na podlagi podanih podatkov.

Podatki: <Grad Bled> <se_nahaja_v> <Občina Bled>. <Občina Bled> <se_nahaja_v> <gorenjska statistična regija>.

Vprašanje: V kateri statistični regiji stoji grad Bled?

"""
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
    
    # Test vprašanja BREZ podatkov v promptu
    knowledge_tests = [
        "V kateri regiji se nahaja Ljubljana?",
        "Kakšna je višina Triglava?", 
        "V kateri občini stoji grad Bled?",
        "Koliko prebivalcev ima občina Maribor?",
        "V kateri statistični regiji leži Koper?",
        "Kakšna je površina občine Kranj?",
        "V kateri občini leži vrh Vogel?",
        "Pod kateri status kulturne dediščine spada grad Predjama?"
    ]
    
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
    
    test_questions = [
        "V kateri regiji se nahaja Ljubljana?",
        "Kakšna je višina Triglava?",
        "V kateri občini stoji grad Bled?"
    ]
    
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

if __name__ == "__main__":
    test_base_model()
    test_finetuned_model()  # Graph-RAG testiranje
    test_knowledge_integration()  # Knowledge integration testiranje
    test_base_vs_knowledge_comparison()  # Direktna primerjava