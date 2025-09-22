from ..output_handler import LocalOutputHandler, CloudOutputHandler, DatabaseOutputHandler

class OutputHandlerFactory:
    @staticmethod
    def get_handler(output_config: dict):
        mapping = {
            "local": LocalOutputHandler(),
            "cloud": CloudOutputHandler(),
            "db": DatabaseOutputHandler()
        }
        output_type = output_config["type"]
        if output_type not in mapping:
            raise ValueError(f"Unsupported output type: {output_type}")
        return mapping[output_type]
