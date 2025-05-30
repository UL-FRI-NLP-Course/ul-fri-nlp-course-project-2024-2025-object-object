import json
import networkx as nx
import os
from qa.generator import QAGenerator
from qa.templates import TEMPLATES

def generate_knowledge_jsonl(graph_path, output_path, num_samples=5000):
    """Ustvari QA pare BREZ podatkov v promptu - za knowledge integration"""
    
    # 1. Naloži graf
    graph = nx.read_graphml(graph_path)
    print(f"Naložen graf: {graph.number_of_nodes()} vozlišč, {graph.number_of_edges()} povezav")
    
    # 2. Generiraj QA pare
    generator = QAGenerator()
    qas = generator.generate_questions(
        graph, 
        TEMPLATES, 
        num_questions=num_samples,
        add_distractors=0  # POMEMBNO: brez distraktov!
    )
    
    # 3. Pretvori v KNOWLEDGE INTEGRATION format
    training_data = []
    for qa in qas:
        # SAMO vprašanje, BREZ podatkov!
        entry = {
            "instruction": "Odgovori na vprašanje o Sloveniji.",
            "input": qa.question,  # Samo vprašanje!
            "output": qa.answer
        }
        training_data.append(entry)
    
    # 4. Ustvari direktorij, če ne obstaja
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 5. Shrani v .jsonl
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in training_data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"Shranjenih {len(training_data)} primerov v {output_path}")
    return training_data

def inspect_knowledge_data(jsonl_path, num_samples=10):
    """Preveri generirane podatke"""
    try:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= num_samples:
                    break
                data = json.loads(line)
                print(f"\n--- Primer {i+1} ---")
                print(f"Vprašanje: {data['input']}")
                print(f"Odgovor: {data['output']}")
                print("-" * 40)
    except FileNotFoundError:
        print(f"Datoteka {jsonl_path} ne obstaja!")

if __name__ == "__main__":
    # Uporabi absolutne poti
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    graph_path = os.path.join(base_dir, "data", "municipalities_peaks_castles.graphml")
    output_path = os.path.join(base_dir, "data", "slovenian_knowledge_training.jsonl")
    
    # Generiraj knowledge integration dataset
    generate_knowledge_jsonl(
        graph_path=graph_path,
        output_path=output_path,
        num_samples=5000
    )
    
    # Preveri podatke
    inspect_knowledge_data(output_path)