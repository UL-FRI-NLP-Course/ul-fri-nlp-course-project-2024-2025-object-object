# Natural language processing course: `Integrating Structured Knowledge into Large Language Models`

## Introduction

The rapid advancement of Large Language Models (LLMs) has significantly improved natural language understanding and generation. However, these models often struggle with complex reasoning tasks that require structured knowledge. This project explores techniques for integrating knowledge graphs (KGs) into LLMs to enhance their ability to answer complex questions accurately.

Our focus is on incorporating structured Slovenian linguistic data into LLMs using knowledge graphs. The aim is to improve the model's performance by leveraging semantic relationships within the Slovenian Digital Dictionary Database and other linguistic sources. The project will evaluate various integration techniques and their impact on model accuracy and reasoning capabilities.

## Existing Solutions and Related Work

Several studies have explored the combination of knowledge graphs and LLMs. Some key works include:

1. **GraphGPT: Graph Instruction Tuning for Large Language Models**  
   Tang et al. (2024) explored methods for tuning LLMs with graph-structured data, demonstrating the benefits of structured knowledge in language generation.

2. **Combining Knowledge Graphs and Large Language Models**  
   Kau et al. (2024) discussed various methodologies for integrating KGs into LLMs, including direct augmentation and embedding-based techniques.

3. **Deep Bidirectional Language-Knowledge Graph Pretraining**  
   Yasunaga et al. (2022) examined how bidirectional pretraining with language and knowledge graph structures can enhance model performance.

4. **Graph Language Models**  
   Plenz & Frank (2024) proposed novel architectures for graph-based language modeling, relevant to our approach of integrating Slovenian linguistic data.

5. **Chain-of-Knowledge: Integrating Knowledge Reasoning into Large Language Models by Learning from Knowledge Graphs**  
   Zhang et al. (2024) explored integrating knowledge reasoning into LLMs by learning from knowledge graphs.

6. **InfuserKI: Enhancing Large Language Models with Knowledge Graphs via Infuser-Guided Knowledge Integration**  
   Wang et al. (2024) proposed enhancing LLMs with knowledge graphs via infuser-guided knowledge integration.

These studies provide a strong foundation for exploring KG-based integration techniques to enhance LLMs.

## Initial Ideas and Methodology

### 1. Literature Review
A thorough review of existing methodologies for integrating knowledge graphs into LLMs will be conducted. This will include analyzing methods such as direct input augmentation, graph embeddings, and attention-based fusion techniques.

### 2. Creation of an Evaluation Set
We will construct an evaluation dataset consisting of complex questions related to Slovenian linguistics. Each question will be paired with relevant knowledge graphs that contain hints for the model.

### 3. Selection of Integration Techniques
Potential techniques for injecting knowledge graphs into LLMs include:
- **Direct input augmentation**: Incorporating KG-based facts into the model’s prompt.
- **Graph embedding-based integration**: Converting knowledge graphs into vector representations and feeding them into the model.
- **Attention-based fusion**: Modifying the model's attention mechanism to prioritize structured knowledge.

### 4. Implementation of Knowledge Graph Injection
The chosen methods will be implemented, and the performance of different integration techniques will be evaluated using Slovenian linguistic data.

### 5. Evaluation and Performance Analysis
Performance metrics such as accuracy, precision, recall, and F1-score will be used to measure the effectiveness of each integration method.

## Proposed Project Dataset

The primary dataset for this project will be sourced from the **Slovenian Digital Dictionary Database**. This dataset contains structured linguistic information crucial for our integration techniques.

Additionally, we may incorporate other Slovenian linguistic resources and adapt existing datasets where necessary. The dataset will be preprocessed and merged with other sources, ensuring its compatibility with knowledge graph structures.

## Repository Organization

A well-organized repository will be maintained to ensure proper documentation and version control. The repository will include:

- `/docs/`: Literature review, methodology, and project documentation.
- `/data/`: Processed dataset files and knowledge graphs.
- `/notebooks/`: Jupyter notebooks for data analysis and preprocessing.
- `/src/`: Source code for model integration and evaluation.
- `/results/`: Performance analysis and evaluation reports.

The repository will be structured to facilitate collaboration among team members and ensure reproducibility of results.

## Conclusion

This project aims to enhance the reasoning capabilities of LLMs by integrating structured knowledge graphs, focusing on Slovenian linguistic data. By leveraging existing research and exploring innovative integration techniques, we aim to improve the accuracy and efficiency of LLMs in handling complex linguistic queries.

## References

1. Tang, J., et al. (2024). *GraphGPT: Graph instruction tuning for large language models*. Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval.

2. Kau, A., He, X., Nambissan, A., Astudillo, A., Yin, H., & Aryani, A. (2024). *Combining Knowledge Graphs and Large Language Models*. arXiv preprint arXiv:2407.06564.

3. Yasunaga, M., et al. (2022). *Deep bidirectional language-knowledge graph pretraining*. Advances in Neural Information Processing Systems 35, pp. 37309-37323.

4. Plenz, M., & Frank, A. (2024). *Graph Language Models*. arXiv preprint arXiv:2401.07105.

5. Zhang, Y., Wang, X., Liang, J., Xia, S., Chen, L., & Xiao, Y. (2024). *Chain-of-knowledge: Integrating knowledge reasoning into large language models by learning from knowledge graphs*. arXiv preprint arXiv:2407.00653.

6. Wang, F., Bao, R., Wang, S., Yu, W., Liu, Y., Cheng, W., & Chen, H. (2024). *InfuserKI: Enhancing large language models with knowledge graphs via infuser-guided knowledge integration*. arXiv preprint arXiv:2402.11441.

