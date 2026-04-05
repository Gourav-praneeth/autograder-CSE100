import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

BINARY = "Lab10_Question2.out"
SOURCE = "Lab10_Question2.cpp"

INVALID_MSG = "Invalid input! Expenses should be non-negative."
EXIT_MSG = "Too many Invalid Attempts!"
COMPARISON_HEADER = "=== Four-month budget comparison ==="


def month_lines(*vals):
    """One month: five expense lines (Housing, Food, Medical, Entertainment, Miscellaneous)."""
    assert len(vals) == 5
    return "".join(f"{v}\n" for v in vals)


def four_months(*months):
    """Each argument is a 5-tuple of expenses for that month."""
    return "".join(month_lines(*m) for m in months)


class TestMonthlyBudget(unittest.TestCase):
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
            nearest = difflib.get_close_matches(
                expected, output.splitlines(), n=1
            )
            found = (
                nearest[0]
                if nearest
                else (output[:500] + ("..." if len(output) > 500 else ""))
            )
            self.fail(
                f"{title} failed.\nExpected: {expected}\nFound:    {found}"
            )

    def assertNotContains(self, unexpected: str, output: str, title: str):
        if unexpected in output:
            self.fail(
                f"{title} failed.\nDid not expect to find: {unexpected}\nOutput: {output}"
            )

    ON_BUDGET = (1200, 300, 100, 150, 250)

    @weight(0.2)
    def test_compile(self):
        """Test Case 0: Code compiles without errors"""
        _, err = self.compile_program()
        self.assertEqual(err.strip(), "", msg="Compilation failed:\n" + err)

    @weight(0.1)
    def test_case_1_valid_mixed_with_zero(self):
        """Test Case 1: All valid tests"""
        m1 = (1300, 40, 260, 100, 50)
        m2 = (1000, 40, 260, 100, 50)
        m3_with_zero = (1200, 300, 100, 150, 0)
        inp = four_months(m1, m2, m3_with_zero, self.ON_BUDGET)
        out = self.run_program(inp)
        self.assertContains(COMPARISON_HEADER, out, "Comparison header")
        self.assertContains("Housing: Saved: $100.00", out, "Housing saved (4-mo)")
        self.assertContains("Food: Saved: $520.00", out, "Food saved (4-mo)")
        self.assertContains("Medical: Over expenditure: $320.00", out, "Medical over (4-mo)")
        self.assertContains("Entertainment: Saved: $100.00", out, "Entertainment saved")
        self.assertContains("Miscellaneous: Saved: $650.00", out, "Misc saved (includes 0)")

    @weight(0.1)
    def test_case_2_three_invalid_same_element(self):
        """Test Case 2: Invalid checks for same element"""
        out = self.run_program("-1\n-2\n-3\n")
        self.assertContains(INVALID_MSG, out, "Invalid message")
        self.assertContains(EXIT_MSG, out, "Exit message")
        self.assertNotContains(COMPARISON_HEADER, out, "No comparison after exit")

    @weight(0.1)
    def test_case_3_three_invalid_different_elements(self):
        """Test Case 3: Invalid checks for different elements"""
        out = self.run_program("1800\n40\n-3\n3\n-4\n4\n-5\n")
        self.assertContains(INVALID_MSG, out, "Invalid message")
        self.assertContains(EXIT_MSG, out, "Exit message")
        self.assertNotContains(COMPARISON_HEADER, out, "No comparison after exit")

    @weight(0.1)
    def test_case_4_invalids_two_months_then_on_budget(self):
        """Test Case 4: Invalid checks for two months"""
        m = self.ON_BUDGET
        inp = (
            "-1\n"
            + month_lines(*m)
            + "-5\n-13.5\n"
            + month_lines(*m)
            + month_lines(*m)
            + month_lines(*m)
        )
        out = self.run_program(inp)
        self.assertContains(INVALID_MSG, out, "Invalid message")
        self.assertContains(COMPARISON_HEADER, out, "Completes successfully")
        self.assertContains("Housing: On budget", out, "On budget housing")
        self.assertContains("Food: On budget", out, "On budget food")
        self.assertContains("Medical: On budget", out, "On budget medical")
        self.assertContains("Entertainment: On budget", out, "On budget entertainment")
        self.assertContains("Miscellaneous: On budget", out, "On budget misc")

    @weight(0.1)
    def test_case_5_all_valid_all_above_budget(self):
        """Test Case 5: Monthly over budget"""
        hi = (1300, 400, 200, 200, 300)
        inp = four_months(hi, hi, hi, hi)
        out = self.run_program(inp)
        self.assertContains(COMPARISON_HEADER, out, "Comparison header")
        self.assertNotContains("Saved:", out, "No savings when all over")
        self.assertContains("Housing: Over expenditure: $400.00", out, "Housing over")
        self.assertContains("Food: Over expenditure: $400.00", out, "Food over")
        self.assertContains("Medical: Over expenditure: $400.00", out, "Medical over")

    @weight(0.1)
    def test_case_6_all_valid_all_below_budget(self):
        """Test Case 6: Monthly below budget"""
        lo = (1000, 200, 50, 100, 100)
        inp = four_months(lo, lo, lo, lo)
        out = self.run_program(inp)
        self.assertContains(COMPARISON_HEADER, out, "Comparison header")
        self.assertNotContains("Over expenditure:", out, "No over when all under")
        self.assertContains("Housing: Saved: $800.00", out, "Housing saved")
        self.assertContains("Food: Saved: $400.00", out, "Food saved")
