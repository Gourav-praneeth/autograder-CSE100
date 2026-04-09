import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

BINARY = "Lab11_Question1.out"
SOURCE = "Lab11_Question1.cpp"


class TestGratuityCalculator(unittest.TestCase):
    # --------------- helpers ---------------
    def compile_program(self):
        proc = subprocess.Popen(
            ["g++", "-std=gnu++17", "-O2", "-o", BINARY, SOURCE],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = proc.communicate()
        return out.decode("utf-8"), err.decode("utf-8")

    def run_program(self, input_data: str) -> str:
        """Return full stdout as one string (don't split lines)."""
        proc = subprocess.Popen(
            [f"./{BINARY}"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, _ = proc.communicate(input=input_data.encode("utf-8"))
        return out.decode("utf-8").strip()

    def assertContains(self, expected: str, output: str, title: str):
        """Substring check with helpful snippet on failure."""
        if expected not in output:
            nearest = difflib.get_close_matches(expected, output.splitlines(), n=1)
            found = nearest[0] if nearest else (output[:500] + ("..." if len(output) > 500 else ""))
            self.fail(f"{title} failed.\nExpected: {expected}\nFound:    {found}")

    def assertNotContains(self, unexpected: str, output: str, title: str):
        if unexpected in output:
            self.fail(f"{title} failed.\nDid not expect to find: {unexpected}\nOutput: {output}")

    # --------------- tests ---------------

    @weight(0.2)
    def test_compile(self):
        """Test Case 0: Code compiles without errors"""
        _, err = self.compile_program()
        self.assertEqual(err.strip(), "", msg="Compilation failed:\n" + err)

    @weight(0.1)
    def test_banner_and_simple_tip(self):
        """Test Case 1: Banner, prompts, and tip for $100 at 15%"""
        # meal = 100 / 1.085; tip ≈ 13.82
        out = self.run_program("100\n0.15\n-1\n")
        self.assertContains("Gratuity Calculator", out, "Program title")
        self.assertContains("Calculated tip: $13.82", out, "Tip calculation")

    @weight(0.1)
    def test_sentinel_quits_immediately(self):
        """Test Case 2: Negative bill exits without computing a tip"""
        out = self.run_program("-1\n")
        self.assertContains("negative", out, "Quit instruction mentions negative bill")
        self.assertContains("Goodbye.", out, "Exit message")
        self.assertNotContains("Calculated tip:", out, "No tip when quitting immediately")

    @weight(0.1)
    def test_multiple_iterations(self):
        """Test Case 3: Two valid calculations then sentinel exit"""
        # 50 at 20% → 9.22; 1000 at 20% → 184.33
        out = self.run_program("50\n0.20\n1000\n0.20\n-1\n")
        self.assertContains("Calculated tip: $9.22", out, "First tip")
        self.assertContains("Calculated tip: $184.33", out, "Second tip")
        self.assertContains("Goodbye.", out, "Exit after loop")

    @weight(0.1)
    def test_zero_tip_rate(self):
        """Test Case 4: Zero tip rate yields $0.00"""
        out = self.run_program("100\n0\n-1\n")
        self.assertContains("Calculated tip: $0.00", out, "Zero tip")

    @weight(0.1)
    def test_pre_tax_round_trip(self):
        """Test Case 5: Total that divides cleanly pre-tax (10.85 / 1.085 = 10)"""
        out = self.run_program("10.85\n0.10\n-1\n")
        self.assertContains("Calculated tip: $1.00", out, "Clean rounding tip")

    @weight(0.1)
    def test_small_bill(self):
        """Test Case 6: Small bill with 10% tip"""
        # 1.085 / 1.085 = 1.00 pre-tax → $0.10 tip
        out = self.run_program("1.085\n0.10\n-1\n")
        self.assertContains("Calculated tip: $0.10", out, "Small bill tip")

    @weight(0.1)
    def test_negative_bill_after_one_tip(self):
        """Test Case 7: Sentinel after one calculation still exits cleanly"""
        out = self.run_program("50\n0.18\n-1\n")
        self.assertContains("Calculated tip: $8.29", out, "Tip before quit")
        self.assertContains("Goodbye.", out, "Goodbye on sentinel")

    @weight(0.1)
    def test_exact_two_dollar_tip(self):
        """Test Case 8: Pre-tax amount is round dollar (21.70 with tax, 10% tip → $2.00)"""
        out = self.run_program("21.70\n0.10\n-1\n")
        self.assertContains("Calculated tip: $2.00", out, "Two dollar tip")
