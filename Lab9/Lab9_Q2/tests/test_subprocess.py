import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

BINARY = "./Lab9_Question2.out"
SOURCE = "Lab9_Question2.cpp"

class TestSavingsProgram(unittest.TestCase):
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

    # --------------- tests ---------------

    @weight(0.2)
    def test_compile(self):
        """Compilation"""
        _, err = self.compile_program()
        self.assertEqual(err.strip(), "", msg="Compilation failed:\n" + err)

    @weight(0.1)
    def test_valid_flow_three_months(self):
        """Test Case 1"""
        #"""Test case 1: Valid 3-month, verify report totals & final balance."""
        # starting=1000, annual=0.12 (1%/mo)
        # M1: +200, -50  -> interest 10.75
        # M2: +100, -160 -> interest 11.31
        # M3: +0,   -100 -> interest 10.62
        # Totals: deposits=300.00, withdrawals=310.00, interest=32.68, final=1022.68
        input_data = (
            "1000\n"
            "0.12\n"
            "200\n50\n"   # month 1
            "100\n160\n"  # month 2
            "0\n100\n"    # month 3
        )
        out = self.run_program(input_data)

        self.assertContains("Savings Account Report", out, "Report header")
        self.assertContains("Starting Balance: $1000.00", out, "Start balance")
        self.assertContains("Total Deposits:   $300.00", out, "Total deposits")
        self.assertContains("Total Withdrawals:$310.00", out, "Total withdrawals")
        self.assertContains("Total Interest:   $32.68", out, "Total interest")
        self.assertContains("Final Balance:    $1022.68", out, "Final balance")

    @weight(0.1)
    def test_invalid_starting_balance_exits(self):
        """Test Case 2"""
        #"""Test case 2: Starting balance invalid 3 times"""
        input_data = (
            "-1\n"
            "-7\n"
            "-5\n"
        )
        out = self.run_program(input_data)
        self.assertContains("Invalid input! Value should be non-negative.", out, "Invalid start msgs")
        self.assertContains("Too many invalid attempts!", out, "Too many invalid attempts exit")

    @weight(0.1)
    def test_invalid_annual_rate_exits(self):
        """Test Case 3"""
        #"""Test Case 3: Annual rate invalid 3 times."""
        input_data = (
            "1000\n"
            "-0.1\n"
            "-0.7\n"
            "-0.5\n"
        )
        out = self.run_program(input_data)
        self.assertContains("Invalid input! Value should be non-negative.", out, "Invalid rate msgs")
        self.assertContains("Too many invalid attempts!", out, "Too many invalid attempts exit")

    @weight(0.1)
    def test_deposit_invalid_then_valid(self):
        """Test Case 4"""
        #"""Test Case 4: Deposit negative then corrected; verify final report numbers."""
        # starting=500, annual=0.06 (0.5%/mo)
        # M1: deposit -10 (invalid), then 100; withdrawal 50 -> interest ≈ 2.63
        # M2: +0, -0 -> interest ≈ 2.76
        # M3: +0, -0 -> interest ≈ 2.78
        # Totals: deposits=100.00, withdrawals=50.00, interest=8.17, final≈558.17
        input_data = (
            "500\n"
            "0.06\n"
            "-10\n"    # invalid deposit
            "100\n"    # corrected deposit
            "50\n"     # withdrawal
            "0\n0\n"   # month 2
            "0\n0\n"   # month 3
        )
        out = self.run_program(input_data)

        self.assertContains("Invalid input! Value should be non-negative.", out, "Deposit invalid message")
        self.assertContains("Total Deposits:   $100.00", out, "Deposits total")
        self.assertContains("Total Withdrawals:$50.00", out, "Withdrawals total")
        self.assertContains("Total Interest:   $8.17", out, "Interest total")
        self.assertContains("Final Balance:    $558.17", out, "Final balance")

    @weight(0.1)
    def test_withdrawal_exceeds_then_valid(self):
        """Test Case 5"""
        #"""Test Case 5: Mixed invalid/valid corrections across rate, deposits, withdrawals."""
        # starting=1050
        # annual=-1 (invalid), then 0.15 (valid)
        # M1: deposit 50, withdrawal -50 (invalid), then 50
        # M2: deposit 1000, withdrawal 125
        # M3: deposit -670 (invalid), then 500; withdrawal 670
        # Totals: deposits=1550.00, withdrawals=845.00, interest=55.28, final=1810.28
        input_data = (
            "1050\n"
            "-1\n"      # invalid annual rate
            "0.15\n"    # corrected annual rate
            "50\n"
            "-50\n"     # invalid withdrawal
            "50\n"      # valid withdrawal
            "1000\n"
            "125\n"
            "-670\n"    # invalid deposit
            "500\n"     # valid deposit
            "670\n"
        )
        out = self.run_program(input_data)

        self.assertContains("Invalid input! Value should be non-negative.", out, "Invalid non-negative message")
        self.assertContains("Withdrawal cannot be negative or exceed current balance!", out, "Withdrawal bound message")
        self.assertContains("Total Deposits:   $1550.00", out, "Deposits total")
        self.assertContains("Total Withdrawals:$845.00", out, "Withdrawals total")
        self.assertContains("Total Interest:   $55.28", out, "Interest total")
        self.assertContains("Final Balance:    $1810.28", out, "Final balance")

    @weight(0.1)
    def test_withdrawal_three_invalids_exit(self):
        """Test Case 6"""
        #"""Test Case 6: Withdrawal invalid 3 times, exit 'Too many invalid attempts!'."""
        # starting=100, annual=0.12
        # M1: deposit 0; then withdrawal attempts 200 (exceed), -5 (neg), 1000 (exceed) -> exit
        input_data = (
            "100\n"
            "0.12\n"
            "0\n"
            "200\n"
            "-5\n"
            "1000\n"
        )
        out = self.run_program(input_data)

        self.assertContains("Withdrawal cannot be negative or exceed current balance!", out, "Withdrawal invalid msgs")
        self.assertContains("Too many invalid attempts!", out, "Too many invalid attempts exit")
