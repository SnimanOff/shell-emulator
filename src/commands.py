from datetime import datetime

from src.vfs import Node

DEFAULT_LINES = 10


class ShellError(Exception):
    pass


def get_node(shell, path: str) -> Node:
    node = shell.vfs.get(path)
    if node is None:
        raise ShellError(f"{path}: No such file or directory")
    return node


def cmd_ls(shell, args: list[str]) -> None:
    if len(args) > 1:
        raise ShellError("too many arguments")
    path = args[0] if args else "."
    node = get_node(shell, path)
    names = sorted(node.children) if node.is_dir else [path]
    for name in names:
        print(name)


def cmd_cd(shell, args: list[str]) -> None:
    if len(args) > 1:
        raise ShellError("too many arguments")
    path = args[0] if args else "~"
    if not get_node(shell, path).is_dir:
        raise ShellError(f"{path}: Not a directory")
    shell.vfs.cwd = shell.vfs.split(path)


def cmd_uptime(shell, args: list[str]) -> None:
    if args:
        raise ShellError("too many arguments")
    now = datetime.now()
    minutes = int((now - shell.started).total_seconds()) // 60
    hours, minutes = divmod(minutes, 60)
    print(f"{now:%H:%M:%S} up {hours}:{minutes:02}, 1 user")


def cmd_who(shell, args: list[str]) -> None:
    if args:
        raise ShellError("too many arguments")
    print(f"{shell.user} pts/0 {shell.started:%Y-%m-%d %H:%M}")


def cmd_tail(shell, args: list[str]) -> None:
    count = DEFAULT_LINES
    if args[:1] == ["-n"]:
        text = args[1] if len(args) > 1 else ""
        if not text.isdigit():
            raise ShellError(f"invalid number of lines: '{text}'")
        count = int(text)
        args = args[2:]
    if len(args) != 1:
        raise ShellError("expected one file")
    node = get_node(shell, args[0])
    if node.is_dir:
        raise ShellError(f"{args[0]}: Is a directory")
    lines = node.data.decode("utf-8", errors="replace").splitlines()
    for line in lines[max(len(lines) - count, 0):]:
        print(line)


def cmd_mkdir(shell, args: list[str]) -> None:
    if not args:
        raise ShellError("missing operand")
    for path in args:
        parts = shell.vfs.split(path)
        if not parts or shell.vfs.find(parts) is not None:
            raise ShellError(f"{path}: File exists")
        parent = shell.vfs.find(parts[:-1])
        if parent is None or not parent.is_dir:
            raise ShellError(f"{path}: No such file or directory")
        parent.children[parts[-1]] = Node(True)


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
    "uptime": cmd_uptime,
    "who": cmd_who,
    "tail": cmd_tail,
    "mkdir": cmd_mkdir,
    "exit": cmd_exit,
}
