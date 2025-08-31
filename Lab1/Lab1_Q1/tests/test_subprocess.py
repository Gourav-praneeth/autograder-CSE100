import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess

class TestStudentInfo(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0.9)
    def test_Compile(self):
        """Clean Compile: Program compiles without errors"""

        # Attempt to compile the student's code using make or g++
        compile_process = subprocess.Popen(["g++", "-o", "test1.out", "Lab1_Q1.cpp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, compile_errors = compile_process.communicate()
        compile_process.kill()

        # Fail the test if there are compilation errors
        self.assertEqual(compile_errors.decode('utf-8').strip(), "", msg="Compilation errors:\n" + compile_errors.decode('utf-8'))
        compile_process.terminate()

    def run_student_program(self):
        """Helper method to run the compiled program and get output lines"""
        test = subprocess.Popen(["./test1.out"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = test.stdout.read().strip().decode('utf-8').splitlines()
        test.kill()
        test.terminate()
        return output

    @weight(0.2)
    def test_Name(self):
        """Check if Name is displayed correctly"""
        output = self.run_student_program()
        expected_name = "John, Doe"
        self.assertIn(expected_name, output, msg=f"Expected: {expected_name}\nFound: {output}")

    @weight(0.2)
    def test_Age(self):
        """Check if Age is displayed correctly"""
        output = self.run_student_program()
        expected_age = "27"
        self.assertIn(expected_age, output, msg=f"Expected: {expected_age}\nFound: {output}")

    @weight(0.2)
    def test_AcademicLevel(self):
        """Check if Academic Level is displayed correctly"""
        output = self.run_student_program()
        expected_level = "Freshman"
        self.assertIn(expected_level, output, msg=f"Expected: {expected_level}\nFound: {output}")
