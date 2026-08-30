import time
import uuid
import httpx
from app.schemas import LLMRequest, LLMResponse

# In-memory store for simple idempotency tracking (No external DB required)
PROCESSED_KEYS = set()

async def call_primary_llm(prompt: str) -> str:
    """
    Simulates or calls the primary LLM endpoint.
    Raises an exception if simulating a network/service failure.
    """
    # Demonstration: If prompt contains 'fail', simulate primary model downtime
    if "fail" in prompt.lower():
        raise RuntimeError("Primary LLM Service Unavailable (Simulated Error)")
    
    # Simple simulated response for instant execution
    return f"Processed query using Primary-LLM: '{prompt}'"

async def call_fallback_llm(prompt: str) -> str:
    """
    Secondary fallback model used when the primary model fails or times out.
    """
    return f"Processed query using Fallback-LLM (Backup Route): '{prompt}'"

async def process_llm_request(request: LLMRequest) -> LLMResponse:
    """
    Main orchestration logic handling Idempotency, Primary Routing, and Fallback.
    """
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    # 1. Idempotency Check
    if request.idempotency_key:
        if request.idempotency_key in PROCESSED_KEYS:
            return LLMResponse(
                request_id=request_id,
                content="DUPLICATE_REQUEST_BLOCKED: This request was already processed.",
                model_used="none",
                latency_ms=0.0,
                status="idempotent_duplicate"
            )
        PROCESSED_KEYS.add(request.idempotency_key)

    # 2. Primary Routing with Fallback Mechanism
    model_used = "Primary-LLM"
    try:
        content = await call_primary_llm(request.prompt)
    except Exception as e:
        # Gracefully handle primary failure by routing to fallback
        model_used = "Fallback-LLM"
        content = await call_fallback_llm(request.prompt)

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

    return LLMResponse(
        request_id=request_id,
        content=content,
        model_used=model_used,
        latency_ms=elapsed_ms,
        status="success"
    )