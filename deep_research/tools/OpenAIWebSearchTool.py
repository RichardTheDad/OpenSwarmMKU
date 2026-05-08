# OpenAI Responses API Web Search Tool
#
# HOW IT WORKS:
#   This tool uses OpenAI's hosted web search via the Responses API.
#   The model calls web_search natively — no external search service needed.
#
# WHAT IT NEEDS:
#   - OPENAI_API_KEY (already in .env)
#   - An OpenAI model that supports the Responses API (gpt-4o, gpt-4o-mini, gpt-5.x)
#
# WHAT IT DOES NOT NEED:
#   - SEARCH_API_KEY is NOT required for this tool
#   - No SearchAPI.io account needed
#
# SEARCH CONTEXT SIZE:
#   "high" = more web content fetched per search = better for competitor research
#   and local SEO keyword research where depth matters.
#   Costs slightly more tokens per search — stay within budget rules in instructions.md.
#
# SOURCE CITATIONS:
#   The agent is configured with response_include=["web_search_call.action.sources"]
#   so source URLs are returned with every search result.

import os
from agency_swarm.tools import WebSearchTool


def create_openai_web_search_tool() -> WebSearchTool:
    """
    Returns a WebSearchTool configured for local market research.

    Uses OpenAI Responses API hosted web search (web_search_preview).
    Requires OPENAI_API_KEY. SEARCH_API_KEY is not used.

    search_context_size="high" gives more thorough results for competitor
    and keyword research tasks. Use the search budget rules in instructions.md
    to avoid unnecessary API calls.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. OpenAI web search requires this key.\n"
            "Add it to your .env file: OPENAI_API_KEY=sk-..."
        )

    return WebSearchTool(search_context_size="high")
