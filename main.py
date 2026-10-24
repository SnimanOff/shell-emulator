import argparse
import sys

from src.shell import Shell
from src.vfs import VFS, VFSError, load_vfs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs")
    parser.add_argument("--script")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(f"[debug] vfs = {args.vfs}, script = {args.script}")
    vfs = VFS()
    if args.vfs:
        try:
            vfs = load_vfs(args.vfs)
        except VFSError as error:
            print(f"vfs error: {error}")
            sys.exit(1)
    shell = Shell(vfs)
    if args.script and not shell.run_script(args.script):
        sys.exit(1)
    shell.run()
    sys.exit(shell.exit_code)


if __name__ == "__main__":
    main()
