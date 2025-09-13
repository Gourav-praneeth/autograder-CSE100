import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import re

BINARY = "./Lab5_Question1.out"
SOURCE = "Lab5_Question1.cpp"   # <-- change to your actual filename if needed

class TestBeverageSurvey(unittest.TestCase):
    # ---------- helpers ----------
    def compile_program(self):
        proc = subprocess.Popen(
            ["g++", "-std=c++17", "-O2", "-o", BINARY, SOURCE],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = proc.communicate()
        return out.decode("utf-8"), err.decode("utf-8")

    def run_program(self, input_data: str) -> str:
        proc = subprocess.Popen(
            [BINARY],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, _ = proc.communicate(input=input_data.encode("utf-8"))
        return out.decode("utf-8").strip()

    def assertContains(self, expected: str, output: str, title: str):
        if expected not in output:
            self.fail(f"{title} failed.\nExpected: {expected}\nFound:    {output}")

    def find_line_starting_with(self, prefix: str, output: str):
        for line in output.splitlines():
            if line.startswith(prefix):
                return line
        return None

    # ---------- tests ----------
    @weight(0.2)
    def test_Compile(self):
        """Clean Compile (0.2)"""
        _, err = self.compile_program()
        self.assertEqual(err.strip(), "", msg="Compilation failed:\n" + err)

    @weight(0.1)
    def test_base_flow_each_once(self):
        """Test Case 1""" # (0.1): votes 1,2,3,4 then -1 -> each = 1, total = 4
        # 1 (coffee), 2 (tea), 3 (coke), 4 (orange), exit
        output = self.run_program("1\n2\n3\n4\n-1\n")

        # Totals
        self.assertContains("The total number of people surveyed is 4.", output, "Total surveyed")

        # Table header present
        self.assertContains("Beverage", output, "Table header")
        self.assertContains("Number of Votes", output, "Table header")

        # Each line: we check the line that starts with the label and ends with the expected count
        for label, count in [("Coffee", 1), ("Tea", 1), ("Coke", 1), ("Orange Juice", 1)]:
            line = self.find_line_starting_with(label, output)
            self.assertIsNotNone(line, msg=f"Missing row for '{label}'. Full output:\n{output}")
            # allow spaces due to setw
            self.assertRegex(line, rf"^{re.escape(label)}\s+{count}\s*$",
                             msg=f"Wrong count for '{label}'.\nExpected: {count}\nFound line: {line}")

    @weight(0.1)
    def test_invalid_attempts_then_valid(self):
        """Test Case 2""" #(0.1): three invalids -> message; then a valid vote; exit
        # Person #1: 3 invalid choices, triggers message; Person #2: valid '2' then exit
        output = self.run_program("9\n0\n7\n2\n-1\n")

        # Check the message about too many invalid attempts
        self.assertContains("Too many invalid attempts. Moving to next person.", output, "Invalid attempts message")

        # Only one valid vote (tea) counted
        self.assertContains("The total number of people surveyed is 1.", output, "Total surveyed after invalids")

        tea_line = self.find_line_starting_with("Tea", output)
        self.assertIsNotNone(tea_line, "Missing row for 'Tea'")
        self.assertRegex(tea_line, r"^Tea\s+1\s*$", msg=f"Tea count incorrect.\nFound: {tea_line}")

        # Others should be 0
        for label in ["Coffee", "Coke", "Orange Juice"]:
            line = self.find_line_starting_with(label, output)
            self.assertIsNotNone(line, f"Missing row for '{label}'")
            self.assertRegex(line, rf"^{re.escape(label)}\s+0\s*$",
                             msg=f"{label} count should be 0.\nFound: {line}")

    @weight(0.1)
    def test_immediate_exit(self):
        """Test Case 3""" # (0.1): -1 immediately -> totals all zero
        output = self.run_program("-1\n")

        self.assertContains("The total number of people surveyed is 0.", output, "Total surveyed")
        for label in ["Coffee", "Tea", "Coke", "Orange Juice"]:
            line = self.find_line_starting_with(label, output)
            self.assertIsNotNone(line, f"Missing row for '{label}'")
            self.assertRegex(line, rf"^{re.escape(label)}\s+0\s*$",
                             msg=f"{label} count should be 0.\nFound: {line}")

    @weight(0.1)
    def test_aggregation_many_votes(self):
        """Test Case 4""" #(0.1): 1,1,4,3,2,4 then -1 => Coffee=2, Tea=1, Coke=1, Orange=2; total=6
        output = self.run_program("1\n1\n4\n3\n2\n4\n-1\n")

        self.assertContains("The total number of people surveyed is 6.", output, "Total surveyed")

        expected_counts = {
            "Coffee": 2,
            "Tea": 1,
            "Coke": 1,
            "Orange Juice": 2
        }
        for label, count in expected_counts.items():
            line = self.find_line_starting_with(label, output)
            self.assertIsNotNone(line, f"Missing row for '{label}'")
            self.assertRegex(line, rf"^{re.escape(label)}\s+{count}\s*$",
                             msg=f"{label} count incorrect.\nExpected: {count}\nFound: {line}")
