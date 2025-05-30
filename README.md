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

### Dataset Preparation

An example notebook for how to generate a knowledge graph can be found in the `src/knowledge_graph.ipynb` file. This notebook demonstrates how to process the raw data and create a knowledge graph from it. If you are having issues running the notebook using the virtual environment, export the notebook to a Python script and run it directly.