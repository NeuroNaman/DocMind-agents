"""
Agents module for AutoDocThinker.
Contains all agent implementations for the LangGraph workflow.
"""

from app.agents.base import BaseAgent
from app.agents.executor import ExecutorAgent
from app.agents.fallback import FallbackAgent
from app.agents.ingestion import IngestionAgent
from app.agents.llm_answer import LLMAnswerAgent
from app.agents.planner import PlannerAgent
from app.agents.retriever import RetrieverAgent
from app.agents.tool_router import ToolRouterAgent

__all__ = [
    "BaseAgent",
    "ToolRouterAgent",
    "IngestionAgent",
    "PlannerAgent",
    "RetrieverAgent",
    "LLMAnswerAgent",
    "FallbackAgent",
    "ExecutorAgent",
]

# Agent registry for dynamic access
AGENT_REGISTRY = {
    "tool_router": ToolRouterAgent,
    "ingestion": IngestionAgent,
    "planner": PlannerAgent,
    "retriever": RetrieverAgent,
    "llm_answer": LLMAnswerAgent,
    "fallback": FallbackAgent,
    "executor": ExecutorAgent,
}


def get_agent(name: str) -> BaseAgent:
    """Get an agent instance by name."""
    if name not in AGENT_REGISTRY:
        raise ValueError(f"Unknown agent: {name}")
    return AGENT_REGISTRY[name]()
