import json

from src.agent.agent import ReActAgent
from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger
from src.tools.nearby_tools import extract_location_and_need, get_nearby_tools


class NearbyAgentV2:
    """
    Improved nearby-place Agent.

    Improvements over Agent v1:
    - Deterministic pre-check for missing location before calling the LLM.
    - Normalized context is injected into the ReAct prompt.
    - Stricter system prompt focused on local recommendation behavior.
    """

    def __init__(self, llm: LLMProvider, max_steps: int = 5):
        self.llm = llm
        self.tools = get_nearby_tools()
        self._agent = ReActAgent(llm=llm, tools=self.tools, max_steps=max_steps)
        self._agent.get_system_prompt = self.get_system_prompt
        self.pending_query = ""

    def get_system_prompt(self) -> str:
        tool_descriptions = "\n".join(
            f"- {tool['name']}: {tool['description']}" for tool in self.tools
        )
        return f"""You are Nearby Food & Coffee Agent v2.

Your job is to recommend nearby places around VinUni, Ocean Park, and Gia Lam.
Supported categories:
- food: restaurants and meals
- drink: coffee, cafe, milk tea, drinks
- grocery: supermarket and daily goods
- market: local markets
- mall: shopping centers
- map_url: Google Maps search link for opening a suggested place on a map

AVAILABLE TOOLS:
{tool_descriptions}

RESPONSE FORMAT:
Use exactly one of these formats.

If you need a tool:
Thought: <short reasoning>
Action: tool_name(argument)

If you have enough information:
Thought: <short final reasoning>
Final Answer: <clear Vietnamese answer>

STRICT RULES:
- Do not invent places from memory.
- Use rank_and_recommend_places when the user's location and need are clear.
- Use get_place_map_link if the user asks for a map, direction, coordinate, or link for a specific place.
- If a tool returns ERROR_MISSING_LOCATION, ask the user for a location.
- If a tool returns ERROR_UNSUPPORTED_LOCATION, explain the current data limitation.
- If a tool returns NO_RESULTS, explain that no matching place was found and suggest broadening radius/category.
- Call only one tool per step.
- Use only tool names listed in AVAILABLE TOOLS.
- Final Answer must include place name, category, distance, price level, reason, and map_url when places are available.
"""

    def run(self, user_input: str) -> str:
        candidate_input = user_input
        if self.pending_query:
            current_precheck = json.loads(extract_location_and_need(user_input))
            if current_precheck["location_status"] != "missing":
                candidate_input = f"{self.pending_query}\nUser provided location: {user_input}"
                logger.log_event("AGENT_V2_RESUME_PENDING_QUERY", {
                    "pending_query": self.pending_query,
                    "location_reply": user_input,
                    "combined_input": candidate_input,
                })

        precheck_raw = extract_location_and_need(candidate_input)
        precheck = json.loads(precheck_raw)

        logger.log_event("AGENT_V2_PRECHECK", {
            "input": candidate_input,
            "precheck": precheck,
        })

        if precheck["needs_clarification"]:
            self.pending_query = user_input
            logger.log_event("AGENT_V2_GUARDRAIL", {
                "reason": "missing_location",
                "input": user_input,
            })
            return (
                "Bạn đang ở khu vực nào? Vui lòng cung cấp vị trí cụ thể, "
                "ví dụ: VinUni, Vinhomes Ocean Park hoặc Gia Lâm. "
                "Sau đó tôi sẽ tìm địa điểm phù hợp gần bạn."
            )

        if precheck.get("unsupported_location"):
            self.pending_query = ""
            logger.log_event("AGENT_V2_GUARDRAIL", {
                "reason": "unsupported_location",
                "input": candidate_input,
                "location": precheck["location"],
            })
            return (
                f"Hiện dữ liệu của tôi chưa có cho khu vực {precheck['location']}. "
                "Hiện tôi chỉ hỗ trợ các địa điểm trong khu vực gần trường VinUni."
            )

        self.pending_query = ""
        enriched_input = (
            f"{candidate_input}\n\n"
            "Normalized context for tool use:\n"
            f"- location: {precheck['location']}\n"
            f"- category: {precheck['category']}\n"
            f"- radius_km: {precheck['radius_km']}\n"
            "Use this normalized context when calling tools."
        )

        logger.log_event("AGENT_V2_START_REACT", {
            "location": precheck["location"],
            "category": precheck["category"],
            "radius_km": precheck["radius_km"],
        })

        return self._agent.run(enriched_input)
