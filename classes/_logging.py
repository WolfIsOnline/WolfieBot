import logging
from rich.logging import RichHandler

class _Logging:
    def __init__(self):
        FORMAT = "%(message)s"
        logging.basicConfig(level="INFO", format=FORMAT, datefmt="[%x@%X]", handlers=[RichHandler()])