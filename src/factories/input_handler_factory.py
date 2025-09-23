from src.input_handler import LocalFileInputHandler, DatabaseInputHandler, CloudInputHandler

class InputHandlerFactory:
    @staticmethod
    def get_handler(source_type: str):
        match source_type.lower():
            case "local":
                return LocalFileInputHandler()
            case "db":
                return DatabaseInputHandler()
            case "cloud":
                return CloudInputHandler()
            case _:
                raise ValueError(f"Unknown input handler type: {source_type}")
