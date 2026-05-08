from agency_swarm import Agent, ModelSettings
from openai.types.shared import Reasoning
from dotenv import load_dotenv

from config import get_default_model, is_openai_provider

load_dotenv()


def create_orchestrator() -> Agent:
    return Agent(
        name="Marketing Director",
        description=(
            "Primary coordinator for the Small Business Marketing Swarm. Routes client marketing requests "
            "to specialist agents, assembles deliverable packages, and ensures nothing reaches a client "
            "without human review."
        ),
        instructions="./instructions.md",
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium", summary="auto") if is_openai_provider() else None,
        ),
        conversation_starters=[
            "Create a monthly content package for [client name].",
            "Write a Facebook post and GBP update for [client name] this week.",
            "Run a full local market research brief for a new client.",
            "Assemble the monthly marketing report for [client name] using this month's data.",
        ],
    )


if __name__ == "__main__":
    from agency_swarm import Agency
    Agency(create_orchestrator()).terminal_demo()