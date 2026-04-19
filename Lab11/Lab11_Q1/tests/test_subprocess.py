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
    def test_case_1_one_valid_then_exit(self):
        """Test Case 1"""
        #"""Test Case 1: One valid bill/tip and exit (n)"""
        # tax 0 → default 8.5%; $100 @ 15% → $13.82
        out = self.run_program("0\n100\n0.15\nn\n")
        self.assertContains("Gratuity Calculator", out, "Program title")
        self.assertContains("Total Bill Amount: $100.00", out, "Total bill")
        self.assertContains("Tax Rate: 8.50%", out, "Tax rate")
        self.assertContains("Tip Rate: 15.00%", out, "Tip rate line")
        self.assertContains("Tip Amount: $13.82", out, "Tip amount")

    @weight(0.1)
    def test_case_2_three_invalid_bills_negative_values(self):
        """Test Case 2"""
        #"""Test Case 2: Three invalid bills (different negative amounts) then exit"""
        out = self.run_program("0\n-1\n-2.5\n-100\n")
        self.assertContains("Invalid input. Attempt 1 of 3. Value must be positive.", out, "Bill attempt 1")
        self.assertContains("Invalid input. Attempt 2 of 3. Value must be positive.", out, "Bill attempt 2")
        self.assertContains("Invalid input. Attempt 3 of 3. Value must be positive.", out, "Bill attempt 3")
        self.assertContains("Too many invalid attempts!", out, "Exit after bad bills")
        self.assertNotContains("Tip Amount:", out, "No tip computed")

    @weight(0.1)
    def test_case_3_two_valid_calculations_then_exit(self):
        """Test Case 3"""
        #"""Test Case 3: Two valid calculations then n to quit"""
        # default tax 0.085: 50 @ 20% → 9.22; 1000 @ 20% → 184.33
        out = self.run_program("0\n50\n0.20\ny\n1000\n0.20\nn\n")
        self.assertContains("Tip Amount: $9.22", out, "First tip")
        self.assertContains("Tip Amount: $184.33", out, "Second tip")

    @weight(0.1)
    def test_case_4_tax_zero_three_invalid_tips(self):
        """Test Case 4"""
        #"""Test Case 4: Tax 0 (default rate) and three invalid tip entries"""
        out = self.run_program("0\n100\n0\n-0.5\n-1\n")
        self.assertContains("Invalid input. Attempt 1 of 3. Value must be positive.", out, "Tip 1")
        self.assertContains("Invalid input. Attempt 2 of 3. Value must be positive.", out, "Tip 2")
        self.assertContains("Invalid input. Attempt 3 of 3. Value must be positive.", out, "Tip 3")
        self.assertContains("Too many invalid attempts!", out, "Too many tip attempts")
        self.assertNotContains("Tip Amount:", out, "No tip output")

    @weight(0.1)
    def test_case_5_rounding_tip(self):
        """Test Case 5"""
        #"""Test Case 5: Rounded tip display (setprecision 2)"""
        # 10.85 / 1.085 = 10.00 pre-tax; 10% tip → $1.00
        out = self.run_program("0\n10.85\n0.10\nn\n")
        self.assertContains("Tip Amount: $1.00", out, "Rounded tip")

    @weight(0.1)
    def test_case_6_multiple_invalid_then_valid_each(self):
        """Test Case 6"""
        #"""Test Case 6: Invalid bill then valid; invalid tips then valid; invalid continue then n"""
        # tax 0.085; bill 0 invalid → 1.085; tip 0 and -0.5 invalid → 0.10; continue h, i invalid → n
        out = self.run_program("0.085\n0\n1.085\n0\n-0.5\n0.10\nh\ni\nn\n")
        self.assertGreaterEqual(
            out.count("Invalid input. Attempt 1 of 3. Value must be positive."),
            2,
            "Invalid bill and first invalid tip",
        )
        self.assertContains(
            "Invalid input. Attempt 2 of 3. Value must be positive.",
            out,
            "Second invalid tip",
        )
        self.assertContains("Invalid choice. Attempt 1 of 3.", out, "Invalid continue h")
        self.assertContains("Invalid choice. Attempt 2 of 3.", out, "Invalid continue i")
        self.assertContains("Tip Amount: $0.10", out, "Correct tip after recovery")
