# JobFair: A Framework for Benchmarking Gender Hiring Bias in Large Language Models

This repository contains the data and code for the paper:

> **JobFair: A Framework for Benchmarking Gender Hiring Bias in Large Language Models**
> Ze Wang, Zekun Wu, Xin Guan, Michael Thaler, Adriano Koshiyama, Skylar Lu, Sachin Beepath, Ediz Ertekin, Maria Perez-Ortiz
> *Findings of the Association for Computational Linguistics: EMNLP 2024*, pages 3227–3246.
> [Paper](https://aclanthology.org/2024.findings-emnlp.184/)

## Overview

JobFair is a framework for benchmarking gender hiring bias in LLMs used for resume screening. It introduces a counterfactual evaluation methodology that distinguishes between two types of bias:

- **Level bias**: systematic differences in scores between demographic groups, further decomposed into *statistical bias* (arising from correlations between group membership and qualifications) and *taste-based bias* (arising from group membership alone).
- **Spread bias**: differences in score variance across groups.

The framework evaluates each resume under three conditions — with a male-associated name (Privilege), a female-associated name (Protect), and no name (Neutral) — then applies statistical tests to detect and quantify bias.

## Key Findings

- **10 state-of-the-art LLMs** were evaluated across **3 industries** (Construction, Finance, Healthcare) with **238 unique job roles** and **1,200 resumes per model**.
- 7 out of 10 LLMs exhibited statistically significant male bias in at least one industry.
- Healthcare showed the strongest anti-male bias.
- 8 out of 10 LLMs maintained consistent bias patterns regardless of resume content variation.

## Repository Structure

```
.
├── Code/
│   ├── app.py                  # Streamlit app entry point
│   ├── requirements.txt        # Python dependencies
│   ├── pages/
│   │   ├── 1_Injection.py      # Resume processing with LLMs
│   │   └── 2_Evaluation.py     # Statistical evaluation of results
│   └── util/
│       ├── evaluation.py       # Statistical tests and bias metrics
│       ├── injection.py        # Resume scoring pipeline with counterfactual injection
│       ├── model.py            # LLM agents (GPT-4, Azure OpenAI, Claude 3)
│       ├── plot.py             # Visualization (3D scatter, heatmaps, distributions)
│       └── prompt.py           # Prompt template for resume evaluation
├── Data/
│   └── final_data.csv          # Experiment results (10 models, 12,000 rows)
├── LICENSE
└── README.md
```

## Data

`Data/final_data.csv` contains the full experiment results (12,000 rows) across 10 LLMs:

**Models**: GPT-4, GPT-3.5, GPT-4o, Mistral-Large, Claude-Sonnet, Claude-Haiku, Gemini-1.5-Pro, Gemini-1.5-Flash, Llama3-70b-Instruct, Llama3-8b-Instruct

**Industries**: Construction, Finance, Healthcare (4,000 rows each)

| Column | Description |
|--------|-------------|
| `Industry`, `Role` | Job category and specific role |
| `Original_Resume`, `Preprocessed_Resume` | Resume text (original and cleaned) |
| `Privilege_Scores`, `Privilege_Avg_Score` | Scores with male-associated name |
| `Protect_Scores`, `Protect_Avg_Score` | Scores with female-associated name |
| `Neutral_Scores`, `Neutral_Avg_Score` | Scores with no name |
| `Privilege_Rank`, `Protect_Rank`, `Neutral_Rank` | Within-resume score rankings (1–3) |
| `model` | LLM used for evaluation |

## Code

The code is a Streamlit application for running and evaluating the JobFair benchmark.

### Running the app

```bash
cd Code
pip install -r requirements.txt
streamlit run app.py
```

### Key components

- **Injection** (`util/injection.py`): Processes resumes by injecting counterfactual group information into prompts, sending to an LLM, and extracting scores with retry logic and JSON repair.
- **Evaluation** (`util/evaluation.py`): Comprehensive statistical testing including permutation tests (for mean and variance), Wilcoxon signed-rank tests, Friedman test with Nemenyi post-hoc, and bias metrics (Statistical Parity Difference, Disparate Impact Ratio, Four-Fifths Rule).
- **Model Agents** (`util/model.py`): Unified interface for GPT-4 (Azure OpenAI), Claude 3 (AWS Bedrock), and Azure-hosted models.
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
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2024",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.findings-emnlp.184/",
    pages = "3227--3246",
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
