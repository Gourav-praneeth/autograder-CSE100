import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

BINARY = "./Lab6_Question1.out"
SOURCE = "Lab6_Question1.cpp"

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

    @weight(0.2)
    def test_valid_flow_march_range_and_stats(self):
        """Test Case 1""" #: Valid month + 7 consecutive days; header, highest/lowest, average.
        # Month: March; Dates: 10..16; Snow: 1,2,3,2,1,0,4  (avg=13/7=1.857142.. -> 1.86)
        input_data = "March\n10 1\n11 2\n12 3\n13 2\n14 1\n15 0\n16 4\n"
        out = self.run_program(input_data)

        self.assertContains("Snow report March 10 - 16", out, "Header range")
        self.assertContains("Highest snow fall is 4.00 on 16th", out, "Highest")
        self.assertContains("Lowest snow fall is 0.00 on 15th", out, "Lowest")
        self.assertContains("The average snow fall is 1.86", out, "Average")

    @weight(0.2)
    def test_invalid_month_three_attempts(self):
        """Test Case 2: 3 invalid months -> show error and exit."""
        input_data = "Marth\nJanuari\nBoo\n"
        out = self.run_program(input_data)

        self.assertContains("Invalid month!", out, "Invalid month message")
        self.assertContains("Exceeded the number of Invalid Attempts!", out, "Exceeded attempts exit")

    @weight(0.2)
    def test_negative_snowfall_then_correct(self):
        """Test Case 3: Negative snowfall rejected; then corrected; final report prints."""
        # Month: April (30 days). First entry attempts 20 -1 -> invalid snowfall.
        # Retry first entry as 20 2.25, then continue 21..26.
        input_data = (
            "April\n"
            "20 -1\n"      # invalid snowfall
            "20 2.25\n"    # corrected
            "21 0\n"
            "22 1\n"
            "23 0.5\n"
            "24 0\n"
            "25 0\n"
            "26 0\n"
        )
        out = self.run_program(input_data)

        self.assertContains("Invalid snowfall!", out, "Negative snowfall rejected")
        self.assertContains("Snow report April 20 - 26", out, "Header range present")
        # Spot-check that 2.25 shows in the table with two decimals
        self.assertContains("2.25", out, "Corrected snowfall present")

    @weight(0.2)
    def test_non_consecutive_dates_requires_retry(self):
        """Test Case 4: Non-consecutive date rejected; then corrected."""
        # Month: May (31 days). First entry 10 1.0, second entry mistakenly 12 1.0 (invalid),
        # then correct it with 11 1.0, then continue 12..16.
        input_data = (
            "May\n"
            "10 1.00\n"
            "12 1.00\n"   # invalid (non-consecutive)
            "11 1.00\n"   # corrected
            "12 1.00\n"
            "13 1.00\n"
            "14 1.00\n"
            "15 1.00\n"
            "16 1.00\n"
        )
        out = self.run_program(input_data)

        self.assertContains("Dates must be strictly consecutive!", out, "Non-consecutive rejection")
        self.assertContains("Snow report May 10 - 16", out, "Header range after correction")

    @weight(0.2)
    def test_date_larger_than_days(self):
        """Test Case 5: Date exceeds days in month rejected; then corrected."""
        # Month: April (30 days). First entry tries 31 1.0 -> invalid ("Date is larger...")
        # Then provide 23 0.5 (OK for first entry), and continue 24..29.
        input_data = (
            "April\n"
            "23 0.50\n"   
            "31 0.50\n"    # invalid (over days in month)
            "24 0.50\n"
            "25 0.50\n"
            "26 0.50\n"
            "27 0.50\n"
            "28 0.50\n"
            "29 0.50\n"
        )
        out = self.run_program(input_data)

        self.assertContains("Date is larger than number of days in the month!", out, "Over-days rejection")
        self.assertContains("Snow report April 23 - 29", out, "Header range after correction")

    @weight(0.2)
    def test_first_date_range_exceeds_month(self):
        """Test Case 6: First date too high to fit 7 entries -> 'Range exceeds...' then corrected."""
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
