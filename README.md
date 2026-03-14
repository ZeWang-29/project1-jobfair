# JobFair: A Framework for Benchmarking Gender Hiring Bias in Large Language Models

This repository contains the data and code for the paper:

> **JobFair: A Framework for Benchmarking Gender Hiring Bias in Large Language Models**
> Ze Wang, Zekun Wu, Xin Guan, Michael Thaler, Adriano Koshiyama, Skylar Lu, Sachin Beepath, Ediz Ertekin, Maria Perez-Ortiz
> *Findings of the Association for Computational Linguistics: EMNLP 2024*, pages 3227–3246.
> [Paper](https://aclanthology.org/2024.findings-emnlp.184/)

## Overview

JobFair is a framework for benchmarking gender hiring bias in LLMs. It uses a counterfactual approach: the same resume is presented to an LLM three times — with a male-associated name (Privilege), a female-associated name (Protect), and no name (Neutral). The LLM scores each resume 0–10 for a given job role. Statistical tests then measure whether scores differ systematically across groups.

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
│       ├── evaluation.py       # Statistical tests (permutation, Wilcoxon, Friedman, bias metrics)
│       ├── injection.py        # Resume scoring pipeline with counterfactual injection
│       ├── model.py            # LLM agents (GPT-4, Azure OpenAI, Claude 3)
│       ├── plot.py             # Visualization (3D scatter, heatmaps, distributions)
│       └── prompt.py           # Prompt template for resume evaluation
├── Data/
│   └── final_data.csv          # Experiment results (GPT-4, 116K rows)
├── LICENSE
└── README.md
```

## Data

`Data/final_data.csv` contains the full experiment results with the following columns:

| Column | Description |
|--------|-------------|
| `Industry`, `Role` | Job category |
| `Original_Resume`, `Preprocessed_Resume` | Resume text |
| `Privilege_Scores`, `Privilege_Avg_Score` | Scores with male-associated name |
| `Protect_Scores`, `Protect_Avg_Score` | Scores with female-associated name |
| `Neutral_Scores`, `Neutral_Avg_Score` | Scores with no name |
| `Privilege_Rank`, `Protect_Rank`, `Neutral_Rank` | Within-resume score rankings (1–3) |
| `model` | LLM used (GPT-4) |

## Code

The code is a Streamlit application for running and evaluating the JobFair benchmark.

### Running the app

```bash
cd Code
pip install -r requirements.txt
streamlit run app.py
```

### Key components

- **Injection** (`util/injection.py`): Processes resumes by injecting counterfactual group information (privilege/protect/neutral) into prompts, sending to an LLM, and extracting scores.
- **Evaluation** (`util/evaluation.py`): Statistical tests including permutation tests, Wilcoxon signed-rank tests, Friedman test with Nemenyi post-hoc, and bias metrics (Statistical Parity Difference, Disparate Impact Ratio, Four-Fifths Rule).
- **Visualization** (`util/plot.py`): 3D scatter plots with ideal fairness line, correlation heatmaps, and score distributions.

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
