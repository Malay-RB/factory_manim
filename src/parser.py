import json
import csv
from abc import ABC, abstractmethod


class Parser(ABC):
    """Abstract base class for all parsers"""

    @abstractmethod
    def parse(self, raw_data):
        pass

    @staticmethod
    def validate_raw_data(raw_data):
        if raw_data is None or (isinstance(raw_data, str) and not raw_data.strip()):
            raise ValueError("Raw data cannot be empty")


class JSONParser(Parser):
    def parse(self, raw_data: str):
        self.validate_raw_data(raw_data)
        data = json.loads(raw_data)

        # If the root is already a list of sequences
        if isinstance(data, list):
            return {"sequences": data}

        # If root is a dict with "sequences"
        if isinstance(data, dict) and "sequences" in data:
            return data

        raise ValueError("Invalid JSON format. Expected a list of sequences or a dict with 'sequences'.")


# Keep other parsers for future use
class CSVParser(Parser):
    def parse(self, raw_data: str):
        self.validate_raw_data(raw_data)
        reader = csv.DictReader(raw_data.splitlines())
        return {"sequences": list(reader)}


class TXTParser(Parser):
    def parse(self, raw_data: str):
        self.validate_raw_data(raw_data)
        return {
            "sequences": [
                {"id": i + 1, "script": line.strip(), "voice_over": line.strip()}
                for i, line in enumerate(raw_data.splitlines()) if line.strip()
            ]
        }


class DBParser(Parser):
    def parse(self, raw_data: list[dict]):
        self.validate_raw_data(raw_data)
        return {"sequences": raw_data}
