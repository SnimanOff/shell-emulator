import sys

from src.shell import Shell


def main() -> None:
    shell = Shell()
    shell.run()
    sys.exit(shell.exit_code)


if __name__ == "__main__":
    main()
