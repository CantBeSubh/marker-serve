from rich.console import Console


class Chalk:
    def __init__(self) -> None:
        self.console = Console()

    def error(self, text: str) -> None:
        self.console.print(f"ERROR:     {text}", style="red")

    def success(self, text: str) -> None:
        self.console.print(f"SUCCESS:     {text}", style="green")

    def warn(self, text: str) -> None:
        self.console.print(f"WARNING:     {text}", style="yellow")

    def info(self, text: str) -> None:
        self.console.print(f"INFO:      {text}", style="blue")
