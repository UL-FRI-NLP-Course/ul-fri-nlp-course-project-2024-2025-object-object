# Natural language processing course: `Integrating Structured Knowledge into Large Language Models`

## About

This project explores techniques for improving Large Language Models (LLMs) by integrating structured knowledge from knowledge graphs (KGs). Focusing on subset of Wikidata's data about the Slovenian counties, cities, castles, rivers and mountain peaks, we aim to improve the model's ability to accurately answer complex questions by leveraging semantic relationships. This repository contains the code, data, and documentation for our experiments with various KG integration methods, including direct input augmentation, graph embedding-based integration, and attention-based fusion techniques.

## Repository Organization

- `/docs/`: Project documentation, literature review, and methodology details.
- `/data/`: Processed dataset files containing knowledge graph triples and raw data.
- `/src/`: Source code for implementing KG integration techniques and model evaluation.
- `/results/`: Performance analysis, evaluation reports, and visualizations.

## Get Started

To get started with the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/UL-FRI-NLP-Course/ul-fri-nlp-course-project-2024-2025-object-object

2. Navigate to the project directory:
   ```bash
   cd ul-fri-nlp-course-project-2024-2025-object-object
   ```
3. Create a virtual environment and install dependencies (eg. virtualenv or conda):
   ```bash
   virtualenv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```

#### Note

If you encounter issues with the virtual environment being recognized by the Jupyter Notebook, you can export the notebook to a Python script and run it directly.

### Dataset Preparation

An example notebook for how to generate a knowledge graph can be found in the `src/knowledge_graph.ipynb` file. The process does not require a GPU, but it does require an internet connection to download the necessary data from Wikidata using our proprietary client. If you do not want to run the notebook, you can view the output data in the `data/municipalities_peaks_castles.graphml` file, which is used for downstream tasks as well.

### Questions & Answers Generation

An example notebook for how to generate questions and answers from the knowledge graph can be found in the `src/qa_generation.ipynb` file. The process does not require a GPU and does not require an internet connection, however the `data/municipalities_peaks_castles.graphml` file must be present.

### Evaluation

#### RAG Method

An example notebook for how to evaluate the RAG method can be found in the `src/rag_evaluation.ipynb` file. The process requires a GPU but no internet connection. The `data/municipalities_peaks_castles.graphml` file must be present, as questions are generated inline.