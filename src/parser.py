import json
import csv
from abc import ABC, abstractmethod


class Parser(ABC):
    """Abstract base class for all parsers"""

    @abstractmethod
    def parse(self, raw_data):
        """Parse raw input data into structured format"""
        pass

    @staticmethod
    def validate_raw_data(raw_data):
        """Utility validation for non-empty input"""
        if raw_data is None or (isinstance(raw_data, str) and not raw_data.strip()):
            raise ValueError("Raw data cannot be empty")


class JSONParser(Parser):
    def parse(self, raw_data: str):
        self.validate_raw_data(raw_data)
        return json.loads(raw_data)


class CSVParser(Parser):
    def parse(self, raw_data: str):
        self.validate_raw_data(raw_data)
        reader = csv.DictReader(raw_data.splitlines())
        return {"sequences": list(reader)}


class TXTParser(Parser):
    def parse(self, raw_data: str):
        self.validate_raw_data(raw_data)
        return {"sequences": [
            {"id": i+1, "script": line.strip(), "voice_over": line.strip()}
            for i, line in enumerate(raw_data.splitlines())
            if line.strip()
        ]}


class DBParser(Parser):
    def parse(self, raw_data: list[dict]):
        """
        raw_data: list of dicts from DBInputHandler, e.g.:
        [{"user_id": 1, "name": "Alice", "email": "a@b.com"}, ...]
        """
        self.validate_raw_data(raw_data)

        sequences = []
        for row in raw_data:
            # Map every column dynamically
            sequence = {k: v for k, v in row.items()}
            sequences.append(sequence)

        return {"sequences": sequences}

