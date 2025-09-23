from src.parser import JSONParser, CSVParser, TXTParser, DBParser

class ParserFactory:
    @staticmethod
    def get_parser(parser_type: str):
        parser_map = {
            "json": JSONParser,
            "csv": CSVParser,
            "txt": TXTParser,
            "db": DBParser
        }

        if parser_type.lower() not in parser_map:
            raise ValueError(f"Unsupported parser type: {parser_type}")

        return parser_map[parser_type.lower()]()
