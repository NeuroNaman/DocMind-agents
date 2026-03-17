"""
Tests for workflow graph.
"""

from unittest.mock import MagicMock, patch

from app.workflow.graph import (
    create_workflow,
    get_workflow,
    process_query,
    reset_workflow,
)


class TestCreateWorkflow:
    """Tests for create_workflow function."""

    @patch("app.workflow.graph.StateGraph")
    def test_create_workflow_returns_compiled_graph(self, mock_state_graph):
        """Test create_workflow returns compiled graph."""
        mock_graph = MagicMock()
        mock_compiled = MagicMock()
        mock_graph.compile.return_value = mock_compiled
        mock_state_graph.return_value = mock_graph

        result = create_workflow()

        assert result is mock_compiled
        mock_graph.compile.assert_called_once()

    @patch("app.workflow.graph.StateGraph")
    def test_create_workflow_adds_all_nodes(self, mock_state_graph):
        """Test create_workflow adds all agent nodes."""
        mock_graph = MagicMock()
        mock_state_graph.return_value = mock_graph

        create_workflow()

        # Check that all nodes are added
        node_calls = mock_graph.add_node.call_args_list
        node_names = [call[0][0] for call in node_calls]

        assert "tool_router_agent" in node_names
        assert "ingestion_agent" in node_names
        assert "planner_agent" in node_names
        assert "retriever_agent" in node_names
        assert "llm_answer_agent" in node_names
        assert "fallback_agent" in node_names
        assert "executor_agent" in node_names

    @patch("app.workflow.graph.StateGraph")
    def test_create_workflow_sets_entry_point(self, mock_state_graph):
        """Test create_workflow sets entry point."""
        mock_graph = MagicMock()
        mock_state_graph.return_value = mock_graph

        create_workflow()

        mock_graph.set_entry_point.assert_called_once_with("tool_router_agent")


class TestGetWorkflow:
    """Tests for get_workflow function."""

    @patch("app.workflow.graph.create_workflow")
    def test_get_workflow_creates_if_none(self, mock_create):
        """Test get_workflow creates workflow if none exists."""
        import app.workflow.graph as graph

        graph._workflow = None

        mock_workflow = MagicMock()
        mock_create.return_value = mock_workflow

        result = get_workflow()

        assert result is mock_workflow
        mock_create.assert_called_once()

    @patch("app.workflow.graph.create_workflow")
    def test_get_workflow_returns_existing(self, mock_create):
        """Test get_workflow returns existing workflow."""
        import app.workflow.graph as graph

        mock_workflow = MagicMock()
        graph._workflow = mock_workflow

        result = get_workflow()

        assert result is mock_workflow
        mock_create.assert_not_called()


class TestResetWorkflow:
    """Tests for reset_workflow function."""

    def test_reset_workflow_clears_global(self):
        """Test reset_workflow clears global workflow."""
        import app.workflow.graph as graph

        graph._workflow = MagicMock()

        reset_workflow()

        assert graph._workflow is None


class TestProcessQuery:
    """Tests for process_query function."""

    @patch("app.workflow.graph.get_workflow")
    def test_process_query_success(self, mock_get_workflow):
        """Test process_query with successful execution."""
        mock_workflow = MagicMock()
        mock_workflow.invoke.return_value = {
            "answer": "Test answer",
            "source": "rag",
        }
        mock_get_workflow.return_value = mock_workflow

        answer, source = process_query("What is Python?")

        assert answer == "Test answer"
        assert source == "rag"

    @patch("app.workflow.graph.get_workflow")
    def test_process_query_with_file(self, mock_get_workflow):
        """Test process_query with file parameter."""
        mock_workflow = MagicMock()
        mock_workflow.invoke.return_value = {
            "answer": "From document",
            "source": "rag",
        }
        mock_get_workflow.return_value = mock_workflow

        answer, source = process_query(
            "Question?", file_path="test.pdf", file_type="pdf"
        )

        call_args = mock_workflow.invoke.call_args[0][0]
        assert call_args["file_content"] == "test.pdf"
        assert call_args["file_type"] == "pdf"

    @patch("app.workflow.graph.get_workflow")
    def test_process_query_with_error_in_result(self, mock_get_workflow):
        """Test process_query with error in result."""
        mock_workflow = MagicMock()
        mock_workflow.invoke.return_value = {
            "answer": "Partial answer",
            "source": "rag",
            "error": "Some warning",
        }
        mock_get_workflow.return_value = mock_workflow

        answer, source = process_query("Test")

        assert answer == "Partial answer"

    @patch("app.workflow.graph.get_workflow")
    def test_process_query_exception(self, mock_get_workflow):
        """Test process_query with exception."""
        mock_workflow = MagicMock()
        mock_workflow.invoke.side_effect = Exception("Workflow failed")
        mock_get_workflow.return_value = mock_workflow

        answer, source = process_query("Test")

        assert "error" in answer.lower()
        assert source == "error"

    @patch("app.workflow.graph.get_workflow")
    def test_process_query_no_answer(self, mock_get_workflow):
        """Test process_query with no answer in result."""
        mock_workflow = MagicMock()
        mock_workflow.invoke.return_value = {}
        mock_get_workflow.return_value = mock_workflow

        answer, source = process_query("Test")

        assert answer == "No answer generated"
        assert source == "unknown"
