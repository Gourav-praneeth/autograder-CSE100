import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

class TestCppProgram(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0.7)
    def test_Compile(self):
        """Clean Compile: Program compiles without errors"""
        compile_process = subprocess.Popen(["g++", "-o", "test2.out", "Lab1_Q2.cpp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, compile_errors = compile_process.communicate()
        compile_process.kill()

        self.assertEqual(
            compile_errors.decode('utf-8').strip(), "",
            msg="Compilation failed. Please check your C++ syntax.\nErrors:\n" + compile_errors.decode('utf-8')
        )
        compile_process.terminate()

    def run_student_program(self):
        """Helper method to run the compiled program and get output lines"""
        test = subprocess.Popen(["./test2.out"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = test.stdout.read().strip().decode('utf-8').splitlines()
        test.kill()
        test.terminate()
        return output

    def assertInOutput(self, expected, output, section=""):
        """Helper to provide better error messages"""
        if expected not in output:
            # Try to suggest the closest match
            closest = difflib.get_close_matches(expected, output, n=1)
            suggestion = f"But got:  '{closest[0]}'" if closest else ""
            self.fail(f"{section} check failed.\nExpected: '{expected}'\n{suggestion}")

    @weight(0.2)
    def test_Output_Header(self):
        """Check if header is displayed correctly"""
        output = self.run_student_program()
        self.assertInOutput("******************************", output, "Header border")
        self.assertInOutput("\tCSE 100", output, "Header title")
        self.assertInOutput(" Welcome to C++ Programming", output, "Header message")

    @weight(0.1)
    def test_Output_Arithmetic_Sum(self):
        """Check if Sum is displayed correctly"""
        output = self.run_student_program()
        expected = "1. The sum of 2 and 3\t\t\t= 5"
        self.assertInOutput(expected, output, "Sum expression")

    @weight(0.1)
    def test_Output_Arithmetic_Product(self):
        """Check if Product is displayed correctly"""
        output = self.run_student_program()
        expected = "2. The product of 5 and 6\t\t= 30"
        self.assertInOutput(expected, output, "Product expression")

    @weight(0.1)
    def test_Output_Arithmetic_Quotient(self):
        """Check if Quotient is displayed correctly"""
        output = self.run_student_program()
        expected = "3. 15 divided by 7 gives quotient\t= 2"
        self.assertInOutput(expected, output, "Quotient expression")

    @weight(0.1)
    def test_Output_Arithmetic_Remainder(self):
        """Check if Remainder is displayed correctly"""
        output = self.run_student_program()
        expected = "4. 15 divided by 4 has remainder\t= 3"
        self.assertInOutput(expected, output, "Remainder expression")

    @weight(0.2)
    def test_Output_Ending(self):
        """Check if ending lines are displayed correctly"""
        output = self.run_student_program()
        # Since ending has 2 lines, check separately
        self.assertInOutput("\tThis is end of my first Program", output, "Ending line 1")
        self.assertInOutput("\t\tThank you!", output, "Ending line 2")
