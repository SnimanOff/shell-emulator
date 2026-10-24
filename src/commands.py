from src.vfs import Node


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
