import argparse
import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, ".")

from src.agent.chatbot import Chatbot


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value or value.startswith("your_"):
        raise ValueError(f"Missing environment variable: {name}")
    return value


def build_provider():
    provider_name = os.getenv("DEFAULT_PROVIDER", "opencode").lower()

    if provider_name == "opencode":
        from src.core.openai_compatible_provider import OpenAICompatibleProvider

        return OpenAICompatibleProvider(
            provider_name="opencode",
            model_name=os.getenv("OPENCODE_MODEL", os.getenv("DEFAULT_MODEL", "deepseek-v4-flash")),
            api_key=_require_env("OPENCODE_API_KEY"),
            base_url=os.getenv("OPENCODE_BASE_URL", "https://opencode.ai/zen/go/v1"),
        )

    if provider_name == "mimo":
        from src.core.openai_compatible_provider import OpenAICompatibleProvider

        return OpenAICompatibleProvider(
            provider_name="mimo",
            model_name=os.getenv("MIMO_MODEL", os.getenv("DEFAULT_MODEL", "mimo-v2.5-pro")),
            api_key=_require_env("MIMO_API_KEY"),
            base_url=os.getenv("MIMO_BASE_URL", "https://token-plan-sgp.xiaomimimo.com/v1"),
        )

    if provider_name == "openai":
        from src.core.openai_provider import OpenAIProvider

        return OpenAIProvider(
            model_name=os.getenv("OPENAI_MODEL", os.getenv("DEFAULT_MODEL", "gpt-4o")),
            api_key=_require_env("OPENAI_API_KEY"),
        )

    if provider_name in ("google", "gemini"):
        from src.core.gemini_provider import GeminiProvider

        return GeminiProvider(
            model_name=os.getenv("GEMINI_MODEL", os.getenv("DEFAULT_MODEL", "gemini-1.5-flash")),
            api_key=_require_env("GEMINI_API_KEY"),
        )

    raise ValueError(
        f"Unknown DEFAULT_PROVIDER='{provider_name}'. "
        "Use one of: opencode, mimo, openai, google."
    )


def run_chatbot_interactive():
    llm = build_provider()
    chatbot = Chatbot(llm=llm)

    print("=" * 64)
    print(f"Chatbot Baseline | provider model: {llm.model_name}")
    print("Type your message. Use 'exit' to quit.")
    print("=" * 64)

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ("exit", "quit", "q"):
                print("Goodbye.")
                break
            if not user_input:
                continue

            answer = chatbot.chat(user_input)
            print(f"\nChatbot: {answer}\n")
        except KeyboardInterrupt:
            print("\nGoodbye.")
            break


def run_agent_interactive():
    from src.agent.agent import ReActAgent
    from src.tools.nearby_tools import get_nearby_tools

    llm = build_provider()
    tools = get_nearby_tools()
    agent = ReActAgent(llm=llm, tools=tools, max_steps=5)

    print("=" * 64)
    print(f"ReAct Agent v1 | provider model: {llm.model_name}")
    print(f"Tools: {', '.join(tool['name'] for tool in tools)}")
    print("Type your nearby-place question. Use 'exit' to quit.")
    print("=" * 64)

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ("exit", "quit", "q"):
                print("Goodbye.")
                break
            if not user_input:
                continue

            answer = agent.run(user_input)
            print(f"\nAgent: {answer}\n")
        except KeyboardInterrupt:
            print("\nGoodbye.")
            break


def run_agent_v2_interactive():
    from src.agent.nearby_agent_v2 import NearbyAgentV2

    llm = build_provider()
    agent = NearbyAgentV2(llm=llm, max_steps=5)

    print("=" * 64)
    print(f"ReAct Agent v2 | provider model: {llm.model_name}")
    print("Improvements: missing-location guardrail + normalized context")
    print("Type your nearby-place question. Use 'exit' to quit.")
    print("=" * 64)

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ("exit", "quit", "q"):
                print("Goodbye.")
                break
            if not user_input:
                continue

            answer = agent.run(user_input)
            print(f"\nAgent v2: {answer}\n")
        except KeyboardInterrupt:
            print("\nGoodbye.")
            break


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Lab 3 runner")
    parser.add_argument(
        "--mode",
        choices=["chatbot", "agent", "agent-v2"],
        default="chatbot",
        help="Run mode: chatbot | agent | agent-v2",
    )
    args = parser.parse_args()

    if args.mode == "chatbot":
        run_chatbot_interactive()
    elif args.mode == "agent":
        run_agent_interactive()
    elif args.mode == "agent-v2":
        run_agent_v2_interactive()


if __name__ == "__main__":
    main()
