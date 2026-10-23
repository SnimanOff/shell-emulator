import getpass
import socket


class Shell:
    def __init__(self):
        self.user = getpass.getuser()
        self.host = socket.gethostname()
        self.running = True
        self.exit_code = 0

    def prompt(self) -> str:
        return f"{self.user}@{self.host}:~$ "

    def execute(self, line: str) -> bool:
        line = line.strip()
        if not line:
            return True
        if line == "exit":
            self.running = False
            return True
        print(f"{line}: command not found")
        return False

    def run(self) -> None:
        while self.running:
            try:
                line = input(self.prompt())
            except (EOFError, KeyboardInterrupt):
                print()
                break
            self.execute(line)
