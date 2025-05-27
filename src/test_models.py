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

if __name__ == "__main__":
    test_base_model()
    test_finetuned_model()