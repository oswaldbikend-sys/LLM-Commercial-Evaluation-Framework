# LLM Commercial Evaluation & RLHF Framework

## Overview
This repository demonstrates a structured methodology for evaluating Large Language Models (LLMs) in complex, real-world commercial scenarios. It simulates the RLHF (Reinforcement Learning from Human Feedback) pipeline by auditing model responses for factual accuracy, logical consistency, tone, and safety. 

## Methodology
To efficiently generate the dataset, I built an automated Python pipeline using Google's Gemini API:
1. **Adversarial Prompt Generation:** Created 50 complex commercial prompts (e.g., users demanding refunds violating policies, contradictory instructions, prompt injection attempts).
2. **Concurrent Model Output:** Generated side-by-side responses instructing Model A to use a strict corporate tone, and Model B to use an empathetic, flexible tone.
3. **Automated Baseline Evaluation:** Used a foundational model as an initial RLHF judge to categorize flaws (Hallucination, Tone, Logic Error).
4. **Human-in-the-Loop (HITL) Audit:** Conducted a rigorous manual review of the generated dataset to refine the English justifications, correct the AI judge's verdicts, and ensure high-fidelity evaluation.

## Skills Demonstrated
* **AI Evaluation & RLHF:** Auditing responses for safety, factual alignment, and logical soundness.
* **Prompt Engineering:** Designing multimodal and complex commercial scenarios.
* **Critical Analysis (Bilingual):** Providing highly analytical justifications in English for Spanish prompts.
* **Automation:** Python scripting and API integration to accelerate data generation.

## Repository Contents
* `generar_dataset.py`: The Python script used to automate the generation of prompts and initial baseline evaluations.
* `dataset_evaluacion.csv`: The final dataset containing 50 evaluated interactions, complete with identified flaws and human-refined justifications.
