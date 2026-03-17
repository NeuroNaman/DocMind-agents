


from typing import Any, Dict

from app.agents.base import BaseAgent
from app.core.state import AgentState
from app.services.llm_service import get_llm_service


class LLMAnswerAgent(BaseAgent):
    """
    Generates answers using LLM based on retrieved context.
    If answer is not found in the document, routes to fallback agent.
    """

    def execute(self, state: AgentState) -> Dict[str, Any]:

        question = state.get("input", "")
        context = state.get("context", [])
        history = state.get("history", [])

        # ------------------------------------------------
        # No question
        # ------------------------------------------------
        if not question:
            self.logger.warning("No question provided")

            return {
                "answer": "No question was provided.",
                "source": "error",
                "next_agent": "executor_agent",
            }

        # ------------------------------------------------
        # No context → send to fallback
        # ------------------------------------------------
        if not context:

            self.logger.info(
                "No context available -> routing to fallback agent"
            )

            return {
                "next_agent": "fallback_agent"
            }

        try:

            llm_service = get_llm_service()

            self.logger.info(
                f"Generating answer with {len(context)} context chunks"
            )

            # ------------------------------------------------
            # Generate answer
            # ------------------------------------------------
            if history:
                answer = llm_service.generate_with_history(
                    question=question,
                    context=context,
                    history=history,
                )
            else:
                answer = llm_service.generate_answer(
                    question=question,
                    context=context,
                )

            # ------------------------------------------------
            # Detect if answer NOT in document
            # ------------------------------------------------
            answer_lower = answer.lower()

            negative_patterns = [
                "not contain",
                "not mentioned",
                "not present",
                "no information",
                "does not contain",
                "not found",
                "not provided in the context",
            ]

            if any(p in answer_lower for p in negative_patterns):

                self.logger.info(
                    "Answer not found in document -> routing to fallback agent"
                )

                return {
                    "context": [],
                    "next_agent": "fallback_agent"
                }

            # ------------------------------------------------
            # Valid RAG answer
            # ------------------------------------------------
            self.logger.info("Answer generated successfully")

            return {
                "answer": answer,
                "source": "rag",
                "next_agent": "executor_agent",
            }

        except Exception as e:

            self.logger.error(f"LLM generation failed: {e}")

            return {
                "answer": "Error generating response.",
                "source": "error",
                "next_agent": "executor_agent",
            }


# ------------------------------------------------
# LangGraph wrapper
# ------------------------------------------------
def llm_answer_agent(state: AgentState) -> Dict[str, Any]:
    """LangGraph wrapper"""
    agent = LLMAnswerAgent()
    return agent(state)