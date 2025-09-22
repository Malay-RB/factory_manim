import json
from pathlib import Path

import pytest
from src.input_handler import LocalFileInputHandler, CloudInputHandler, DatabaseInputHandler
from src.factories.parser_factory import ParserFactory
from src.output_handler import LocalOutputHandler, CloudOutputHandler, DatabaseOutputHandler


@pytest.mark.e2e
def test_pipeline_end_to_end(tmp_path):
    """End-to-end test: input -> parser -> output, driven by config.json"""

    # Load config.json
    config_path = Path("config.json")
    assert config_path.exists(), "config.json not found!"
    config = json.loads(config_path.read_text(encoding="utf-8"))

    # -------------------------
    # STEP 1: Input Handler
    # -------------------------
    input_type = config["input"]["type"]
    if input_type == "local":
        handler = LocalFileInputHandler()
        file_path = Path(config["input"]["path"])
        assert file_path.exists(), f"Input file {file_path} not found!"
        raw_data = handler.load(file_path)

    elif input_type == "cloud":
        handler = CloudInputHandler()
        raw_data = handler.load(config["input"]["path"])

    elif input_type == "db":
        handler = DatabaseInputHandler()
        raw_data = handler.load(config["input"]["path"])

    else:
        pytest.fail(f"Unknown input type: {input_type}")

    assert isinstance(raw_data, str)
    assert raw_data.strip() != ""

    # -------------------------
    # STEP 2: Parser
    # -------------------------
    parser = ParserFactory.get_parser(config["input"]["file_type"])
    parsed = parser.parse(raw_data)

    assert "sequences" in parsed
    assert len(parsed["sequences"]) > 0

    # -------------------------
    # STEP 3: Output Handler
    # -------------------------
    output_type = config["output"]["type"]
    if output_type == "local":
        handler = LocalOutputHandler()
        filepath = tmp_path / Path(config["output"]["path"]).name
        saved_path = handler.save(parsed, filepath)
        assert saved_path.exists()
        assert saved_path.read_text(encoding="utf-8").strip() != ""

    elif output_type == "cloud":
        handler = CloudOutputHandler()
        result = handler.save(parsed, config["output"]["path"])
        assert "Uploaded" in result

    elif output_type == "db":
        handler = DatabaseOutputHandler()
        result = handler.save(parsed, config["output"]["path"])
        assert "Saved" in result

    else:
        pytest.fail(f"Unknown output type: {output_type}")
