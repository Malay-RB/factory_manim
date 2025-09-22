from pathlib import Path
import os 
import psycopg2
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()

class InputHandler(ABC):

    @abstractmethod
    def load(self, source):
        """Load raw data from source"""
        pass
    @staticmethod
    def validate_source(source: str | Path):
        """Utility method to validate input sources"""
        if not source:
            raise ValueError("Source cannot be empty")

class LocalFileInputHandler(InputHandler):
    """Reads any local file as text"""
    def load(self, config: dict) -> str:
        path = Path(config["path"]) / config["file"]
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        return path.read_text(encoding="utf-8")


class DatabaseInputHandler(InputHandler):
    def __init__(self):
        # Fetch connection info directly from environment variables
        self.db_config = {
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT"),
            "dbname": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
        }

    def load(self, config: dict):
        table_name = config["table"]

        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        cursor.close()
        conn.close()

        return [dict(zip(columns, row)) for row in rows]


class CloudInputHandler(InputHandler):
    """Placeholder for cloud input"""
    def load(self, cloud_path: str):
        # Future: implement cloud file fetching
        return "Simulated cloud file content"