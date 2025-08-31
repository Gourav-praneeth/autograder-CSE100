import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

class TestBrownieProgram(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0.2)
    def test_Compile(self):
        """Clean Compile: Program compiles without errors"""
        compile_process = subprocess.Popen(
            ["g++", "-o", "Lab2_Question2.out", "Lab2_Question2.cpp"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        _, compile_errors = compile_process.communicate()
        compile_process.kill()

        self.assertEqual(
            compile_errors.decode("utf-8").strip(), "",
            msg="Compilation failed. Errors:\n" + compile_errors.decode("utf-8")
        )
        compile_process.terminate()

    def run_student_program(self, input_data):
        """Run student program and return full output as string"""
        test = subprocess.Popen(
            ["./Lab2_Question2.out"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, _ = test.communicate(input=input_data.encode("utf-8"))
        test.kill()
        test.terminate()
        return output.decode("utf-8")

    def assertInOutput(self, expected, output, section=""):
        """Check if expected string is in output, else show closest match"""
        if expected not in output:
            closest = difflib.get_close_matches(expected, output.split(), n=1)
            wrong = closest[0] if closest else output
            self.fail(
                f"{section} check failed.\nExpected: '{expected}'\nFound:    '{wrong}'"
            )

    # ====== Test Cases ======
    @weight(0.125)
    def test_LengthPrompt(self):
        """Test Case 1: Length Prompt"""
        output = self.run_student_program("8\n12\n")
        expected = "Enter the length of the baking pan (in inches): "
        self.assertInOutput(expected, output, "Length prompt")

    @weight(0.125)
    def test_WidthPrompt(self):
        """Test Case 2: Width Prompt"""
        output = self.run_student_program("8\n12\n")
        expected = "Enter the width of the baking pan (in inches): "
        self.assertInOutput(expected, output, "Width prompt")

    @weight(0.25)
    def test_BrownieCalculation(self):
        """Test Case 3: Brownie Calculation"""
        output = self.run_student_program("8\n12\n")
        expected = "A 8 X 12 inch pan can hold 96 small brownies or 24 large brownies."
        self.assertInOutput(expected, output, "Brownie calculation")

    # additional test case
    @weight(0.25)
    def test_BrownieCalculation(self):
        """Test Case 3: Brownie Calculation"""
        output = self.run_student_program("7\n11\n")
        expected = "A 7 X 11 inch pan can hold 77 small brownies or 19.25 large brownies."
        self.assertInOutput(expected, output, "Brownie calculation")
