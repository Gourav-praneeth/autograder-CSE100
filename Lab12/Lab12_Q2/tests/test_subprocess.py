import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

BINARY = "Lab12_Question2.out"
SOURCE = "Lab12_Question2.cpp"


class TestUniqueSortedNames(unittest.TestCase):
    def compile_program(self):
        proc = subprocess.Popen(
            ["g++", "-std=gnu++17", "-O2", "-o", BINARY, SOURCE],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        return out.decode("utf-8"), err.decode("utf-8")

    def run_program(self, input_data: str) -> str:
        proc = subprocess.Popen(
            [f"./{BINARY}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, _ = proc.communicate(input=input_data.encode("utf-8"))
        return out.decode("utf-8").strip()

    def assertContains(self, expected: str, output: str, title: str):
        if expected not in output:
            nearest = difflib.get_close_matches(expected, output.splitlines(), n=1)
            found = nearest[0] if nearest else (output[:500] + ("..." if len(output) > 500 else ""))
            self.fail(f"{title} failed.\nExpected: {expected}\nFound:    {found}")

    def assertBefore(self, first: str, second: str, output: str, title: str):
        pos1 = output.find(first)
        pos2 = output.find(second)
        self.assertGreaterEqual(pos1, 0, f"{title}: '{first}' not found")
        self.assertGreaterEqual(pos2, 0, f"{title}: '{second}' not found")
        self.assertLess(pos1, pos2, f"{title}: order wrong")

    @weight(0.2)
    def test_compile(self):
        """Compilation"""
        _, err = self.compile_program()
        self.assertEqual(err.strip(), "", msg="Compilation failed:\n" + err)

    @weight(0.1)
    def test_duplicates_removed_sorted(self):
        """Test Case 1"""
        inp = (
            "Smith, Bart\n"
            "Collins, Bill\n"
            "Smith, Bart\n"
            "Michalski, Joe\n"
            "Griffin, Jim\n"
            "0\n"
        )
        out = self.run_program(inp)
        self.assertContains("Unique names:", out, "Output header")
        self.assertBefore("Collins, Bill", "Griffin, Jim", out, "Sort check 1")
        self.assertBefore("Griffin, Jim", "Michalski, Joe", out, "Sort check 2")
        self.assertBefore("Michalski, Joe", "Smith, Bart", out, "Sort check 3")
        self.assertEqual(out.count("Smith, Bart"), 1, "Duplicate name should appear once")

    @weight(0.1)
    def test_three_invalid_then_exit(self):
        """Test Case 2"""
        inp = "JohnsonJill\nJohnson,Jill\nJohnson Jill\n"
        out = self.run_program(inp)
        self.assertContains("Invalid name! Attempt 1 of 3.", out, "Attempt 1")
        self.assertContains("Invalid name! Attempt 2 of 3.", out, "Attempt 2")
        self.assertContains("Invalid name! Attempt 3 of 3.", out, "Attempt 3")
        self.assertContains("Too many Invalid Attempts!", out, "Fatal message")
        self.assertNotIn("Unique names:", out, "No output list on failure")

    @weight(0.1)
    def test_invalid_then_valid_recovery(self):
        """Test Case 3"""
        #"""One invalid, then valid entries and sentinel"""
        inp = "badname\nSmith, Alice\nLee, Bob\n0\n"
        out = self.run_program(inp)
        self.assertContains("Invalid name! Attempt 1 of 3.", out, "Single invalid")
        self.assertContains("Lee, Bob", out, "Second name present")
        self.assertContains("Smith, Alice", out, "First name present")
        self.assertBefore("Lee, Bob", "Smith, Alice", out, "Alphabetical by full string")

    @weight(0.1)
    def test_comma_without_space_invalid(self):
        """Test Case 4"""
        #"""Comma without following space is invalid"""
        inp = "Smith,Bart\nSmith, Bart\n0\n"
        out = self.run_program(inp)
        self.assertContains("Invalid name! Attempt 1 of 3.", out, "Smith,Bart invalid")
        self.assertContains("Smith, Bart", out, "Valid line accepted")

    @weight(0.1)
    def test_empty_only_sentinel(self):
        """Test Case 5"""
        #"""Only sentinel → empty unique list (header only)"""
        out = self.run_program("0\n")
        self.assertContains("Unique names:", out, "Header still printed")

    @weight(0.1)
    def test_all_duplicates_collapsed(self):
        """Test Case 6"""
        #"""Test Case 6 — all duplicate valid names"""
        inp = (
            "Adams, Amy\n"
            "Adams, Amy\n"
            "Adams, Amy\n"
            "0\n"
        )
        out = self.run_program(inp)
        self.assertContains("Unique names:", out, "Output header")
        self.assertEqual(out.count("Adams, Amy"), 1, "Duplicate names should appear once")