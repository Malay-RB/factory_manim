import json
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.factories.input_handler_factory import InputHandlerFactory
from src.factories.parser_factory import ParserFactory
from src.factories.output_handler_factory import OutputHandlerFactory

# Load config
with open("db_config.json") as f:
    config = json.load(f)

# Step 1: Get InputHandler
input_config = config["input"]
db_config = config.get("db_config")   # fetch db_config if present
input_handler = InputHandlerFactory.get_handler(input_config["type"])

# Step 2: Load raw data (pass full config so handler can combine path+file or handle DB/cloud)
raw_data = input_handler.load(input_config)

# Step 3: Get Parser
parser = ParserFactory.get_parser(input_config["file_type"])

# Step 4: Parse data
parsed_data = parser.parse(raw_data)

# Step 5: Get OutputHandler via factory
output_config = config["output"]
output_handler = OutputHandlerFactory.get_handler(output_config)

# Step 6: Save output
output_file = output_handler.save(parsed_data, output_config)

print(f"Output saved to {output_file}")
