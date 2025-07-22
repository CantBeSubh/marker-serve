from datetime import datetime

from rich.console import Console


class Chalk:
    def __init__(self) -> None:
        self.console = Console()

    def error(self, text: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.console.print(f"[{timestamp}] ERROR:     {text}", style="red")

    def success(self, text: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.console.print(f"[{timestamp}] SUCCESS:     {text}", style="green")

    def warn(self, text: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.console.print(f"[{timestamp}] WARNING:     {text}", style="yellow")

    def info(self, text: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.console.print(f"[{timestamp}] INFO:      {text}", style="blue")
