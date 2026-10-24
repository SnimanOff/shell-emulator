import base64
import binascii
import csv

HEADER = ["path", "type", "data"]
DIR_MODE = 0o755
FILE_MODE = 0o644


class VFSError(Exception):
    pass


class Node:
    def __init__(self, is_dir: bool, data: bytes = b""):
        self.is_dir = is_dir
        self.data = data
        self.mode = DIR_MODE if is_dir else FILE_MODE
        self.children: dict[str, Node] = {}


class VFS:
    def __init__(self):
        self.root = Node(True)
        self.cwd: list[str] = []

    def split(self, path: str) -> list[str]:
        if path == "~" or path.startswith("~/"):
            parts = []
            path = path[1:]
        elif path.startswith("/"):
            parts = []
        else:
            parts = list(self.cwd)
        for name in path.split("/"):
            if name == "..":
                if parts:
                    parts.pop()
            elif name not in ("", "."):
                parts.append(name)
        return parts

    def find(self, parts: list[str]) -> Node | None:
        node = self.root
        for name in parts:
            if not node.is_dir or name not in node.children:
                return None
            node = node.children[name]
        return node

    def get(self, path: str) -> Node | None:
        return self.find(self.split(path))

    def cwd_path(self) -> str:
        return "/" + "/".join(self.cwd)


def decode(data: str) -> bytes:
    try:
        return base64.b64decode(data, validate=True)
    except (binascii.Error, ValueError):
        raise VFSError("data is not base64") from None


def add_row(vfs: VFS, row: list[str]) -> None:
    if len(row) != len(HEADER):
        raise VFSError(f"expected {len(HEADER)} columns")
    path, kind, data = row
    parts = [name for name in path.split("/") if name]
    parent = vfs.find(parts[:-1])
    if not parts or parent is None or not parent.is_dir:
        raise VFSError(f"no parent folder for '{path}'")
    if kind == "dir":
        parent.children[parts[-1]] = Node(True)
    elif kind == "file":
        parent.children[parts[-1]] = Node(False, decode(data))
    else:
        raise VFSError(f"unknown type '{kind}'")


def load_vfs(path: str) -> VFS:
    try:
        with open(path, encoding="utf-8", newline="") as file:
            rows = list(csv.reader(file))
    except FileNotFoundError:
        raise VFSError(f"file not found: {path}") from None
    except (OSError, UnicodeDecodeError):
        raise VFSError(f"cannot open {path}") from None
    if not rows or rows[0] != HEADER:
        raise VFSError("bad header, expected path,type,data")
    vfs = VFS()
    for number, row in enumerate(rows[1:], 2):
        try:
            add_row(vfs, row)
        except VFSError as error:
            raise VFSError(f"line {number}: {error}") from None
    return vfs
