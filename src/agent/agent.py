import re
from typing import Any, Dict, List

from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger
from src.telemetry.metrics import tracker


class ReActAgent:
    """
    ReAct-style Agent that follows the Thought -> Action -> Observation loop.

    The LLM decides which tool to call, but Python code executes the tool.
    This is the key difference from a plain chatbot.
    """

    _ACTION_RE = re.compile(r"Action\s*:\s*(\w+)\s*\((.*?)\)", re.IGNORECASE | re.DOTALL)
    _FINAL_RE = re.compile(r"Final Answer\s*:\s*(.+)", re.IGNORECASE | re.DOTALL)

    def __init__(self, llm: LLMProvider, tools: List[Dict[str, Any]], max_steps: int = 5):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.history = []

    def get_system_prompt(self) -> str:
        """
        Build the system prompt that instructs the LLM to use ReAct.
        """
        tool_descriptions = "\n".join(
            f"- {tool['name']}: {tool['description']}" for tool in self.tools
        )
        return f"""You are a practical ReAct agent for local place recommendations.

AVAILABLE TOOLS:
{tool_descriptions}

RESPONSE FORMAT:
Use exactly one of these formats.

If you need a tool:
Thought: <reason about what information is needed>
Action: tool_name(argument)

If you have enough information:
Thought: <short final reasoning>
Final Answer: <answer to the user>

STRICT RULES:
- Use tools for nearby food, drink, grocery, market, or mall recommendations.
- Do not invent nearby places from memory.
- If the user did not provide a clear location, ask for the location in Final Answer.
- Call only one tool per step.
- Use only tool names listed in AVAILABLE TOOLS.
- Never fabricate Observation. Wait for the code to provide it.
- When a tool returns enough useful places, produce Final Answer.
"""

    def run(self, user_input: str) -> str:
        """
        Run the ReAct loop until Final Answer or max_steps.
        """
        logger.log_event("AGENT_START", {
            "input": user_input,
            "model": self.llm.model_name,
            "max_steps": self.max_steps,
        })

        scratchpad = f"User Question: {user_input}\n\n"
        steps = 0
        total_tokens = 0

        while steps < self.max_steps:
            steps += 1

            try:
                result = self.llm.generate(
                    prompt=scratchpad,
                    system_prompt=self.get_system_prompt(),
                )
            except Exception as exc:
                logger.error(f"Agent LLM call failed at step {steps}: {exc}")
                logger.log_event("AGENT_LLM_ERROR", {"step": steps, "error": str(exc)})
                return f"Agent error: {exc}"

            llm_output = result.get("content", "").strip()
            usage = result.get("usage", {})
            total_tokens += usage.get("total_tokens", 0)

            tracker.track_request(
                provider=result.get("provider", "unknown"),
                model=self.llm.model_name,
                usage=usage,
                latency_ms=result.get("latency_ms", 0),
            )

            logger.log_event("AGENT_LLM_RESPONSE", {
                "step": steps,
                "output_preview": llm_output[:300],
                "tokens": usage,
                "latency_ms": result.get("latency_ms", 0),
            })

            final_match = self._FINAL_RE.search(llm_output)
            if final_match:
                final_answer = final_match.group(1).strip()
                logger.log_event("AGENT_END", {
                    "status": "success",
                    "steps": steps,
                    "total_tokens": total_tokens,
                    "answer_preview": final_answer[:200],
                })
                return final_answer

            action_match = self._ACTION_RE.search(llm_output)
            if action_match:
                tool_name = action_match.group(1).strip()
                args = action_match.group(2).strip()

                logger.log_event("AGENT_ACTION", {
                    "step": steps,
                    "tool": tool_name,
                    "argument": args,
                })

                observation = self._execute_tool(tool_name, args)
                logger.log_event("AGENT_OBSERVATION", {
                    "step": steps,
                    "tool": tool_name,
                    "observation_preview": observation[:300],
                })

                scratchpad += f"{llm_output}\nObservation: {observation}\n\n"
                continue

            logger.log_event("AGENT_PARSE_FAILURE", {
                "step": steps,
                "raw_output": llm_output[:500],
            })
            scratchpad += (
                f"{llm_output}\n"
                "Observation: Invalid format. Use either Action: tool_name(argument) "
                "or Final Answer: <answer>.\n\n"
            )

        logger.log_event("AGENT_END", {
            "status": "max_steps_exceeded",
            "steps": steps,
            "total_tokens": total_tokens,
        })
        return (
            f"Agent reached max_steps={self.max_steps} without a final answer. "
            "Try asking with a clearer location and category."
        )

    def _execute_tool(self, tool_name: str, args: str) -> str:
        """
        Execute a registered tool by name.
        """
        for tool in self.tools:
            if tool["name"].lower() == tool_name.lower():
                try:
                    result = tool["function"](args)
                    return str(result)
                except Exception as exc:
                    logger.error(f"Tool '{tool_name}' failed: {exc}", exc_info=False)
                    return f"Tool error in '{tool_name}': {exc}"

        available = ", ".join(tool["name"] for tool in self.tools)
        return f"Tool '{tool_name}' not found. Available tools: {available}."
