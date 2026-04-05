import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

BINARY = "Lab10_Question1.out"
SOURCE = "Lab10_Question1.cpp"


class TestPayrollSystem(unittest.TestCase):
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
    def test_valid_flow_simple(self):
        """Test Case 1: Simple valid inputs compute gross/net"""
        # rate=20, hours=10 -> gross=200.00, net=170.00
        out = self.run_program("20\n10\n")
        self.assertContains("Gross Pay: $200.00", out, "Gross pay calculation")
        self.assertContains("Net Pay:   $170.00", out, "Net pay calculation")

    # @weight(0.1)
    # def test_invalid_pay_rate_zero_then_valid(self):
    #     """Test Case 2: Zero pay rate is invalid, then valid rate succeeds"""
    #     out = self.run_program("0\n0.15\n10\n")
    #     self.assertContains("Invalid input. Pay rate must be positive.", out, "Invalid rate message")
    #     self.assertContains("Gross Pay: $1.50", out, "Gross after valid rate")
    #     self.assertContains("Net Pay:   $14.78", out, "Net after valid rate")

    @weight(0.1)
    def test_pay_rate_three_invalids_then_exit(self):
        """Test Case 2: Three invalid pay rates then exit"""
        out = self.run_program("-1\n0\n-2\n")
        self.assertContains("Invalid input. Pay rate must be positive.", out, "Invalid rate message")
        self.assertContains("Too many invalid attempts!", out, "Too many attempts exit")
        self.assertNotContains("Gross Pay:", out, "No output after termination")

    @weight(0.1)
    def test_invalid_rate_then_correct(self):
        """Test Case 3: Invalid pay rate then correction"""
        # rate: -5 (invalid), -13.5 (invalid), then 15.25 (valid); hours: 10
        out = self.run_program("-5\n-13.5\n15.25\n10\n")
        self.assertContains("Invalid input. Pay rate must be positive.", out, "Invalid rate message")
        self.assertContains("Gross Pay: $152.50", out, "Gross after fix")
        self.assertContains("Net Pay:   $129.62", out, "Net after fix")

    @weight(0.1)
    def test_hours_three_invalids_then_exit(self):
        """Test Case 4: Hours invalid 3 times"""
        out = self.run_program("25\n0\n81\n-3\n")
        self.assertContains("Invalid input. Hours must be between 1 and 80.", out, "Invalid hours message")
        self.assertContains("Too many invalid attempts!", out, "Too many attempts exit")
        self.assertNotContains("Gross Pay:", out, "No output after termination")

    @weight(0.1)
    def test_boundary_hours_80(self):
        """Test Case 5: Boundary check"""
        out = self.run_program("25\n80\n")
        self.assertContains("Gross Pay: $2000.00", out, "Gross at boundary")
        self.assertContains("Net Pay:   $1700.00", out, "Net at boundary")

    @weight(0.1)
    def test_two_decimal_rounding(self):
        """Test Case 6: Values rounded to two decimals"""
        out = self.run_program("12.345\n7\n")
        self.assertContains("Gross Pay: $86.42", out, "Gross rounding")
        self.assertContains("Net Pay:   $73.45", out, "Net rounding")