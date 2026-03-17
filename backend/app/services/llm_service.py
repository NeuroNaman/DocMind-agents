"""
LLM service for language model operations.
Provides abstraction over LLM providers.
"""

import os
from typing import Dict, List, Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from app.config import get_config
from app.exceptions import LLMError
from app.utils.logger import get_logger

logger = get_logger("llm_service")


class LLMService:
    """
    Service for LLM operations.
    Supports Groq LLM provider.
    """

    _instance: Optional["LLMService"] = None
    _llm = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._llm is None:
            self._initialize()

    # ------------------------------------------------
    # Initialize LLM
    # ------------------------------------------------
    def _initialize(self):

        config = get_config()

        try:

            api_key = config.GROQ_API_KEY or os.getenv("GROQ_API_KEY")

            if not api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")

            self._llm = ChatGroq(
                model=config.LLM_MODEL,
                temperature=config.LLM_TEMPERATURE,
                groq_api_key=api_key,
            )

            logger.info(f"LLM initialized successfully: {config.LLM_MODEL}")

        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise LLMError(f"LLM initialization failed: {str(e)}")

    @property
    def llm(self):
        """Return LLM instance"""
        return self._llm

    # ------------------------------------------------
    # Context-based generation (RAG)
    # ------------------------------------------------
    def generate_answer(
        self,
        question: str,
        context: List[str],
        system_prompt: Optional[str] = None,
    ) -> str:

        if system_prompt is None:
            system_prompt = (
                "You are a helpful assistant that answers questions using ONLY the provided context.\n"
                "If the answer is not present in the context, respond exactly with:\n"
                "'The context does not contain the answer.'\n"
                "Do not hallucinate."
            )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "Context:\n{context}\n\nQuestion: {question}"),
            ]
        )

        chain = prompt | self._llm | StrOutputParser()

        try:

            context_str = "\n\n".join(context) if context else "No context provided"

            answer = chain.invoke(
                {
                    "context": context_str,
                    "question": question,
                }
            )

            logger.info("Generated answer successfully")

            return answer.strip()

        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise LLMError(f"Failed to generate answer: {str(e)}")

    # ------------------------------------------------
    # Simple generation
    # ------------------------------------------------
    def generate_simple(self, prompt: str) -> str:

        try:

            response = self._llm.invoke(prompt)

            return response.content.strip()

        except Exception as e:
            logger.error(f"Simple generation failed: {e}")
            raise LLMError(f"Generation failed: {str(e)}")

    # ------------------------------------------------
    # Generation with chat history
    # ------------------------------------------------
    def generate_with_history(
        self,
        question: str,
        context: List[str],
        history: List[Dict[str, str]],
    ) -> str:

        messages = [
            (
                "system",
                "You are a helpful assistant that answers using the provided context.",
            )
        ]

        for msg in history[-5:]:
            role = "human" if msg.get("role") == "user" else "assistant"
            messages.append((role, msg.get("content", "")))

        context_str = "\n\n".join(context) if context else "No additional context"

        messages.append(
            (
                "human",
                f"Context:\n{context_str}\n\nQuestion: {question}",
            )
        )

        prompt = ChatPromptTemplate.from_messages(messages)

        chain = prompt | self._llm | StrOutputParser()

        try:

            answer = chain.invoke({})

            return answer.strip()

        except Exception as e:
            logger.error(f"Generation with history failed: {e}")
            raise LLMError(f"Failed to generate answer: {str(e)}")


# ------------------------------------------------
# Global singleton instance
# ------------------------------------------------
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:

    global _llm_service

    if _llm_service is None:
        _llm_service = LLMService()

    return _llm_service