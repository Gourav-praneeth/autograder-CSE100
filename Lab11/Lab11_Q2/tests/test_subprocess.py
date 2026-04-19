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

    @weight(0.1)
    def test_case_1_mixed_valid_invalid_then_exit(self):
        """Test Case 1"""
        #"""Test Case 1: some name — W,W, invalid, T, invalid, L, W, E"""
        # Invalid choices use 9 (not W/T/L/D/E).
        out = self.run_program("Sun Devils\nW\nW\n9\nT\n9\nL\nW\nE\n")
        self.assertContains("SOCCER POINTS", out, "Program title")
        self.assertContains("Team Name\t: Sun Devils", out, "Team name in output")
        self.assertContains("Invalid choice! Attempt 1 of 3.", out, "First invalid")
        self.assertContains("Invalid choice! Attempt 2 of 3.", out, "Second invalid")
        self.assertContains("Wins\t\t: 3", out, "Win count")
        self.assertContains("Ties\t\t: 1", out, "Tie count")
        self.assertContains("Losses\t\t: 1", out, "Loss count")
        self.assertContains("Total Points\t: 10", out, "Points 3*3+1")

    @weight(0.1)
    def test_case_2_sun_devils_w_t_l_e(self):
        """Test Case 2"""
        #"""Test Case 2: Sun Devils — W, T, L, E"""
        out = self.run_program("Sun Devils\nW\nT\nL\nE\n")
        self.assertContains("Team Name\t: Sun Devils", out, "Team name in output")
        self.assertContains("Wins\t\t: 1", out, "Win count")
        self.assertContains("Ties\t\t: 1", out, "Tie count")
        self.assertContains("Losses\t\t: 1", out, "Loss count")
        self.assertContains("Total Points\t: 4", out, "3+1+0 points")

    @weight(0.1)
    def test_case_3_team_name_display_and_case(self):
        """Test Case 3"""
        #"""Test Case 3: Lakers — W,W,w,T, LD, W, TE (L then D, T then E)"""
        out = self.run_program("Lakers\nW\nW\nw\nT\nL\nD\nW\nT\nE\n")
        self.assertContains("Team Name\t: Lakers", out, "Team name in output")
        self.assertContains("Wins\t\t: 4", out, "Win count")
        self.assertContains("Ties\t\t: 2", out, "Tie count")
        self.assertContains("Losses\t\t: 1", out, "Loss count")
        self.assertContains("Total Points\t: 14", out, "4*3+2 points")

    @weight(0.1)
    def test_case_4_name_w_t_l_l_w_d_e(self):
        """Test Case 4"""
        #"""Test Case 4: Name — W,T,L,L,w,D,E"""
        out = self.run_program("Cardinals\nW\nT\nL\nL\nw\nD\nE\n")
        self.assertContains("Team Name\t: Cardinals", out, "Team name in output")
        self.assertContains("Wins\t\t: 2", out, "Win count")
        self.assertContains("Ties\t\t: 1", out, "Tie count")
        self.assertContains("Losses\t\t: 2", out, "Loss count")
        self.assertContains("Total Points\t: 7", out, "2*3+1 points")

    @weight(0.1)
    def test_case_5_three_invalid_only(self):
        """Test Case 5"""
        #"""Test Case 5: Three invalid menu choices then exit message"""
        out = self.run_program("Tigers\n9\n9\n9\n")
        self.assertContains("Invalid choice! Attempt 1 of 3.", out, "First invalid")
        self.assertContains("Invalid choice! Attempt 2 of 3.", out, "Second invalid")
        self.assertContains("Invalid choice! Attempt 3 of 3.", out, "Third invalid")
        self.assertContains("Too many Invalid Attempts!", out, "Exit after max invalid")

    @weight(0.1)
    def test_case_6_games_then_three_invalid(self):
        """Test Case 6"""
        #"""Test Case 6: W,T,L,L then three invalid attempts"""
        out = self.run_program("Terps\nW\nT\nL\nL\n9\n9\n9\n")
        self.assertContains("Invalid choice! Attempt 1 of 3.", out, "First invalid")
        self.assertContains("Invalid choice! Attempt 2 of 3.", out, "Second invalid")
        self.assertContains("Invalid choice! Attempt 3 of 3.", out, "Third invalid")
        self.assertContains("Too many Invalid Attempts!", out, "Exit after max invalid")
        self.assertContains("Team Name\t: Terps", out, "Team name in output")
        self.assertContains("Wins\t\t: 1", out, "Win count")
        self.assertContains("Ties\t\t: 1", out, "Tie count")
        self.assertContains("Losses\t\t: 2", out, "Loss count")
        self.assertContains("Total Points\t: 4", out, "3+1+0 points")