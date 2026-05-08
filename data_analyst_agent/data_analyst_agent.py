import os
from agency_swarm import Agent, ModelSettings
from openai.types.shared.reasoning import Reasoning
from agency_swarm.tools import (
    WebSearchTool,
    PersistentShellTool,
    IPythonInterpreter,
    LoadFileAttachment,
)
from shared_tools import CopyFile, ExecuteTool, FindTools, ManageConnections, SearchTools

from config import get_default_model, is_openai_provider

current_dir = os.path.dirname(os.path.abspath(__file__))
instructions_path = os.path.join(current_dir, "instructions.md")

def create_data_analyst() -> Agent:
    return Agent(
        name="Marketing Report Agent",
        description=(
            "Turns website traffic, social media, Google Business Profile, and ad performance data into "
            "clear monthly reports for local small businesses. Never fakes or estimates numbers. "
            "Explicitly flags missing data."
        ),
        instructions=instructions_path,
        tools_folder=os.path.join(current_dir, "tools"),
        model=get_default_model(),
        tools=[
            WebSearchTool(),
            PersistentShellTool,
            IPythonInterpreter,
            LoadFileAttachment,
            CopyFile,
            ExecuteTool,
            FindTools,
            ManageConnections,
            SearchTools,
        ],
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium", summary="auto") if is_openai_provider() else None,
            truncation="auto",
            response_include=["web_search_call.action.sources"] if is_openai_provider() else None,
        ),
        conversation_starters=[
            "Generate a monthly marketing report for [client name] using this data.",
            "Analyze this month's Google Business Profile stats for [client name].",
            "Create a performance summary chart from this social media export.",
            "Build a monthly report from these GA4 and Meta data exports.",
        ],
    )
