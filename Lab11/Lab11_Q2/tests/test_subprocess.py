import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

BINARY = "Lab11_Question2.out"
SOURCE = "Lab11_Question2.cpp"


class TestSoccerPoints(unittest.TestCase):
    # --------------- helpers ---------------
    def compile_program(self):
        proc = subprocess.Popen(
            ["g++", "-std=gnu++17", "-O2", "-o", BINARY, SOURCE],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        return out.decode("utf-8"), err.decode("utf-8")

    def run_program(self, input_data: str) -> str:
        """Return full stdout as one string (don't split lines)."""
        proc = subprocess.Popen(
            [f"./{BINARY}"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        out, _ = proc.communicate(input=input_data.encode("utf-8"))
        return out.decode("utf-8").strip()

    def assertContains(self, expected: str, output: str, title: str):
        """Substring check with helpful snippet on failure."""
        if expected not in output:
            nearest = difflib.get_close_matches(expected, output.splitlines(), n=1)
            found = nearest[0] if nearest else (output[:500] + ("..." if len(output) > 500 else ""))
            self.fail(f"{title} failed.\nExpected: {expected}\nFound:    {found}")

    # --------------- tests ---------------

    @weight(0.2)
    def test_compile(self):
        """Test Case 0: Code compiles without errors"""
        _, err = self.compile_program()
        self.assertEqual(err.strip(), "", msg="Compilation failed:\n" + err)

    @weight(0.2)
    def test_banner_team_and_points(self):
        """Test Case 1: Banner, team name, wins update points correctly"""
        out = self.run_program("Wildcats\n1\n1\n4\n5\n")
        self.assertContains("Soccer Points", out, "Program title")
        self.assertContains("Wildcats", out, "Team name in output")
        self.assertContains("Wins: 2", out, "Win count")
        self.assertContains("Total points: 6", out, "Two wins => 6 points")

    @weight(0.2)
    def test_ties_add_one_point(self):
        """Test Case 2: Ties contribute 1 point each"""
        out = self.run_program("Eagles\n2\n2\n4\n5\n")
        self.assertContains("Ties: 2", out, "Tie count")
        self.assertContains("Total points: 2", out, "Two ties => 2 points")

    @weight(0.2)
    def test_losses_zero_points(self):
        """Test Case 3: Losses do not add points"""
        out = self.run_program("Sharks\n3\n3\n4\n5\n")
        self.assertContains("Losses: 2", out, "Loss count")
        self.assertContains("Total points: 0", out, "Losses => 0 points")

    @weight(0.2)
    def test_three_invalid_menu_exits(self):
        """Test Case 4: Three invalid menu choices then exit message"""
        out = self.run_program("TestTeam\n9\n9\n9\n")
        self.assertContains("Invalid choice! Attempt 1 of 3.", out, "First invalid")
        self.assertContains("Invalid choice! Attempt 2 of 3.", out, "Second invalid")
        self.assertContains("Invalid choice! Attempt 3 of 3.", out, "Third invalid")
        self.assertContains("Too many invalid attempts!", out, "Exit after max invalid")
