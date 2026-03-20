import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

BINARY = "./Lab7_Question1.out"
SOURCE = "Lab7_Question1.cpp"

class TestSnowReport(unittest.TestCase):
    # ----------------- helpers -----------------
    def compile_program(self):
        proc = subprocess.Popen(
            ["g++", "-std=gnu++17", "-O2", "-o", BINARY, SOURCE],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = proc.communicate()
        return out.decode("utf-8"), err.decode("utf-8")

    def run_program(self, input_data: str) -> str:
        """Run compiled program and return raw stdout as a single string.

        We do NOT split lines because prompts often lack trailing newlines.
        """
        proc = subprocess.Popen(
            [f"./{BINARY}"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, _ = proc.communicate(input=input_data.encode("utf-8"))
        return out.decode("utf-8").strip()

    def assertContains(self, expected: str, output: str, title: str):
        """Substring check with a clear failure message showing a helpful snippet."""
        if expected not in output:
            nearest = difflib.get_close_matches(expected, output.splitlines(), n=1)
            found = nearest[0] if nearest else (output[:500] + ("..." if len(output) > 500 else ""))
            self.fail(f"{title} failed.\nExpected: {expected}\nFound:    {found}")

    # ----------------- tests -----------------

    @weight(0.2)
    def test_compile(self):
        """Compilation"""
        _, err = self.compile_program()
        self.assertEqual(err.strip(), "", msg="Compilation failed:\n" + err)

    @weight(0.1)
    def test_valid_flow_march_range_and_stats(self):
        """Test Case 1""" #: Valid month + 7 consecutive days; header, highest/lowest, average.
        # Month: March; Dates: 10..16; Snow: 1,2,3,2,1,0,4  (avg=13/7=1.857142.. -> 1.86)
        input_data = "March\n10 1\n11 2\n12 3\n13 2\n14 1\n15 0\n16 4\n"
        out = self.run_program(input_data)

        self.assertContains("Snow report March 10 - 16", out, "Header range")
        self.assertContains("Highest snow fall is 4.00 on 16th", out, "Highest")
        self.assertContains("Lowest snow fall is 0.00 on 15th", out, "Lowest")
        self.assertContains("The average snow fall is 1.86", out, "Average")

    @weight(0.1)
    def test_invalid_month_three_attempts(self):
        """Test Case 2"""
        input_data = "Marth\nJanuari\nBoo\n"
        out = self.run_program(input_data)

        self.assertContains("Invalid month!", out, "Invalid month message")
        self.assertContains("Exceeded the number of Invalid Attempts!", out, "Exceeded attempts exit")

    @weight(0.1)
    def test_all_invalid_snowfall_attempts(self):
        """Test Case 3""" #All invalid attempts (3 invalid snowfalls) -> error and exit.
        # Month: April. First date 20: user gives 3 invalid snowfall values -> program exits.
        input_data = (
            "April\n"
            "20 -1\n"   # invalid snowfall (attempt 1)
            "20 -2\n"   # invalid snowfall (attempt 2)
            "20 -5\n"   # invalid snowfall (attempt 3) -> exceed limit, exit
        )
        out = self.run_program(input_data)

        self.assertContains("Invalid snowfall!", out, "Invalid snowfall message")
        self.assertContains("Exceeded the number of Invalid Attempts!", out, "All failed attempts exit")

    @weight(0.1)
    def test_non_consecutive_dates_requires_retry(self):
        """Test Case 4"""
        input_data = (
            "May\n"
            "10 1.0\n"
            "12 1.0\n"    # invalid (non-consecutive)
            "11 -1.0\n"   # invalid (negative snowfall)
            "11 1.5\n"    # corrected
            "12 1.0\n"
            "13 1.0\n"
            "14 1.0\n"
            "15 1.0\n"
            "16 1.0\n"
        )
        out = self.run_program(input_data)

        self.assertContains("Dates must be strictly consecutive!", out, "Non-consecutive rejection")
        self.assertContains("Invalid snowfall!", out, "Negative snowfall rejected")
        self.assertContains("Snow report May 10 - 16", out, "Header range after correction")
        self.assertContains("1.5", out, "Corrected snowfall 1.5 present")

    @weight(0.1)
    def test_invalid_month_apr_then_april(self):
        """Test Case 5"""
        input_data = (
            "Apr\n"
            "April\n"
            "1 0.5\n"
            "2 0.5\n"
            "3 0.5\n"
            "4 0.5\n"
            "5 0.5\n"
            "6 0.5\n"
            "7 0.5\n"
        )
        out = self.run_program(input_data)

        self.assertContains("Invalid month!", out, "Invalid month (Apr) message")
        self.assertContains("Snow report April 1 - 7", out, "Header range after correct month")

    @weight(0.1)
    def test_first_date_range_exceeds_month(self):
        """Test Case 6"""
        # Month: February (28 days). First date 25 > 21 => invalid range for 7 days.
        # Correct to 21 and continue 22..27.
        input_data = (
            "February\n"
            "25 0.30\n"   # invalid (cannot fit 7 entries)
            "21 0.30\n"
            "22 0.30\n"
            "23 0.30\n"
            "24 0.30\n"
            "25 0.30\n"
            "26 0.30\n"
            "27 0.30\n"
        )
        out = self.run_program(input_data)

        self.assertContains("Range exceeds the days in the month!", out, "First-date range rejection")
        self.assertContains("Snow report February 21 - 27", out, "Header range after correction")