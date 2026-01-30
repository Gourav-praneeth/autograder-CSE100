import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib
import re

class TestCppProgram(unittest.TestCase):
    def setUp(self):
        pass

    def read_source_code(self):
        """Helper method to read the student's source code"""
        with open("Lab1_Question2.cpp", "r") as f:
            return f.read()

    @weight(0.3)
    def test_Compile(self):
        """Clean Compile: Program compiles without errors"""
        compile_process = subprocess.Popen(["g++", "-o", "test2.out", "Lab1_Question2.cpp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

    @weight(0.1)
    def test_Output_Header(self):
        """Check if header is displayed correctly"""
        output = self.run_student_program()
        self.assertInOutput("******************************", output, "Header border")
        self.assertInOutput("\tCSE 100", output, "Header title")
        self.assertInOutput(" Welcome to C++ Programming", output, "Header message")

    @weight(0.1)
    def test_Arithmetic_Addition_Used(self):
        """Check if addition operator (+) is used correctly in code"""
        source = self.read_source_code()
        # Check for addition operation: 2 + 3
        pattern = r'2\s*\+\s*3'
        self.assertIsNotNone(
            re.search(pattern, source),
            msg="Addition operator (+) not found. You must use '2 + 3' to compute the sum."
        )

    @weight(0.1)
    def test_Arithmetic_Multiplication_Used(self):
        """Check if multiplication operator (*) is used correctly in code"""
        source = self.read_source_code()
        # Check for multiplication operation: 5 * 6
        pattern = r'5\s*\*\s*6'
        self.assertIsNotNone(
            re.search(pattern, source),
            msg="Multiplication operator (*) not found. You must use '5 * 6' to compute the product."
        )

    @weight(0.1)
    def test_Arithmetic_Division_Used(self):
        """Check if division operator (/) is used correctly in code"""
        source = self.read_source_code()
        # Check for division operation: 15 / 7
        pattern = r'15\s*/\s*7'
        self.assertIsNotNone(
            re.search(pattern, source),
            msg="Division operator (/) not found. You must use '15 / 7' to compute the quotient."
        )

    @weight(0.1)
    def test_Arithmetic_Modulus_Used(self):
        """Check if modulus operator (%) is used correctly in code"""
        source = self.read_source_code()
        # Check for modulus operation: 15 % 4
        pattern = r'15\s*%\s*4'
        self.assertIsNotNone(
            re.search(pattern, source),
            msg="Modulus operator (%) not found. You must use '15 % 4' to compute the remainder."
        )

    @weight(0.1)
    def test_Output_Arithmetic_Results(self):
        """Check if arithmetic results are displayed correctly"""
        output = self.run_student_program()
        # Check that output contains the correct computed values
        self.assertInOutput("1. The sum of 2 and 3\t\t\t= 5", output, "Sum expression")
        self.assertInOutput("2. The product of 5 and 6\t\t= 30", output, "Product expression")
        self.assertInOutput("3. 15 divided by 7 gives quotient\t= 2", output, "Quotient expression")
        self.assertInOutput("4. 15 divided by 4 has remainder\t= 3", output, "Remainder expression")

    @weight(0.1)
    def test_Output_Ending(self):
        """Check if ending lines are displayed correctly"""
        output = self.run_student_program()
        # Since ending has 2 lines, check separately
        self.assertInOutput("\tThis is end of my first Program", output, "Ending line 1")
        self.assertInOutput("\t\tThank you!", output, "Ending line 2")
