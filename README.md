# Zapier AI Proxy & Observability Gateway

A minimal Python AI Platform Gateway engine demonstrating core enterprise LLM infrastructure patterns: **Dynamic Model Fallback Routing**, **Idempotency Execution Rules**, and **Asynchronous LLM-as-a-Judge Evaluation**.

---

## Key Features

* **Idempotency Layer**: Blocks duplicate API calls using an idempotency key to prevent unnecessary token consumption and redundant costs.
* **Automatic Failover Routing**: Dynamically detects primary model failures or timeouts and reroutes requests to a fallback backup model without client-side downtime.
* **Async LLM-as-a-Judge**: Runs non-blocking evaluation tasks in the background using FastAPI `BackgroundTasks` to score model outputs against defined quality rubrics.
* **Schema Validation & Guardrails**: Enforces type safety, strict payload structures, and boundary checks using `Pydantic`.

---

## Project Structure

```text
zap-ai-proxy-eval/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI Gateway routes & Background Tasks setup
│   ├── proxy.py         # Routing, Fallback, & Idempotency logic
│   ├── evaluator.py     # Async evaluation engine (LLM-as-a-Judge)
│   └── schemas.py       # Pydantic data validation schemas
├── requirements.txt     # Dependencies
└── README.md

```
---

## Quick Start

* **1- Install Dependencies**
# pip install fastapi uvicorn pydantic

* **2-Run the Gateway Server**
# python -m uvicorn app.main:app --reload

* **3-Interactive Documentation**
# Open your browser and navigate to http://127.0.0.1:8000/docs to interact with the API endpoints via Swagger UI.