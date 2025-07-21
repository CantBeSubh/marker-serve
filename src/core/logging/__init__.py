# TODO: I don't think this is the best way to do this


class Chalk:
    def __init__(self) -> None:
        from colorama import Fore, Style, init

        init()
        self.fore = Fore
        self.style = Style

    def red(self, text: str) -> str:
        return f"[!] {self.fore.RED}{text}{self.style.RESET_ALL}"

    def green(self, text: str) -> str:
        return f"[+] {self.fore.GREEN}{text}{self.style.RESET_ALL}"

    def yellow(self, text: str) -> str:
        return f"[x] {self.fore.YELLOW}{text}{self.style.RESET_ALL}"

    def blue(self, text: str) -> str:
        return f"[.] {self.fore.BLUE}{text}{self.style.RESET_ALL}"
