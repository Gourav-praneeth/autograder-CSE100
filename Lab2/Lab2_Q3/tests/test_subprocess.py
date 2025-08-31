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
            ["g++", "-o", "Lab2_Q3.out", "Lab2_Question3.cpp"],
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
            ["./Lab2_Question3.out"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, _ = test.communicate(input=input_data.encode("utf-8"))
        test.kill()
        test.terminate()
        return output.decode("utf-8")

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
        output = self.run_student_program("Soumya\nGourav\nBread\n101\ncute\ngreen\ncat")
        expected = "Dear Instructor Soumya,\n\nI am sorry that I am unable to turn in my homework at this time. First, I ate a rotten Bread, which made me turn green and extremely ill. I come down with a fever of 101. Next, my cute pet cat must have smelled the remains of the Bread on my homework, because he ate it. I am currently rewriting my homework and hope you will accept it here.\n\nSincerely,\nGourav"
        self.assertInOutput(expected, output, "Test Case 1")

    @weight(0.25)
    def test_case2(self):
        """Test Case 2"""
        output = self.run_student_program("Lee\nTom\nApple\n105\nbeautiful\nred\ndog")
        expected = "Dear Instructor Lee,\n\nI am sorry that I am unable to turn in my homework at this time. First, I ate a rotten Apple, which made me turn red and extremely ill. I come down with a fever of 105. Next, my beautiful pet dog must have smelled the remains of the Apple on my homework, because he ate it. I am currently rewriting my homework and hope you will accept it here.\n\nSincerely,\nTom"
        self.assertInOutput(expected, output, "Test Case 2")

