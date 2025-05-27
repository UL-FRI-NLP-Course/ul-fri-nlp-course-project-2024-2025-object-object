import json
import networkx as nx
from qa.generator import QAGenerator
from qa.templates import TEMPLATES

def generate_training_jsonl(graph_path, output_path, num_samples=1000):
    """Pretvori .graphml v .jsonl za fine-tuning"""
    
    # 1. Naloži graf
    graph = nx.read_graphml(graph_path)
    print(f"Naložen graf: {graph.number_of_nodes()} vozlišč, {graph.number_of_edges()} povezav")
    
    # 2. Generiraj QA pare
    generator = QAGenerator()
    qas = generator.generate_questions(
        graph, 
        TEMPLATES, 
        num_questions=num_samples,
        add_distractors=5
    )
    
    # 3. Pretvori v instruction-tuning format
    training_data = []
    for qa in qas:
        context = " ".join([str(fact) for fact in qa.context_facts])
        
        entry = {
            "instruction": "Odgovori na vprašanje na podlagi podanih podatkov.",
            "input": f"Podatki: {context}\nVprašanje: {qa.question}",
            "output": qa.answer
        }
        training_data.append(entry)
    
    # 4. Shrani v .jsonl
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in training_data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"Shranjenih {len(training_data)} primerov v {output_path}")
    return training_data

if __name__ == "__main__":
    generate_training_jsonl(
        graph_path="data\municipalities_peaks_castles.graphml",
        output_path="data\slovenian_qa_training.jsonl",
        num_samples=5000
    )