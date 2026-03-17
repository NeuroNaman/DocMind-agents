"""
Wikipedia service for fallback searches.
Uses LangChain Wikipedia integration.
"""

from typing import Optional

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from app.utils.logger import get_logger

logger = get_logger("wikipedia_service")


class WikipediaService:
    """
    Service for Wikipedia searches.
    Used when document context does not contain the answer.
    """

    _instance: Optional["WikipediaService"] = None
    _wikipedia = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._wikipedia is None:
            self._initialize()

    def _initialize(self):
        """Initialize Wikipedia search tool."""
        try:

            api_wrapper = WikipediaAPIWrapper(
                top_k_results=3,
                doc_content_chars_max=2000,
            )

            self._wikipedia = WikipediaQueryRun(api_wrapper=api_wrapper)

            logger.info("Wikipedia service initialized")

        except Exception as e:

            logger.error(f"Failed to initialize Wikipedia service: {e}")
            raise

    # ------------------------------------------------
    # Search Wikipedia
    # ------------------------------------------------
    def search(self, query: str) -> str:

        try:

            if not query:
                return "No query provided."

            result = self._wikipedia.run(query)

            if not result:
                return "No relevant information found on Wikipedia."

            logger.info(
                f"Wikipedia search successful for query: {query[:50]}"
            )

            return result.strip()

        except Exception as e:

            logger.error(f"Wikipedia search failed: {e}")

            return "Failed to retrieve information from Wikipedia."

    # ------------------------------------------------
    # Get topic summary
    # ------------------------------------------------
    def get_summary(self, topic: str) -> str:

        return self.search(topic)


# ------------------------------------------------
# Global singleton instance
# ------------------------------------------------
_wikipedia_service: Optional[WikipediaService] = None


def get_wikipedia_service() -> WikipediaService:

    global _wikipedia_service

    if _wikipedia_service is None:
        _wikipedia_service = WikipediaService()

    return _wikipedia_service