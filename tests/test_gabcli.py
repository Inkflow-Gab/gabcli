import sys
import tempfile
import unittest
from pathlib import Path

from gabcli import Agent, GabClient
from gabcli_diff import colorize_diff, make_unified_diff, summarize


class DiffTests(unittest.TestCase):
    def test_diff_counts_additions_and_removals(self):
        diff = make_unified_diff("one\ntwo\n", "one\nthree\n", "demo.txt")
        summary = summarize(diff)
        self.assertEqual(summary.added, 1)
        self.assertEqual(summary.removed, 1)
        self.assertIn("-two", diff)
        self.assertIn("+three", diff)

    def test_plain_diff_has_no_ansi(self):
        diff = make_unified_diff("old\n", "new\n", "demo.txt")
        self.assertNotIn("\\033[", colorize_diff(diff, plain=True))


class SafetyTests(unittest.TestCase):
    def make_agent(self, root, **kwargs):
        client = GabClient("https://example.invalid/v1", "test", "test", plain=True)
        return Agent(client, root, plain=True, **kwargs)

    def test_tools_keep_paths_inside_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            agent = self.make_agent(root, auto_approve=True)
            agent.call_tool("write_file", {"path": "hello.txt", "content": "hello\n"})
            self.assertIn("hello", agent.call_tool("read_file", {"path": "hello.txt"}))
            result = agent.call_tool("read_file", {"path": "../outside.txt"})
            self.assertIn("outside the GabCli working directory", result)

    def test_find_files_and_live_command(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "app.py").write_text("print(1)\n", encoding="utf-8")
            agent = self.make_agent(root, auto_approve=True)
            self.assertIn("app.py", agent.call_tool("find_files", {"pattern": "*.py", "path": "."}))
            result = agent.call_tool(
                "run_command",
                {"command": f'{sys.executable} -c "print(123)"'},
            )
            self.assertIn("exit_code: 0", result)
            self.assertIn("123", result)

    def test_delete_requires_explicit_feature_flag(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "remove.txt").write_text("remove me\n", encoding="utf-8")
            blocked = self.make_agent(root, auto_approve=True)
            self.assertIn("--allow-delete", blocked.call_tool("delete_file", {"path": "remove.txt"}))
            allowed = self.make_agent(root, auto_approve=True, allow_delete=True)
            result = allowed.call_tool("delete_file", {"path": "remove.txt"})
            self.assertIn("Deleted", result)
            self.assertFalse((root / "remove.txt").exists())


if __name__ == "__main__":
    unittest.main()
