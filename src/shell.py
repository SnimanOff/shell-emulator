import getpass
import socket

from src.commands import COMMANDS, ShellError
from src.parser import ParseError, split_line, strip_comment
from src.vfs import VFS


class Shell:
    def __init__(self, vfs: VFS | None = None):
        self.user = getpass.getuser()
        self.host = socket.gethostname()
        self.vfs = vfs or VFS()
        self.running = True
        self.exit_code = 0

    def prompt(self) -> str:
        path = "~" + self.vfs.cwd_path() if self.vfs.cwd else "~"
        return f"{self.user}@{self.host}:{path}$ "

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

    def run_script(self, path: str) -> bool:
        try:
            with open(path, encoding="utf-8") as file:
                lines = file.read().splitlines()
        except (OSError, UnicodeDecodeError):
            print(f"script error: cannot open {path}")
            return False
        for number, line in enumerate(lines, 1):
            line = strip_comment(line).strip()
            if not line:
                continue
            print(f"{self.prompt()}{line}")
            if not self.execute(line):
                print(f"script error: line {number}")
            if not self.running:
                break
        return True

    def run(self) -> None:
        while self.running:
            try:
                line = input(self.prompt())
            except (EOFError, KeyboardInterrupt):
                print()
                break
            self.execute(line)
