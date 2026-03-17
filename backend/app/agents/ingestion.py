
"""
Ingestion Agent - Processes and stores documents.
Handles document loading, chunking, and vector store insertion.
"""

from typing import Any, Dict

from app.agents.base import BaseAgent
from app.core.state import AgentState
from app.exceptions import DocumentProcessingError
from app.services.vector_store import get_vector_store
from app.tools.document_loader import DocumentLoader
from app.tools.text_splitter import get_text_splitter


class IngestionAgent(BaseAgent):
    """
    Processes documents and adds them to the vector store.
    Supports PDF, DOCX, TXT, and URL content.
    """

    def execute(self, state: AgentState) -> Dict[str, Any]:

        file_content = state.get("file_content")
        file_type = state.get("file_type")
        metadata = state.get("metadata") or {}

        # ------------------------------------------------
        # Skip ingestion if already processed
        # ------------------------------------------------
        if metadata.get("ingested"):

            self.logger.info("Document already ingested - skipping ingestion")

            return {
                "next_agent": "planner_agent"
            }

        if not file_content or not file_type:

            self.logger.warning("No content to ingest, skipping to planner")

            return {
                "next_agent": "planner_agent"
            }

        try:

            # Load document
            self.logger.info(f"Loading {file_type} document: {file_content}")

            documents = DocumentLoader.load(file_content, file_type)

            if not documents:

                self.logger.warning("No documents loaded")

                return {
                    "next_agent": "planner_agent",
                    "chunks_added": 0
                }

            # Split into chunks
            splitter = get_text_splitter()

            chunks = splitter.split_documents(documents)

            self.logger.info(f"Created {len(chunks)} chunks from document")

            if chunks:

                vector_store = get_vector_store()

                # Clear vector store ONLY during upload
                try:

                    vector_store.clear()

                    self.logger.info(
                        "Cleared existing vector store for fresh upload"
                    )

                except Exception as e:

                    self.logger.warning(
                        f"Could not clear vector store: {e}"
                    )

                vector_store.add_documents(chunks)

                self.logger.info(
                    f"Added {len(chunks)} chunks to vector store"
                )

            return {
                "next_agent": "planner_agent",
                "chunks_added": len(chunks),
                "metadata": {
                    "source": file_content,
                    "type": file_type,
                    "chunks": len(chunks),
                    "ingested": True,
                },
            }

        except DocumentProcessingError as e:

            self.logger.error(f"Document processing failed: {e}")

            return {
                "error": str(e),
                "next_agent": "planner_agent",
                "chunks_added": 0,
            }

        except Exception as e:

            self.logger.error(f"Unexpected error during ingestion: {e}")

            return {
                "error": f"Ingestion failed: {str(e)}",
                "next_agent": "planner_agent",
                "chunks_added": 0,
            }


# LangGraph wrapper
def ingestion_agent(state: AgentState) -> Dict[str, Any]:

    agent = IngestionAgent()

    return agent(state)