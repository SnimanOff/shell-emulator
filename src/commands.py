class ShellError(Exception):
    pass


def cmd_ls(shell, args: list[str]) -> None:
    print(f"ls {args}")


def cmd_cd(shell, args: list[str]) -> None:
    if len(args) > 1:
        raise ShellError("too many arguments")
    print(f"cd {args}")


def cmd_exit(shell, args: list[str]) -> None:
    if len(args) > 1:
        raise ShellError("too many arguments")
    if args and not args[0].isdigit():
        raise ShellError(f"{args[0]}: numeric argument required")
    shell.exit_code = int(args[0]) if args else 0
    shell.running = False


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
}
