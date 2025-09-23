from pathlib import Path
from datetime import datetime

class FileGenerator:
    """
    Generates .py and .txt files from parsed JSON data for Manim workflows.
    Now saves files inside the input folder.
    """

    BASE_INPUT_PATH = Path("input")  # Base folder for all generated files

    def generate(self, data: list[dict], base_name: str):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_path = self.BASE_INPUT_PATH / f"{base_name}_{timestamp}"
        base_path.mkdir(parents=True, exist_ok=True)

        generated_files = {"py_files": [], "txt_files": []}

        for item in data:
            seq = item.get("script_seq", "seq_unknown")
            folder_path = base_path / f"script_seq{seq}"
            folder_path.mkdir(parents=True, exist_ok=True)

            py_path = folder_path / f"script_seq{seq}.py"
            py_content = item.get("script_for_manim", "")
            py_path.write_text(py_content, encoding="utf-8")
            generated_files["py_files"].append(str(py_path))

            txt_path = folder_path / f"script_seq{seq}.txt"
            txt_content = item.get("script_voice_over", "")
            txt_path.write_text(txt_content, encoding="utf-8")
            generated_files["txt_files"].append(str(txt_path))

        print(f"🎉 Generated .py and .txt files for {len(data)} sequences at {base_path}")
        return generated_files
