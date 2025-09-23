from pathlib import Path
import json
from src.factories.input_handler_factory import InputHandlerFactory
from src.factories.output_handler_factory import OutputHandlerFactory
from src.parser import JSONParser


def main():
    # Load config
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    input_config = config["input"]
    parsed_config = config["parsed_copy"]
    manim_config = config["manim_output"]
    video_config = config["video_output"]

    # Get factories
    input_handler = InputHandlerFactory.get_handler(input_config["type"])
    video_handler = OutputHandlerFactory.get_handler(video_config)
    manim_handler = OutputHandlerFactory.get_handler(manim_config)

    if manim_config.get("regenerate", True):
        # Step 1: Load raw JSON
        raw_data = input_handler.load(input_config)

        # Step 2: Parse JSON into structured data
        parser = JSONParser()
        parsed_data = parser.parse(raw_data)

        # Step 3: Save parsed copy
        parsed_output_handler = OutputHandlerFactory.get_handler(parsed_config)
        parsed_output_handler.save(parsed_data, parsed_config)
        print("✅ Saved parsed JSON copy")

        # Step 4: Generate Manim .py & .txt files
        generated_files = manim_handler.save(parsed_data, manim_config)
        print("✅ Generated Manim files:", generated_files)

    else:
        print("♻️ Skipping parsing and Manim file generation. Using existing files.")

    # Step 5: Render videos from Manim files
    manim_base_path = Path(manim_config["path"]) / manim_config["base_name"]
    rendered_videos = video_handler.save(manim_base_path)
    print("🎬 Rendered videos:", rendered_videos)


if __name__ == "__main__":
    main()
