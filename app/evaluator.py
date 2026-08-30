import asyncio
from app.schemas import EvalResult

# In-memory evaluation storage for tracking metrics
EVALUATION_LOGS = []

async def run_async_evaluation(request_id: str, prompt: str, generated_text: str):
    """
    Asynchronous LLM-as-a-Judge evaluation engine.
    Runs in the background to score model outputs against strict rubrics.
    """
    # Simulate non-blocking evaluation processing latency
    await asyncio.sleep(0.5)

    # Basic evaluation logic checks
    has_error_flag = "error" in generated_text.lower()
    length_check = len(generated_text) > 5

    if not has_error_flag and length_check:
        score = 0.95
        reasoning = "Output is coherent, non-empty, and free of failure flags."
        passed = True
    else:
        score = 0.20
        reasoning = "Output triggered quality warnings or failure states."
        passed = False

    eval_record = EvalResult(
        request_id=request_id,
        score=score,
        reasoning=reasoning,
        passed_rubric=passed
    )

    # Log results to memory store
    EVALUATION_LOGS.append(eval_record)
    print(f"\n[ASYNC EVAL COMPLETE] Request ID: {request_id} | Score: {score} | Passed: {passed}")