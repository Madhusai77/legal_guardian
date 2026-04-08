---
title: Legal Guardian AI
emoji: ⚖️
colorFrom: blue
colorTo: indigo
sdk: docker
app_file: app.py
pinned: false
---

# Legal Guardian AI Environment

This is an advanced OpenEnv AI training environment for legal harassment resolution in debt collections. 

## Description
This environment simulates a real-world scenario where an AI agent acts as a legal advocate or negotiator to mitigate unfair debt harassment. The agent interacts with a simulated lender or collection agency, submitting legal notices, complaints, and negotiation proposals to achieve a positive resolution while managing the user's stress and compliance.

## Environment Specifications
- **Action Space**: The agent can output JSON encompassing an `action_type` (e.g., `negotiation`, `legal_notice`, `complaint`, `settlement`) and the `content` of the message.
- **Observation Space**: Returns the current session `state` (harassment level, compliance score, legal stage, steps taken, resolution status, user stress), the `message` from the opposing party, and `available_actions`.
- **Reward System**: A comprehensive reward engine provides partial progress signals (e.g., reducing harassment, improving compliance) and penalties (e.g., high stress, inefficiency), clamped between 0.0 and 1.0.

## Tasks and Graders
- **Easy**: Harassment Mitigation - Reduce harassment from medium to low/none.
- **Medium**: Legal Escalation Control - Ensure high compliance score and proper legal stage progression.
- **Hard**: Debt Settlement - Achieve full resolution efficiently with minimal user stress.

## Setup Instructions

### 1. Build and Run via Docker
```bash
docker build -t legal-guardian-ai .
docker run -p 7860:7860 legal-guardian-ai
```

### 2. Run Inference Script
To benchmark a model against this environment:
```bash
export API_BASE_URL="https://api.openai.com/v1"  # Or your custom LLM proxy
export MODEL_NAME="gpt-4o"                       # Target Model
export HF_TOKEN="your-api-key"
python inference.py
```
