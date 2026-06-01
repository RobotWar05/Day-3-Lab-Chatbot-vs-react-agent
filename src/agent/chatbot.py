from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger
from src.telemetry.metrics import tracker


CHATBOT_SYSTEM_PROMPT = """You are a helpful AI assistant.
Answer the user's questions accurately and concisely.
If you do not have enough information, say so instead of inventing facts."""


class Chatbot:
    """
    Minimal chatbot baseline.

    This class intentionally does not use tools or ReAct. It is used as the
    comparison baseline for later Agent v1/v2 evaluation.
    """

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def chat(self, user_input: str) -> str:
        logger.log_event("CHATBOT_REQUEST", {
            "input": user_input,
            "model": self.llm.model_name,
        })

        try:
            result = self.llm.generate(
                prompt=user_input,
                system_prompt=CHATBOT_SYSTEM_PROMPT,
            )
        except Exception as exc:
            logger.error(f"Chatbot LLM call failed: {exc}")
            return f"Error: {exc}"

        tracker.track_request(
            provider=result.get("provider", "unknown"),
            model=self.llm.model_name,
            usage=result.get("usage", {}),
            latency_ms=result.get("latency_ms", 0),
        )

        answer = result.get("content", "").strip()
        logger.log_event("CHATBOT_RESPONSE", {
            "output_preview": answer[:200],
            "tokens": result.get("usage", {}),
            "latency_ms": result.get("latency_ms", 0),
        })

        return answer
