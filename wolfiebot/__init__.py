import os
from dotenv import load_dotenv, find_dotenv

__version__ = "2.0.0"
__authors__ = "WolfIsOnline#6677"
__description__ = "A multi-tool bot with an emphasis on economy"


# load .env file
load_dotenv(find_dotenv())
MONGODB_CONNECTION = os.environ.get("MONGODB_CONNECTION")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

PAYDAY = 1000
DEFAULT_COLOR = 0x02e7e7
CASINO_COLOR = 0xBF40BF
CASINO_SYMBOL = "₵"
CURRENCY_NAME = "Eurodollar"
CURRENCY_ABBR = "ecu"
CURRENCY_SYMBOL = "§"
BANK_ID = 1027113096831053896