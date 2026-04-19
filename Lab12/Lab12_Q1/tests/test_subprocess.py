import difflib
import os
import subprocess
import unittest

from gradescope_utils.autograder_utils.decorators import weight

LAB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
BINARY = "Lab12_Question1.out"
SOURCE = "Lab12_Question1.cpp"


class TestWorldSeriesWins(unittest.TestCase):
    def compile_program(self):
        proc = subprocess.Popen(
            ["g++", "-std=gnu++17", "-O2", "-o", BINARY, SOURCE],
            cwd=LAB_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        return out.decode("utf-8"), err.decode("utf-8")

    def run_program(self, input_data: str, fixture_name: str) -> str:
        exe = os.path.join(LAB_DIR, BINARY)
        fixture_dir = os.path.join(FIXTURES_DIR, fixture_name)
        proc = subprocess.Popen(
            [exe],
            cwd=fixture_dir,
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

    def assertNotContains(self, unexpected: str, output: str, title: str):
        if unexpected in output:
            self.fail(f"{title} failed.\nDid not expect to find: {unexpected}\nOutput: {output}")

    @weight(0.2)
    def test_compile(self):
        """Test Case 0"""
        _, err = self.compile_program()
        self.assertEqual(err.strip(), "", msg="Compilation failed:\n" + err)

    @weight(0.1)
    def test_one_team_then_exit(self):
        """Test Case 1"""
        inp = (
            "teams.txt\nWorldSeriesWinners.txt\n"
            "Boston RedSox\nBoston Red Sox\nn\n"
        )
        out = self.run_program(inp, "case_basic")
        self.assertContains("Enter the teams data file name:", out, "Teams file prompt")
        self.assertContains("Enter the World Series winners file name:", out, "Winners file prompt")
        self.assertContains("Contents of teams.txt:", out, "Teams header")
        self.assertContains("Boston Red Sox", out, "Team line")
        self.assertContains("New York Yankees", out, "Team line")
        self.assertContains("Enter the team name:", out, "Team prompt")
        self.assertContains(
            "Team name does not exist! Enter a different team.", out, "Invalid name"
        )
        self.assertContains("Boston Red Sox won 2 times.", out, "Sox wins")

    @weight(0.1)
    def test_invalid_team_filename_exits(self):
        """Test Case 2"""
        inp = "missing1.txt\n"
        out = self.run_program(inp, "case_minimal")
        self.assertContains("missing1.txt does not exist!", out, "Err message")
        self.assertNotContains("Enter the World Series winners file name:", out, "No winners prompt")

    @weight(0.1)
    def test_invalid_winners_filename_exits(self):
        """Test Case 3"""
        inp = "teams.txt\nbad1.txt\n"
        out = self.run_program(inp, "case_minimal")
        self.assertContains("bad1.txt does not exist!", out, "Err message")
        self.assertNotContains("Enter the team name:", out, "No team lookup")

    @weight(0.1)
    def test_two_lookups_then_exit(self):
        """Test Case 4"""
        #"""Test Case 4 — two lookups: each is 2 invalid names, then correct; then exit."""
        inp = (
            "teams.txt\nWorldSeriesWinners.txt\n"
            "Sun Devils\nYankees\nNew York Yankees\n"
            "y\n"
            "Team4\nTeam5\nBoston Red Sox\n"
            "n\n"
        )
        out = self.run_program(inp, "case_basic")
        err_msg = "Team name does not exist! Enter a different team."
        self.assertEqual(
            out.count(err_msg),
            4,
            msg="Expected two invalid-name errors per lookup.",
        )
        self.assertContains("New York Yankees won 1 times.", out, "Yankees count")
        self.assertContains("Boston Red Sox won 2 times.", out, "Sox count")
        self.assertContains("Look up another team? (y/n):", out, "Continue prompt")

    @weight(0.1)
    def test_three_invalid_team_names_then_exit(self):
        """Test Case 5"""
        inp = (
            "teams.txt\nWorldSeriesWinners.txt\n"
            "Not A Real Team\nAnother Fake\nSun Devils\n"
        )
        out = self.run_program(inp, "case_basic")
        self.assertContains("Team name does not exist! Enter a different team.", out, "Err 1")
        self.assertContains("Too many invalid attempts!", out, "Too many")
        self.assertNotContains("won ", out, "No win line")

    @weight(0.1)
    def test_invalid_team_name_then_invalid_continue_then_second_lookup(self):
        """Test Case 6"""
        #"""Test Case 6 — invalid name, then valid lookup, bad y/n, second lookup"""
        inp = (
            "teams.txt\nWorldSeriesWinners.txt\n"
            "Boston RedSox\n"
            "Boston Red Sox\n"
            "maybe\n"
            "y\n"
            "Boston Red Sox\n"
            "n\n"
        )
        out = self.run_program(inp, "case_basic")
        self.assertContains(
            "Team name does not exist! Enter a different team.", out, "Typo err"
        )
        self.assertContains("Boston Red Sox won 2 times.", out, "Sox wins")
        self.assertContains("Invalid choice. Please enter y or n.", out, "Bad continue")
        self.assertContains("Look up another team? (y/n):", out, "Continue prompt")