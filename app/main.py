from fastapi import FastAPI, BackgroundTasks, HTTPException
from app.schemas import LLMRequest, LLMResponse, EvalResult
from app.proxy import process_llm_request
from app.evaluator import run_async_evaluation, EVALUATION_LOGS
from typing import List

app = FastAPI(
    title="Zapier AI Proxy & Observability Gateway",
    description="Minimal Platform Engine featuring Routing, Fallback, Idempotency, and Async LLM-as-a-Judge Evaluation.",
    version="1.0.0"
)

@app.get("/")
def health_check():
    """Basic health check endpoint."""
    return {"status": "online", "service": "Zapier AI Proxy Gateway"}

@app.post("/v1/chat/completions", response_model=LLMResponse)
async def generate_completion(request: LLMRequest, background_tasks: BackgroundTasks):
    """
    Core Gateway Endpoint:
    1. Validates input schema via Pydantic.
    2. Enforces idempotency & routes to Primary/Fallback LLM.
    3. Triggers Async Evaluation in the background.
    """
    try:
        response = await process_llm_request(request)

        # Trigger background evaluation without blocking the user response
        if response.status == "success":
            background_tasks.add_task(
                run_async_evaluation,
                request_id=response.request_id,
                prompt=request.prompt,
                generated_text=response.content
            )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/evaluations", response_model=List[EvalResult])
def get_evaluation_metrics():
    """Retrieves all logged async evaluation results for observability."""
    return EVALUATION_LOGS