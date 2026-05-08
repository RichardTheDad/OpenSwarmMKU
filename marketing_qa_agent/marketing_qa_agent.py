from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import WebSearchTool, LoadFileAttachment, PersistentShellTool
from openai.types.shared import Reasoning
from shared_tools import CopyFile, ListDirectory, ReadFile, WriteFile

from config import get_default_model, is_openai_provider


def create_marketing_qa_agent() -> Agent:
    return Agent(
        name="Marketing QA Agent",
        description=(
            "Quality assurance reviewer that checks all marketing deliverables for fake claims, "
            "generic AI language, missing CTAs, brand fit, and local relevance before client delivery."
        ),
        instructions="./instructions.md",
        tools=[
            WebSearchTool(),
            LoadFileAttachment,
            PersistentShellTool,
            CopyFile,
            ReadFile,
            WriteFile,
            ListDirectory,
        ],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium", summary="auto") if is_openai_provider() else None,
        ),
        conversation_starters=[
            "Review all content in clients/[client-name]/outputs/ for the monthly package.",
            "QA check this Facebook post draft before it goes to the client.",
            "Run a full QA review on the content package for [client name].",
            "Check this ad copy for fake claims and brand fit.",
        ],
    )


if __name__ == "__main__":
    from agency_swarm import Agency
    Agency(create_marketing_qa_agent()).terminal_demo()
