import re
from datetime import datetime

from src.vfs import Node

DEFAULT_LINES = 10
RWX = "rwx"
MODE_BITS = 9
OCTAL_MODE = re.compile(r"[0-7]{1,3}")


class ShellError(Exception):
    pass


def get_node(shell, path: str) -> Node:
    node = shell.vfs.get(path)
    if node is None:
        raise ShellError(f"{path}: No such file or directory")
    return node


def mode_string(node: Node) -> str:
    bits = "".join(
        RWX[index % len(RWX)] if node.mode >> (MODE_BITS - 1 - index) & 1
        else "-"
        for index in range(MODE_BITS)
    )
    return ("d" if node.is_dir else "-") + bits


def cmd_ls(shell, args: list[str]) -> None:
    detailed = "-l" in args
    paths = [arg for arg in args if arg != "-l"]
    if len(paths) > 1:
        raise ShellError("too many arguments")
    path = paths[0] if paths else "."
    node = get_node(shell, path)
    items = sorted(node.children.items()) if node.is_dir else [(path, node)]
    for name, item in items:
        print(f"{mode_string(item)} {name}" if detailed else name)


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


def cmd_chmod(shell, args: list[str]) -> None:
    if not args[1:]:
        raise ShellError("missing operand")
    if not OCTAL_MODE.fullmatch(args[0]):
        raise ShellError(f"invalid mode: '{args[0]}'")
    nodes = [get_node(shell, path) for path in args[1:]]
    for node in nodes:
        node.mode = int(args[0], 8)


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
    "chmod": cmd_chmod,
    "exit": cmd_exit,
}
