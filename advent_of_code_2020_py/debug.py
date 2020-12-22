import logging

import rich
from rich import logging as rich_logging
from rich import traceback

traceback.install()

console = rich.console.Console()

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[rich_logging.RichHandler()],
)

log = logging.getLogger("rich")
