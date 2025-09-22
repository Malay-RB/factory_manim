from ..parser import JSONParser, CSVParser, TXTParser, DBParser

class ParserFactory:
    @staticmethod
    def get_parser(parser_type: str):
        """Directly returns the appropriate Parser"""
        match parser_type.lower():
            case "json":
                return JSONParser()
            case "csv":
                return CSVParser()
            case "txt":
                return TXTParser()
            case "db":
                return DBParser()
            case _:
                raise ValueError(f"Unsupported parser type: {parser_type}")
