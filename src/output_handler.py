from pathlib import Path
import json
import os
import psycopg2
from abc import ABC, abstractmethod


class OutputHandler(ABC):
    """Abstract base class for output handlers"""

    @abstractmethod
    def save(self, data, destination):
        """Save data to the destination"""
        pass

    @staticmethod
    def validate_data(data):
        """Basic validation for empty data"""
        if data is None:
            raise ValueError("Data cannot be None")


class LocalOutputHandler(OutputHandler):
    """Saves data to local filesystem"""

    def save(self, data, output_config: dict):
        """
        output_config example:
        {
            "path": "output",
            "file": "result.json"
        }
        """
        # Validate data
        self.validate_data(data)

        # Combine path + file
        path = Path(output_config["path"]) / output_config["file"]
        path.parent.mkdir(parents=True, exist_ok=True)

        # Save JSON if dict/list, else save plain text
        if isinstance(data, (dict, list)):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(str(data))

        return path


class DatabaseOutputHandler(OutputHandler):
    """Saves data into a Postgres database"""

    def __connect(self):
        """Private helper for DB connection"""
        return psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

    def save(self, data, table_name: str):
        self.validate_data(data)
        conn = self.__connect()
        cursor = conn.cursor()

        if isinstance(data, dict):
            data = [data]  # wrap dict into list for consistency

        columns = data[0].keys()
        col_defs = ", ".join([f"{col} TEXT" for col in columns])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({col_defs})")

        for row in data:
            placeholders = ", ".join(["%s"] * len(row))
            cursor.execute(
                f"INSERT INTO {table_name} ({', '.join(row.keys())}) VALUES ({placeholders})",
                tuple(row.values()),
            )

        conn.commit()
        cursor.close()
        conn.close()

        return f"Saved {len(data)} records to Postgres table {table_name}"


class CloudOutputHandler(OutputHandler):
    """Placeholder for saving to cloud storage"""

    def save(self, data, cloud_path: str):
        self.validate_data(data)
        # Future: real cloud upload logic
        return f"Uploaded {len(data) if isinstance(data, list) else 1} record(s) to {cloud_path}"
