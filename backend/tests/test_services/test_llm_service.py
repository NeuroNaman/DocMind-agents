"""
Tests for LLM service.
"""

from unittest.mock import MagicMock, patch

import pytest

from app.exceptions import LLMError
from app.services.llm_service import LLMService, get_llm_service


class TestLLMService:
    """Tests for LLMService class."""

    @patch("app.services.llm_service.ChatGroq")
    def test_singleton_pattern(self, mock_groq):
        """Test singleton pattern returns same instance."""
        LLMService._instance = None
        LLMService._llm = None

        service1 = LLMService()
        service2 = LLMService()

        assert service1 is service2

    @patch("app.services.llm_service.ChatGroq")
    def test_llm_property(self, mock_groq_class):
        """Test llm property returns LLM instance."""
        LLMService._instance = None
        LLMService._llm = None

        mock_llm = MagicMock()
        mock_groq_class.return_value = mock_llm

        service = LLMService()
        result = service.llm

        assert result is mock_llm

    @patch("app.services.llm_service.StrOutputParser")
    @patch("app.services.llm_service.ChatPromptTemplate")
    @patch("app.services.llm_service.ChatGroq")
    def test_generate_answer_success(self, mock_groq, mock_prompt, mock_parser):
        """Test generate_answer with context."""
        LLMService._instance = None
        LLMService._llm = None

        mock_llm = MagicMock()
        mock_groq.return_value = mock_llm

        # Create mock chain
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Generated answer"
        mock_prompt.from_messages.return_value.__or__.return_value.__or__.return_value = (
            mock_chain
        )

        service = LLMService()
        result = service.generate_answer(
            question="What is Python?", context=["Python is a programming language."]
        )

        assert result == "Generated answer"

    @patch("app.services.llm_service.StrOutputParser")
    @patch("app.services.llm_service.ChatPromptTemplate")
    @patch("app.services.llm_service.ChatGroq")
    def test_generate_answer_exception(self, mock_groq, mock_prompt, mock_parser):
        """Test generate_answer handles exception."""
        LLMService._instance = None
        LLMService._llm = None

        mock_llm = MagicMock()
        mock_groq.return_value = mock_llm

        # Create mock chain that raises
        mock_chain = MagicMock()
        mock_chain.invoke.side_effect = Exception("LLM error")
        mock_prompt.from_messages.return_value.__or__.return_value.__or__.return_value = (
            mock_chain
        )

        service = LLMService()

        with pytest.raises(LLMError):
            service.generate_answer(question="Test?", context=["Context"])

    @patch("app.services.llm_service.ChatGroq")
    def test_generate_simple(self, mock_groq_class):
        """Test generate_simple method."""
        LLMService._instance = None
        LLMService._llm = None

        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Simple response"
        mock_llm.invoke.return_value = mock_response
        mock_groq_class.return_value = mock_llm

        service = LLMService()
        result = service.generate_simple("Test prompt")

        assert result == "Simple response"

    @patch("app.services.llm_service.ChatGroq")
    def test_generate_simple_exception(self, mock_groq_class):
        """Test generate_simple handles exception."""
        LLMService._instance = None
        LLMService._llm = None

        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = Exception("API error")
        mock_groq_class.return_value = mock_llm

        service = LLMService()

        with pytest.raises(LLMError):
            service.generate_simple("Test prompt")

    @patch("app.services.llm_service.StrOutputParser")
    @patch("app.services.llm_service.ChatPromptTemplate")
    @patch("app.services.llm_service.ChatGroq")
    def test_generate_with_history(self, mock_groq, mock_prompt, mock_parser):
        """Test generate_with_history method."""
        LLMService._instance = None
        LLMService._llm = None

        mock_llm = MagicMock()
        mock_groq.return_value = mock_llm

        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Answer with history"
        mock_prompt.from_messages.return_value.__or__.return_value.__or__.return_value = (
            mock_chain
        )

        service = LLMService()
        result = service.generate_with_history(
            question="Follow up?",
            context=["Some context"],
            history=[
                {"role": "user", "content": "Previous question"},
                {"role": "assistant", "content": "Previous answer"},
            ],
        )

        assert result == "Answer with history"

    @patch("app.services.llm_service.StrOutputParser")
    @patch("app.services.llm_service.ChatPromptTemplate")
    @patch("app.services.llm_service.ChatGroq")
    def test_generate_with_history_exception(self, mock_groq, mock_prompt, mock_parser):
        """Test generate_with_history handles exception."""
        LLMService._instance = None
        LLMService._llm = None

        mock_llm = MagicMock()
        mock_groq.return_value = mock_llm

        mock_chain = MagicMock()
        mock_chain.invoke.side_effect = Exception("History error")
        mock_prompt.from_messages.return_value.__or__.return_value.__or__.return_value = (
            mock_chain
        )

        service = LLMService()

        with pytest.raises(LLMError):
            service.generate_with_history(
                question="Test?", context=["Context"], history=[]
            )

    @patch("app.services.llm_service.ChatGroq")
    def test_initialization_failure(self, mock_groq_class):
        """Test initialization failure raises LLMError."""
        LLMService._instance = None
        LLMService._llm = None

        mock_groq_class.side_effect = Exception("API key invalid")

        with pytest.raises(LLMError):
            LLMService()


class TestGetLLMService:
    """Tests for get_llm_service function."""

    @patch("app.services.llm_service.ChatGroq")
    def test_returns_service_instance(self, mock_groq):
        """Test that function returns LLMService instance."""
        import app.services.llm_service as llm

        llm._llm_service = None
        LLMService._instance = None
        LLMService._llm = None

        result = get_llm_service()

        assert isinstance(result, LLMService)

    @patch("app.services.llm_service.ChatGroq")
    def test_singleton_global(self, mock_groq):
        """Test global singleton pattern."""
        import app.services.llm_service as llm

        llm._llm_service = None
        LLMService._instance = None
        LLMService._llm = None

        service1 = get_llm_service()
        service2 = get_llm_service()

        assert service1 is service2
