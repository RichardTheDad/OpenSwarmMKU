from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import LoadFileAttachment
from openai.types.shared.reasoning import Reasoning
from shared_tools import CopyFile, ListDirectory, ReadFile, WriteFile

from config import get_default_model, is_openai_provider


def create_image_generation_agent() -> Agent:
    return Agent(
        name="Creative Asset Agent",
        description=(
            "Creates graphic concepts, image-generation prompts, promo graphic ideas, and ad creative "
            "concepts for local small business marketing. Generates actual images when needed. "
            "Always follows the client brand guide and avoids misleading or fake visuals."
        ),
        instructions="instructions.md",
        tools_folder="./tools",
        tools=[LoadFileAttachment, CopyFile, ReadFile, WriteFile, ListDirectory],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(summary="auto", effort="medium") if is_openai_provider() else None,
            truncation="auto",
        ),
        conversation_starters=[
            "Create graphic concepts for [client name]'s monthly social media posts.",
            "Generate an ad creative for [client name]'s [service] campaign.",
            "Write image-generation prompts for [client name]'s seasonal promo.",
            "Create a promo graphic concept for [client name] using their brand guide.",
        ],
    )


if __name__ == "__main__":
    from agency_swarm import Agency
    Agency(create_image_generation_agent()).terminal_demo()
