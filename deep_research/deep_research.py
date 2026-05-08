from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import IPythonInterpreter
from openai.types.shared import Reasoning

from config import get_default_model, is_openai_provider
from shared_tools import ListDirectory, ReadFile, WriteFile

# OpenAI Responses API web search — requires OPENAI_API_KEY only.
# SEARCH_API_KEY is NOT needed for this tool.
# See deep_research/tools/OpenAIWebSearchTool.py for full configuration notes.
from deep_research.tools.OpenAIWebSearchTool import create_openai_web_search_tool


def create_deep_research() -> Agent:
    return Agent(
        name="Local Market Research Agent",
        description=(
            "Researches local competitors, customer search intent, local SEO keywords, seasonal content "
            "angles, and content opportunities for small businesses. Always cites sources. "
            "Uses OpenAI Responses API web search — no SEARCH_API_KEY required."
        ),
        instructions="./instructions.md",
        files_folder="./files",
        tools=[
            create_openai_web_search_tool(),  # OpenAI Responses API web search
            IPythonInterpreter,               # For data processing if needed
            ReadFile,
            WriteFile,
            ListDirectory,
        ],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="high", summary="auto") if is_openai_provider() else None,
            # Include source URLs with every web search result
            response_include=["web_search_call.action.sources"] if is_openai_provider() else None,
        ),
        conversation_starters=[
            "Research local competitors for a [business type] in [city].",
            "Find local SEO keyword opportunities for a [business type] in [city].",
            "What seasonal content angles are coming up for a [business type]?",
            "What are customers in [city] searching for when they need [service]?",
        ],
    )
