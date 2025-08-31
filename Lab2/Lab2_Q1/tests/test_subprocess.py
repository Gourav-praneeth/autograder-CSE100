import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

class TestIdealWeightProgram(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0.2)
    def test_Compile(self):
        """Clean Compile: Program compiles without errors"""
        compile_process = subprocess.Popen(
            ["g++", "-o", "Lab2_Q1.out", "Lab2_Question1.cpp"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        _, compile_errors = compile_process.communicate()
        compile_process.kill()

        self.assertEqual(
            compile_errors.decode("utf-8").strip(), "",
            msg="Compilation failed. Please check your C++ syntax.\nErrors:\n" + compile_errors.decode("utf-8")
        )
        compile_process.terminate()

    def run_student_program(self, input_data):
        """Helper method to run the compiled program and capture output lines"""
        test = subprocess.Popen(
            ["./Lab2_Question1.out"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, _ = test.communicate(input=input_data.encode("utf-8"))
        test.kill()
        test.terminate()
        return output.decode("utf-8").strip().splitlines()

    def assertInOutput(self, expected, output, section=""):
        """Helper to provide clearer error messages with suggestions"""
        if expected not in output:
            closest = difflib.get_close_matches(expected, output, n=1)
            suggestion = f"\nFound: '{closest[0]}'" if closest else ""
            self.fail(f"{section} check failed.\nExpected: '{expected}'{suggestion}")



    @weight(0.25)
    def test_WelcomeMessage(self):
        """Test Case 1"""
        output = self.run_student_program()
        self.assertInOutput("Welcome to Ideal Weight Calculation Program", output, "Welcome message")

    @weight(0.25)
    def test_InputPrompt(self):
        """Test Case 2"""
        output = self.run_student_program("5 3")
        expected = "Please enter your height, feet followed by inches (eg; 5 3): "
        self.assertInOutput(expected, output, "Input prompt")

    @weight(0.125)
    def test_MaleIdealWeight(self):
        """Test Case 3A: Male"""
        output = self.run_student_program("5 3")
        expected = "If you are a male, your ideal weight should be 124 pounds."
        self.assertInOutput(expected, output, "Male ideal weight")

    @weight(0.125)
    def test_FemaleIdealWeight(self):
        """Test Case 3B: Female"""
        output = self.run_student_program("5 3")
        expected = "If you are a female, your ideal weight should be 115 pounds."
        self.assertInOutput(expected, output, "Female ideal weight")