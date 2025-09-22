import pytest
import json
from pathlib import Path
from src.input_handler import LocalFileInputHandler, CloudInputHandler, DatabaseInputHandler


# -----------------------------
# UNIT TESTS (isolated with tmp_path)
# -----------------------------

@pytest.mark.unit
@pytest.mark.parametrize("file_content,filename", [
    ('{"key": "value"}', "sample.json"),
    ("id,script\n1,Hello\n2,World", "sample.csv"),
    ("Line one\nLine two\nLine three", "sample.txt")
])
def test_localfileinputhandler(tmp_path, file_content, filename):
    """
    Unit test for LocalFileInputHandler with JSON, CSV, and TXT.
    Uses tmp_path so no real files are needed.
    """
    file_path = tmp_path / filename
    file_path.write_text(file_content, encoding="utf-8")

    handler = LocalFileInputHandler()
    raw_data = handler.load(file_path)

    assert isinstance(raw_data, str)
    assert raw_data.strip() != ""

@pytest.mark.unit
def test_file_not_found():
    """
    Ensure that loading a non-existent file raises FileNotFoundError.
    """
    handler = LocalFileInputHandler()
    fake_path = Path("non_existent_file.txt")
    with pytest.raises(FileNotFoundError):
        handler.load(fake_path)

@pytest.mark.unit
def test_cloud_input_handler():
    """
    Placeholder check for CloudInputHandler.
    """
    handler = CloudInputHandler()
    content = handler.load("some/cloud/path")
    assert "Simulated" in content

@pytest.mark.unit
def test_db_input_handler():
    """
    Placeholder check for DatabaseInputHandler.
    """
    handler = DatabaseInputHandler()
    content = handler.load("table_name")
    assert "Simulated" in content


# -----------------------------
# INTEGRATION TEST (config.json driven)
# -----------------------------

@pytest.mark.integration
def test_input_handler_from_config():
    """
    Integration test:
    Reads config.json and loads the actual file specified inside it.
    This ensures real workflow works dynamically based on config.
    """
    config_path = Path("config.json")
    assert config_path.exists(), "config.json not found!"

    config = json.loads(config_path.read_text(encoding="utf-8"))

    handler = LocalFileInputHandler()
    file_path = Path(config["input"]["path"])
    assert file_path.exists(), f"File {file_path} not found!"

    raw_data = handler.load(file_path)

    assert isinstance(raw_data, str)
    assert raw_data.strip() != ""
