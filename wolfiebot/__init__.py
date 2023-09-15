import os
from dotenv import load_dotenv, find_dotenv

__version__ = "2.2.0-devbuild"
__authors__ = "WolfIsOnline"
__description__ = "Wolfie is an AI conversational bot with its own personality."

# load .env file
load_dotenv(find_dotenv())
MONGODB_CONNECTION = os.environ.get("MONGODB_CONNECTION")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
DISCORD_API_KEY = os.environ.get("DISCORD_API_KEY")
WEBHOOK_ID = os.environ.get("WEBHOOK_ID")
WEBHOOK_TOKEN = os.environ.get("WEBHOOK_TOKEN")
INWORLD_KEY = os.environ.get("INWORLD_KEY")

PAYDAY = 1000
DEFAULT_COLOR = 0x02e7e7
CASINO_COLOR = 0xBF40BF
CASINO_SYMBOL = "₵"
CURRENCY_NAME = "Eurodollar"
CURRENCY_ABBR = "ecu"
CURRENCY_SYMBOL = "§"
BANK_ID = 1027113096831053896
