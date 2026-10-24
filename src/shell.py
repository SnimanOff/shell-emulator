import getpass
import socket

from src.commands import COMMANDS, ShellError
from src.parser import ParseError, split_line


class Shell:
    def __init__(self):
        self.user = getpass.getuser()
        self.host = socket.gethostname()
        self.running = True
        self.exit_code = 0

    def prompt(self) -> str:
        return f"{self.user}@{self.host}:~$ "

    def execute(self, line: str) -> bool:
        try:
            args = split_line(line)
        except ParseError as error:
            print(f"parse error: {error}")
            return False
        if not args:
            return True
        name = args[0]
        if name not in COMMANDS:
            print(f"{name}: command not found")
            return False
        try:
            COMMANDS[name](self, args[1:])
        except ShellError as error:
            print(f"{name}: {error}")
            return False
        return True

    def run(self) -> None:
        while self.running:
            try:
                line = input(self.prompt())
            except (EOFError, KeyboardInterrupt):
                print()
                break
            self.execute(line)
