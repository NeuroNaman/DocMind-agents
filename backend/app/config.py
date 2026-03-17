
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BaseConfig:
    """Base configuration with common settings."""

    # ------------------------------------------------
    # Application Settings
    # ------------------------------------------------
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "autodocthinker-secret-key-change-in-production"
    )
    DEBUG = False
    TESTING = False

    # ------------------------------------------------
    # File Upload Settings
    # ------------------------------------------------
    UPLOAD_FOLDER = "uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit
    ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

    # ------------------------------------------------
    # Vector Database
    # ------------------------------------------------
    VECTOR_DB_PATH = "vector_db/chroma_collection"

    # ------------------------------------------------
    # Embedding Model
    # ------------------------------------------------
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    # ------------------------------------------------
    # LLM Settings
    # ------------------------------------------------
    LLM_MODEL = "llama-3.3-70b-versatile"
    LLM_TEMPERATURE = 0.1

    # ------------------------------------------------
    # API Keys (optional)
    # ------------------------------------------------
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    HUGGINGFACEHUB_API_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")

    # ------------------------------------------------
    # Text Chunking (Important for RAG)
    # Smaller chunks work better for resumes and short documents
    # ------------------------------------------------
    CHUNK_SIZE = 400
    CHUNK_OVERLAP = 80

    # ------------------------------------------------
    # Retrieval Settings
    # Retrieve more chunks so LLM sees full context
    # ------------------------------------------------
    RETRIEVAL_K = 6

    # ------------------------------------------------
    # Logging
    # ------------------------------------------------
    LOG_FILE = "logs/app.log"
    LOG_LEVEL = "INFO"


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    ENV = "development"
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(BaseConfig):
    """Production configuration."""

    ENV = "production"
    DEBUG = False
    LOG_LEVEL = "WARNING"


class TestingConfig(BaseConfig):
    """Testing configuration."""

    ENV = "testing"
    TESTING = True
    DEBUG = True
    VECTOR_DB_PATH = "vector_db/test_collection"
    LOG_LEVEL = "DEBUG"


# ------------------------------------------------
# Configuration Mapping
# ------------------------------------------------
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}


def get_config():
    """Return configuration based on APP_ENV."""
    env = os.environ.get("APP_ENV", "development")
    return config.get(env, config["default"])



