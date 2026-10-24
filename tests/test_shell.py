import io
import unittest
from contextlib import redirect_stdout

from src.parser import ParseError, split_line, strip_comment
from src.shell import Shell
from src.vfs import VFSError, load_vfs


def run(shell: Shell, line: str) -> str:
    output = io.StringIO()
    with redirect_stdout(output):
        shell.execute(line)
    return output.getvalue().strip()


class TestParser(unittest.TestCase):
    def test_quotes(self):
        line = "ls \"my dir\" 'a b' c"
        self.assertEqual(split_line(line), ["ls", "my dir", "a b", "c"])

    def test_unclosed_quote(self):
        with self.assertRaises(ParseError):
            split_line('cd "abc')

    def test_comment(self):
        self.assertEqual(strip_comment("ls '#a' # text"), "ls '#a' ")


class TestVFS(unittest.TestCase):
    def test_load(self):
        vfs = load_vfs("vfs/deep.csv")
        self.assertTrue(vfs.get("/home/user/docs/work").is_dir)
        self.assertEqual(vfs.get("/etc/hostname").data, b"emulator\n")

    def test_errors(self):
        for path in ["vfs/nope.csv", "vfs/bad.csv"]:
            with self.assertRaises(VFSError):
                load_vfs(path)


class TestShell(unittest.TestCase):
    def setUp(self):
        self.shell = Shell()

    def test_unknown(self):
        self.assertEqual(run(self.shell, "foo"), "foo: command not found")

    def test_cd_args(self):
        self.assertEqual(run(self.shell, "cd a b"), "cd: too many arguments")

    def test_exit(self):
        run(self.shell, "exit 3")
        self.assertFalse(self.shell.running)
        self.assertEqual(self.shell.exit_code, 3)
