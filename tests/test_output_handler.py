import pytest
import json
from pathlib import Path
from src.output_handler import LocalOutputHandler, CloudOutputHandler, DatabaseOutputHandler


# -----------------------------
# UNIT TESTS
# -----------------------------

@pytest.mark.unit
def test_local_output_handler(tmp_path):
    handler = LocalOutputHandler()
    filepath = tmp_path / "out.txt"
    data = {"msg": "hello"}

    saved_path = handler.save(data, filepath)

    assert saved_path.exists()
    assert "hello" in saved_path.read_text()

@pytest.mark.unit
def test_cloud_output_handler():
    handler = CloudOutputHandler()
    result = handler.save({"msg": "hello"}, "cloud/output.json")
    assert "Uploaded" in result

@pytest.mark.unit
def test_db_output_handler():
    handler = DatabaseOutputHandler()
    result = handler.save({"msg": "hello"}, "table_name")
    assert "Saved" in result


# -----------------------------
# INTEGRATION TEST (config.json driven)
# -----------------------------
@pytest.mark.integration
def test_output_handler_from_config(tmp_path):
    config = json.loads(Path("config.json").read_text(encoding="utf-8"))

    if config["output"]["type"] == "local":
        handler = LocalOutputHandler()
        filepath = tmp_path / Path(config["output"]["path"]).name
        saved_path = handler.save({"msg": "test"}, filepath)

        assert saved_path.exists()
        assert "test" in saved_path.read_text()

    elif config["output"]["type"] == "cloud":
        handler = CloudOutputHandler()
        result = handler.save({"msg": "test"}, config["output"]["path"])
        assert "Uploaded" in result

    elif config["output"]["type"] == "db":
        handler = DatabaseOutputHandler()
        result = handler.save({"msg": "test"}, config["output"]["path"])
        assert "Saved" in result
