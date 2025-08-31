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
            ["g++", "-o", "Lab3_Question2.out", "Lab3_Question2.cpp"],
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
            ["./Lab3_Question2.out"],
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
    def test_case1(self):
        """Test Case 1"""
        output = self.run_student_program("CAT\nY")
        expected = "Pet Tag fee is $4.00"
        self.assertInOutput(expected, output, "Test Case 1")

    @weight(0.25)
    def test_case2(self):
        """Test Case 2"""
        output = self.run_student_program("cAt\ng\nh")
        expected = "Re-enter spayed or neutered (y/n):Invalid choice for Spayed or neutered!"
        self.assertInOutput(expected, output, "Test Case 2")
        
    @weight(0.25)
    def test_case3(self):
        """Test Case 3"""
        output = self.run_student_program("dog\nn")
        expected = "Pet Tag fee is $12.00"
        self.assertInOutput(expected, output, "Test Case 3")
        
    @weight(0.25)
    def test_case4(self):
        """Test Case 4"""
        output = self.run_student_program("Snake")
        expected = "Only cats and dogs need pet tags!"
        self.assertInOutput(expected, output, "Test Case 4")

