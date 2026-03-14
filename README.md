# JobFair: A Framework for Benchmarking Gender Hiring Bias in Large Language Models

This repository contains the data and code for the paper:

> **JobFair: A Framework for Benchmarking Gender Hiring Bias in Large Language Models**
> Ze Wang, Zekun Wu, Xin Guan, Michael Thaler, Adriano Koshiyama, Qinyang Lu, Sachin Beepath, Ediz Ertekin Jr., Maria Perez-Ortiz
> *Findings of the Association for Computational Linguistics: EMNLP 2024*, pages 3227–3246.
> [Paper](https://aclanthology.org/2024.findings-emnlp.184/)

## Overview

JobFair is a statistics-based framework for benchmarking hierarchical gender hiring bias in LLMs used for resume scoring. Grounded in labour economics and legal principles, it introduces a hierarchical construct of hiring bias:

- **Level bias**: systematic differences in average outcomes between demographic counterfactual groups, further decomposed into:
  - *Taste-based bias*: consistent regardless of resume content/length (inherent prejudice)
  - *Statistical bias*: varies with the amount of non-demographic information available
- **Spread bias**: differences in the variance of outcomes between groups

The framework uses a counterfactual approach inspired by the Rubin Causal Model: each resume is scored three times — with "Gender: Male", "Gender: Female", and no gender label (Neutral). Scores are converted to ranks via **Ranking After Scoring (RAS)** with descending fractional ranking.

## Key Findings

- **10 LLMs** evaluated across **3 industries** (Construction, Finance, Healthcare) using **300 real resumes** (100 per industry) at 4 information proportions (10%, 40%, 60%, 100%), totaling **36,000 API requests**.
- **7 out of 10 LLMs** exhibit significant Level bias against males in at least one industry.
- **No significant Spread bias** was observed across any model.
- An industry-effect regression reveals **Healthcare** as the most biased against males.
- **8 out of 10 LLMs** show no Statistical bias — their bias remains consistent regardless of resume length, indicating **Taste-based bias**.
- Only Llama3-8b-Instruct and Claude-3-Sonnet exhibit Statistical bias (bias level changes with information density).

## Models Evaluated

| Model | Provider | Platform |
|-------|----------|----------|
| GPT-3.5 (2023-11-06) | OpenAI | Azure OpenAI Studio |
| GPT-4 (2023-11-06) | OpenAI | Azure OpenAI Studio |
| GPT-4o (2024-05-13) | OpenAI | Azure OpenAI Studio |
| Gemini-1.5-Flash (001) | Google DeepMind | Google Cloud Vertex AI |
| Gemini-1.5-Pro (001) | Google DeepMind | Google Cloud Vertex AI |
| Llama3-8b-Instruct | Meta AI | Azure ML Studio |
| Llama3-70b-Instruct | Meta AI | Azure ML Studio |
| Claude-3-Haiku | Anthropic | AWS Bedrock |
| Claude-3-Sonnet | Anthropic | AWS Bedrock |
| Mistral-Large | Mistral AI | Azure ML Studio |

## Repository Structure

```
.
├── Code/
│   ├── app.py                  # Streamlit app entry point
│   ├── requirements.txt        # Python dependencies
│   ├── pages/
│   │   ├── 1_Injection.py      # Resume processing with LLMs (counterfactual injection)
│   │   └── 2_Evaluation.py     # Statistical evaluation of results
│   └── util/
│       ├── evaluation.py       # Statistical tests and bias metrics
│       ├── injection.py        # Resume scoring pipeline with counterfactual injection
│       ├── model.py            # LLM agents (GPT, Claude 3, Azure-hosted models)
│       ├── plot.py             # Visualization (3D scatter, heatmaps, distributions)
│       └── prompt.py           # Prompt template for resume evaluation
├── Data/
│   └── final_data.csv          # Experiment results (10 models, 12,000 rows)
├── LICENSE
└── README.md
```

## Data

`Data/final_data.csv` contains the full experiment results (12,000 rows = 10 models × 300 resumes × 4 proportions).

**Models**: GPT-4, GPT-3.5, GPT-4o, Mistral-Large, Claude-Sonnet, Claude-Haiku, Gemini-1.5-Pro, Gemini-1.5-Flash, Llama3-70b-Instruct, Llama3-8b-Instruct

**Industries**: Construction, Finance, Healthcare (4,000 rows each)

| Column | Description |
|--------|-------------|
| `Industry`, `Role` | Job category and specific role |
| `Original_Resume`, `Preprocessed_Resume` | Resume text (original and cleaned) |
| `proportion` | Information proportion used (0.1, 0.4, 0.6, 1.0) |
| `Privilege_Scores`, `Privilege_Avg_Score` | Scores with "Gender: Male" |
| `Protect_Scores`, `Protect_Avg_Score` | Scores with "Gender: Female" |
| `Neutral_Scores`, `Neutral_Avg_Score` | Scores with no gender label |
| `Privilege_Rank`, `Protect_Rank`, `Neutral_Rank` | Within-resume rankings (1=highest, 3=lowest) |
| `model` | LLM used for evaluation |

**Resume Dataset**: The 300 source resumes (from LiveCareer via Kaggle) are available at [HuggingFace](https://huggingface.co/datasets/holisticai/job-fair-resume).

## Code

The code is a Streamlit application for running and evaluating the JobFair benchmark.

### Running the app

```bash
cd Code
pip install -r requirements.txt
streamlit run app.py
```

### Key components

- **Injection** (`util/injection.py`): Processes resumes by injecting counterfactual gender information into prompts, sending to an LLM, and extracting scores with retry logic and JSON repair.
- **Evaluation** (`util/evaluation.py`): Statistical testing suite including:
  - Permutation tests (100,000 permutations) for mean and variance differences
  - Wilcoxon signed-rank tests
  - Friedman test with Nemenyi post-hoc
  - Bias metrics: Statistical Parity Difference, Disparate Impact Ratio, Four-Fifths Rule
- **Model Agents** (`util/model.py`): Unified interface for GPT (Azure OpenAI), Claude 3 (AWS Bedrock), and Azure ML-hosted models. API keys should be provided via environment variables or constructor parameters.
- **Visualization** (`util/plot.py`): 3D scatter plots with ideal fairness line, correlation heatmaps (Pearson, Spearman, Kendall), and score distributions.

## Citation

```bibtex
@inproceedings{wang-etal-2024-jobfair,
    title = "{J}ob{F}air: A Framework for Benchmarking Gender Hiring Bias in Large Language Models",
    author = "Wang, Ze  and
      Wu, Zekun  and
      Guan, Xin  and
      Thaler, Michael  and
      Koshiyama, Adriano  and
      Lu, Skylar  and
      Beepath, Sachin  and
      Ertekin, Ediz  and
      Perez-Ortiz, Maria",
    editor = "Al-Onaizan, Yaser  and
      Bansal, Mohit  and
      Chen, Yun-Nung",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2024",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.findings-emnlp.184/",
    doi = "10.18653/v1/2024.findings-emnlp.184",
    pages = "3227--3246",
    abstract = "The use of Large Language Models (LLMs) in hiring has led to legislative actions to protect vulnerable demographic groups. This paper presents a novel framework for benchmarking hierarchical gender hiring bias in Large Language Models (LLMs) for resume scoring, revealing significant issues of reverse gender hiring bias and overdebiasing. Our contributions are fourfold: Firstly, we introduce a new construct grounded in labour economics, legal principles, and critiques of current bias benchmarks: hiring bias can be categorized into two types: Level bias (difference in the average outcomes between demographic counterfactual groups) and Spread bias (difference in the variance of outcomes between demographic counterfactual groups); Level bias can be further subdivided into statistical bias (i.e. changing with non-demographic content) and taste-based bias (i.e. consistent regardless of non-demographic content). Secondly, the framework includes rigorous statistical and computational hiring bias metrics, such as Rank After Scoring (RAS), Rank-based Impact Ratio, Permutation Test, and Fixed Effects Model. Thirdly, we analyze gender hiring biases in ten state-of-the-art LLMs. Seven out of ten LLMs show significant biases against males in at least one industry. An industry-effect regression reveals that the healthcare industry is the most biased against males. Moreover, we found that the bias performance remains invariant with resume content for eight out of ten LLMs. This indicates that the bias performance measured in this paper might apply to other resume datasets with different resume qualities. Fourthly, we provide a user-friendly demo and resume dataset to support the adoption and practical use of the framework, which can be generalized to other social traits and tasks."
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
