from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import WebSearchTool, IPythonInterpreter
from openai.types.shared import Reasoning
from virtual_assistant.tools.ScholarSearch import ScholarSearch

from config import get_default_model, is_openai_provider


def create_deep_research() -> Agent:
    return Agent(
        name="Local Market Research Agent",
        description=(
            "Researches local competitors, customer search intent, local SEO keywords, seasonal content "
            "angles, and content opportunities for small businesses. Always cites sources."
        ),
        instructions="./instructions.md",
        files_folder="./files",
        tools=[WebSearchTool(), ScholarSearch, IPythonInterpreter],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="high", summary="auto") if is_openai_provider() else None,
            response_include=["web_search_call.action.sources"] if is_openai_provider() else None,
        ),
        conversation_starters=[
            "Research local competitors for a [business type] in [city].",
            "Find local SEO keyword opportunities for a [business type] in [city].",
            "What seasonal content angles are coming up for a [business type]?",
            "What are customers in [city] searching for when they need [service]?",
        ],
    )
