from src.output_handler import LocalOutputHandler, DatabaseOutputHandler, ManimOutputHandler, VideoOutputHandler

class OutputHandlerFactory:
    @staticmethod
    def get_handler(output_config: dict):
        mapping = {
            "local": LocalOutputHandler(),
            "db": DatabaseOutputHandler(),
            "manim": ManimOutputHandler(),
            "video": VideoOutputHandler(quality=output_config.get("quality", "low"))
        }
        output_type = output_config["type"]
        if output_type not in mapping:
            raise ValueError(f"Unsupported output type: {output_type}")
        return mapping[output_type]
