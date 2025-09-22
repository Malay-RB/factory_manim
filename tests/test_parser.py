import pytest
import json
from pathlib import Path
from src.parser import JSONParser, CSVParser, TXTParser
from src.factories.parser_factory import ParserFactory


# -----------------------------
# UNIT TESTS
# -----------------------------

@pytest.mark.unit
def test_json_parser():
    raw_data = '{"sequences": [{"id": 1, "script": "Hello"}]}'
    parser = JSONParser()
    parsed = parser.parse(raw_data)

    assert "sequences" in parsed
    assert parsed["sequences"][0]["script"] == "Hello"

@pytest.mark.unit
def test_csv_parser():
    raw_data = "id,script\n1,Hello\n2,World"
    parser = CSVParser()
    parsed = parser.parse(raw_data)

    assert "sequences" in parsed
    assert parsed["sequences"][1]["script"] == "World"

@pytest.mark.unit
def test_txt_parser():
    raw_data = "Line one\nLine two"
    parser = TXTParser()
    parsed = parser.parse(raw_data)

    assert "sequences" in parsed
    assert parsed["sequences"][0]["script"] == "Line one"


# -----------------------------
# INTEGRATION TEST (config.json driven)
# -----------------------------

@pytest.mark.integration
def test_parser_from_config():
    config = json.loads(Path("config.json").read_text(encoding="utf-8"))
    file_path = Path(config["input"]["path"])
    raw_data = file_path.read_text(encoding="utf-8")

    parser = ParserFactory.get_parser(config["input"]["file_type"])
    parsed = parser.parse(raw_data)

    assert "sequences" in parsed
    assert len(parsed["sequences"]) > 0
