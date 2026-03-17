"""
Edge routing functions for the workflow.
Defines conditional routing logic between agents.
"""

from typing import Literal

from app.core.state import AgentState


def route_after_planner(
    state: AgentState,
) -> Literal["retriever_agent", "fallback_agent"]:
    """
    Route after planner based on next_agent decision.

    Args:
        state: Current agent state

    Returns:
        Next agent name
    """
    next_agent = state.get("next_agent", "fallback_agent")

    if next_agent == "retriever_agent":
        return "retriever_agent"
    else:
        return "fallback_agent"


def route_after_tool_router(
    state: AgentState,
) -> Literal["ingestion_agent", "planner_agent"]:
    """
    Route after tool router based on content availability.

    Args:
        state: Current agent state

    Returns:
        Next agent name
    """
    next_agent = state.get("next_agent", "planner_agent")

    if next_agent == "ingestion_agent":
        return "ingestion_agent"
    else:
        return "planner_agent"


def should_use_rag(state: AgentState) -> bool:
    """
    Determine if RAG should be used.

    Args:
        state: Current agent state

    Returns:
        True if RAG should be used
    """
    context = state.get("context", [])
    return len(context) > 0


def has_error(state: AgentState) -> bool:
    """
    Check if an error occurred.

    Args:
        state: Current agent state

    Returns:
        True if error exists
    """
    return bool(state.get("error"))
