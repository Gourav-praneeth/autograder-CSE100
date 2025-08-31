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
            ["g++", "-o", "Lab3_Question1.out", "Lab3_Question1.cpp"],
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

    def run_student_program(self, input_data="5 3"):
        """Helper method to run the compiled program and capture output lines"""
        test = subprocess.Popen(
            ["./Lab3_Question1.out"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, _ = test.communicate(input=input_data.encode("utf-8"))
        test.kill()
        test.terminate()
        return output.decode("utf-8").splitlines()

    def assertInOutput(self, expected, output, section=""):
        """Helper to provide clearer error messages with suggestions"""
        if expected not in output:
            closest = difflib.get_close_matches(expected, output, n=1)
            suggestion = f"\nFound: '{closest[0]}'" if closest else ""
            self.fail(f"{section} check failed.\nExpected: '{expected}'{suggestion}")

    # ====== Test Cases ======
    @weight(0.25)
    def test_case1_square(self):
        """Test Case 1: Square"""
        output = self.run_student_program("1\n4.5")
        expected = "Area of the Square is 20.25"
        self.assertInOutput(expected, output, "Test Case 1")

    @weight(0.25)
    def test_case2_circle(self):
        """Test Case 2: Circle"""
        output = self.run_student_program("2\n3.0")
        expected = "Area of the Circle is 28.2743"
        self.assertInOutput(expected, output, "Test Case 2")
        
    @weight(0.25)
    def test_case3_triangle(self):
        """Test Case 3: Triangle"""
        output = self.run_student_program("3\n5.0")
        expected = "Area of the Right Triangle is 12.5"
        self.assertInOutput(expected, output, "Test Case 3")
        
    @weight(0.25)
    def test_case4_invalid(self):
        """Test Case 4: Invalid Choice"""
        output = self.run_student_program("0")
        expected = "Invalid Choice of Object!"
        self.assertInOutput(expected, output, "Test Case 4")

