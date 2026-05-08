from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import LoadFileAttachment
from openai.types.shared.reasoning import Reasoning
from shared_tools import CopyFile

from config import get_default_model, is_openai_provider


def create_video_generation_agent() -> Agent:
    return Agent(
        name="Short-Form Video Agent",
        description=(
            "Creates reel scripts, short ad scripts, shot lists, voiceover scripts, and text overlay plans "
            "for local small business marketing. Prioritizes content filmable with a phone. "
            "Can also generate AI video clips when requested."
        ),
        instructions="instructions.md",
        tools_folder="./tools",
        tools=[LoadFileAttachment, CopyFile],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(summary="auto", effort="medium") if is_openai_provider() else None,
            truncation="auto",
        ),
        conversation_starters=[
            "Write a 30-second reel script for [client name] about [topic].",
            "Create a shot list for a behind-the-scenes video for [client name].",
            "Write a short ad script for [client name]'s Facebook video ad.",
            "Plan a 3-video reel series for [client name] for this month.",
        ],
    )
