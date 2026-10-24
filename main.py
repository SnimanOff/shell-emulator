import argparse
import sys

from src.shell import Shell


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs")
    parser.add_argument("--script")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(f"[debug] vfs = {args.vfs}, script = {args.script}")
    shell = Shell()
    if args.script and not shell.run_script(args.script):
        sys.exit(1)
    shell.run()
    sys.exit(shell.exit_code)


if __name__ == "__main__":
    main()
