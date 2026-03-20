import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

BINARY = "./Lab8_Question1.out"
SOURCE = "Lab8_Question1.cpp"


class TestStringSelectionSort(unittest.TestCase):
    def compile_program(self):
        proc = subprocess.Popen(
            ["g++", "-std=gnu++17", "-O2", "-o", BINARY, SOURCE],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = proc.communicate()
        return out.decode("utf-8"), err.decode("utf-8")

    def run_program(self, input_data: str) -> str:
        proc = subprocess.Popen(
            [f"./{BINARY}"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, _ = proc.communicate(input=input_data.encode("utf-8"))
        return out.decode("utf-8").strip()

    def assertContains(self, expected: str, output: str, title: str):
        if expected not in output:
            nearest = difflib.get_close_matches(expected, output.splitlines(), n=1)
            found = nearest[0] if nearest else (output[:500] + ("..." if len(output) > 500 else ""))
            self.fail(f"{title} failed.\nExpected: {expected}\nFound:    {found}")

    def assertBefore(self, first: str, second: str, output: str, title: str):
        pos1 = output.find(first)
        pos2 = output.find(second)
        self.assertGreaterEqual(pos1, 0, f"{title}: '{first}' not found in output")
        self.assertGreaterEqual(pos2, 0, f"{title}: '{second}' not found in output")
        self.assertLess(pos1, pos2, f"{title}: '{first}' should appear before '{second}'")

    @weight(0.2)
    def test_compile(self):
        """Compilation (0.2)"""
        _, err = self.compile_program()
        self.assertEqual(err.strip(), "", msg="Compilation failed:\n" + err)

    @weight(0.1)
    def test_valid_size_and_names(self):
        """Test Case 1"""
        #"""Test 1: n=-1,0,4 then 4 valid names -> sorted output."""
        input_data = (
            "-1\n0\n4\n"
            "Collins, Bill\n"
            "Smith, Bart\n"
            "Michalski, Joe\n"
            "Griffin, Jim\n"
        )
        out = self.run_program(input_data)
        self.assertContains("Sorted names:", out, "Sorted header present")
        # Expected sorted: Collins, Bill; Griffin, Jim; Michalski, Joe; Smith, Bart
        self.assertBefore("Collins, Bill", "Griffin, Jim", out, "Collins before Griffin")
        self.assertBefore("Griffin, Jim", "Michalski, Joe", out, "Griffin before Michalski")
        self.assertBefore("Michalski, Joe", "Smith, Bart", out, "Michalski before Smith")

    @weight(0.1)
    def test_invalid_names_three_attempts_same_person(self):
        """Test Case 2"""
        #"""Test 2: n=4 then three invalid names -> exit."""
        input_data = (
            "4\n"
            "JohnsonJill\n"
            "Johnson,Jill\n"
            "Johnson Jill\n"
        )
        out = self.run_program(input_data)
        self.assertContains("Invalid name! Attempt", out, "Invalid name messages")
        self.assertContains("Too many Invalid Attempts!", out, "Exit after 3 invalid names")
        self.assertNotIn("Sorted names:", out, "Should not print sorted names on failure")

    @weight(0.1)
    def test_invalid_sizes_only(self):
        """Test Case 3"""
        #"""Test 3: n=-4,0,-2 -> exit after 3 invalid sizes."""
        input_data = "-4\n0\n-2\n"
        out = self.run_program(input_data)
        self.assertContains("Invalid number! Attempt", out, "Invalid number message")
        self.assertContains("Too many Invalid Attempts!", out, "Exit after invalid sizes")
        self.assertNotIn("Enter name 1", out, "Should not prompt for names")

    @weight(0.1)
    def test_valid_six_names(self):
        """Test Case 4"""
        #"""Test 4: n=6 with six valid names -> sorted correctly."""
        input_data = (
            "6\n"
            "Allison, Jeff\n"
            "Moreno, Juan\n"
            "Wolfe, Bill\n"
            "Whitman, Jean\n"
            "Moretti, Bella\n"
            "Allison, Bart\n"
        )
        out = self.run_program(input_data)
        self.assertContains("Sorted names:", out, "Sorted header present")
        # Check a few key orderings in sorted result
        self.assertBefore("Allison, Bart", "Allison, Jeff", out, "Allison Bart before Allison Jeff")
        self.assertBefore("Moreno, Juan", "Moretti, Bella", out, "Moreno before Moretti")
        self.assertBefore("Whitman, Jean", "Wolfe, Bill", out, "Whitman before Wolfe")

    @weight(0.1)
    def test_n8_with_names(self):
        """Test Case 5"""
        #"""Test 5: n=8, a mix of names including ones with multiple parts."""
        input_data = (
            "8\n"
            "Sanchez, Manny\n"
            "Rubin, Sarah\n"
            "Mathew, Tyrone\n"
            "Taylor, Smith Tyrone\n"
            "Wu, Eric\n"
            "Patel, Renee\n"
            "Harrison, Rose\n"
            "Smith, Cathy\n"
        )
        out = self.run_program(input_data)
        # Should complete and print sorted list
        self.assertContains("Sorted names:", out, "Sorted header present")
        self.assertContains("Sanchez, Manny", out, "Sanchez present")
        self.assertContains("Smith, Cathy", out, "Smith Cathy present")

    @weight(0.1)
    def test_three_invalid_names_across_people(self):
        """Test Case 6"""
        #"""Test 6: n=3; three invalid names across different people -> exit before final correct name."""
        input_data = (
            "3\n"
            "Wu Eric\n"           # invalid (no comma)
            "Wu, Eric\n"          # valid
            "Harrison,Rose\n"     # invalid (no space)
            "Harrison, Rose\n"    # valid
            "ConroyPat\n"         # invalid (no comma or space) -> 3rd invalid overall, exit
        )
        out = self.run_program(input_data)
        self.assertContains("Invalid name! Attempt", out, "Invalid name messages")
        self.assertContains("Too many Invalid Attempts!", out, "Exit after 3 invalid names total")
        self.assertNotIn("Conroy, Pat", out, "Should not accept final corrected name")