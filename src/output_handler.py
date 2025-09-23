from pathlib import Path
from abc import ABC, abstractmethod
import subprocess
import os
import psycopg2
import json


class OutputHandler(ABC):
    @abstractmethod
    def save(self, data, destination):
        pass

    @staticmethod
    def validate_data(data):
        if data is None:
            raise ValueError("Data cannot be None")


class LocalOutputHandler(OutputHandler):
    """Saves parsed.json under input/parsed_file/"""

    def save(self, data: dict, output_config: dict):
        self.validate_data(data)
        path = Path(output_config["path"]) / output_config["file"]
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return path


class DatabaseOutputHandler(OutputHandler):
    """Optional handler for saving parsed data into DB"""

    def __connect(self):
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
            data = [data]

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


class ManimOutputHandler(OutputHandler):
    def save(self, data, config: dict):
        """
        data: {"sequences": [...]}
        config: {"type": "manim", "base_name": "...", "base_output_path": "..."}
        """
        self.validate_data(data)
        sequences = data.get("sequences", [])

        base_name = config.get("base_name", "script_data")
        base_path = Path(config.get("base_output_path", "input")) / "manim_files" / base_name
        base_path.mkdir(parents=True, exist_ok=True)

        generated_files = {"py_files": [], "txt_files": []}

        for seq in sequences:
            seq_num = seq.get("script_seq")
            py_content = f'"""{seq.get("script_for_manim")}"""'
            txt_content = seq.get("script_voice_over", "")

            seq_folder = base_path / f"script_seq{seq_num}"
            seq_folder.mkdir(parents=True, exist_ok=True)

            py_file = seq_folder / f"script_seq{seq_num}.py"
            py_file.write_text(py_content, encoding="utf-8")
            generated_files["py_files"].append(str(py_file))

            txt_file = seq_folder / f"script_seq{seq_num}.txt"
            txt_file.write_text(txt_content, encoding="utf-8")
            generated_files["txt_files"].append(str(txt_file))

        return generated_files



class VideoOutputHandler(OutputHandler):
    """Renders videos from generated .py files"""

    def __init__(self, quality="low"):
        self.quality_map = {
            "low": "l", "medium": "m", "high": "h", "production": "p", "4k": "k"
        }
        self.quality = self.quality_map.get(quality.lower(), "l")

    def save(self, manim_base_path: Path):
        self.validate_data(manim_base_path)
        if not manim_base_path.exists():
            raise FileNotFoundError(f"Manim folder not found: {manim_base_path}")

        py_files = list(manim_base_path.glob("script_seq*/script_seq*.py"))
        rendered_videos = []

        for py_file in py_files:
            scene_name = py_file.stem.capitalize()
            cmd = [
                "manim", "render",
                f"-q{self.quality}",
                str(py_file), scene_name
            ]
            print("🎬 Running:", " ".join(cmd))
            try:
                subprocess.run(cmd, check=True)
                rendered_videos.append(str(py_file))
            except subprocess.CalledProcessError as e:
                print(f"❌ Error rendering {py_file}: {e}")

        return rendered_videos
