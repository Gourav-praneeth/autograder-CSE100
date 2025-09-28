import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

BINARY = "./Lab7_Question1.out"
SOURCE = "Lab7_Question1.cpp"

class TestGradeCalculator(unittest.TestCase):
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
        """Test Case 0: Code runs without any errors"""
        _, err = self.compile_program()
        self.assertEqual(err.strip(), "", msg="Compilation failed:\n" + err)

    @weight(0.2)
    def test_valid_flow_B_grade(self):
        """Test Case 1: Valid inputs"""
        # Test1=80, Test2=90, HW=70 → 32 + 36 + 14 = 82.00 → B correct final score & letter B
        out = self.run_program("80\n90\n70\n")
        self.assertContains("Final Score: 82.00", out, "Final score")
        self.assertContains("Letter Grade: B", out, "Letter grade")

    @weight(0.2)
    def test_all_hundreds_A_grade(self):
        """Test Case 2: Checking Grade Letter A"""
        out = self.run_program("100\n100\n100\n")
        self.assertContains("Final Score: 100.00", out, "Final score 100")
        self.assertContains("Letter Grade: A", out, "Letter grade A")

    @weight(0.2)
    def test_boundary_just_below_A(self):
        """Test Case 3: Edge Case"""
        # Boundary near A — ensure 89.99 prints and grade is B
        # Choose values to produce exactly 89.99:
        # t1=90, t2=90, hw=89.95 → 36 + 36 + 17.99 = 89.99
        out = self.run_program("90\n90\n89.95\n")
        self.assertContains("Final Score: 89.99", out, "Boundary score 89.99")
        self.assertContains("Letter Grade: B", out, "Letter grade B just below A")

    @weight(0.2)
    def test_invalid_then_corrected_input(self):
        """Test Case 4: Enter's one invalid score"""
        # Test1: -5 (invalid) then 80; Test2: 70; HW: 60 → 72.00 → C
        out = self.run_program("-5\n80\n70\n60\n")
        self.assertContains("Invalid input! Score must be between 0 and 100.", out, "Invalid message shown")
        self.assertContains("Final Score: 72.00", out, "Final score 72")
        self.assertContains("Letter Grade: C", out, "Letter grade C")

    @weight(0.2)
    def test_three_invalid_attempts_exit(self):
        """Test Case 5: Invalid Attempts Check"""
        # Three invalid attempts for Test 1 → exit with message, no final report
        out = self.run_program("-1\nabc\n105\n")
        self.assertContains("Invalid input! Score must be between 0 and 100.", out, "Invalid messages present")
        self.assertContains("Too many invalid attempts!", out, "Too many attempts message")
        self.assertNotContains("Final Score:", out, "No report printed after exit")

    @weight(0.2)
    def test_boundary_D_grade_exact_60(self):
        """Test Case 6: Boundary Grade Check"""
        # t1=t2=hw=60 → 24 + 24 + 12 = 60.00 → D
        out = self.run_program("60\n60\n60\n")
        self.assertContains("Final Score: 60.00", out, "Boundary final score 60.00")
        self.assertContains("Letter Grade: D", out, "Letter grade D at boundary")
