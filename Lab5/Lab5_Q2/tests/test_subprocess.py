import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

class TestFallingDistanceProgram(unittest.TestCase):

    def setUp(self):
        pass

    @weight(0.2)
    def test_Compile(self):
        """Program compiles without errors"""
        compile_process = subprocess.Popen(
            ["g++", "-o", "Lab5_Q2.out", "Lab5_Question2.cpp"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        _, compile_errors = compile_process.communicate()
        compile_process.kill()
        self.assertEqual(
            compile_errors.decode("utf-8").strip(), "",
            msg="Compilation failed.\nErrors:\n" + compile_errors.decode("utf-8")
        )
        compile_process.terminate()

    def run_student_program(self, input_data):
        """Helper: run compiled program with given input"""
        test = subprocess.Popen(
            ["./Lab5_Q2.out"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, _ = test.communicate(input=input_data.encode("utf-8"))
        test.kill()
        test.terminate()
        return output.decode("utf-8").strip()

    def assertInOutput(self, expected, output, section=""):
        """Check if expected substring exists in output; otherwise show nearby match"""
        if expected not in output:
            closest = difflib.get_close_matches(expected, output.splitlines(), n=1)
            suggestion = f"\nFound: '{closest[0]}'" if closest else ""
            self.fail(f"{section} check failed.\nExpected: '{expected}'{suggestion}")

    # ====== Test Cases ======

    @weight(0.1)
    def test_case1_combination_all_chars(self):
        """Test Case 1: String with combination of all chars"""
        # "Hello! Welcome to CSE 100#"
        output = self.run_student_program("Hello! Welcome to CSE 100#")
        self.assertInOutput("Total Characters   : 25", output, "Total count")
        self.assertInOutput("Uppercase Letters  : 5", output, "Uppercase")
        self.assertInOutput("Lowercase Letters  : 12", output, "Lowercase")
        self.assertInOutput("Digits             : 3", output, "Digits")

    @weight(0.1)
    def test_case2_only_special_chars(self):
        """Test Case 2: String with only special characters"""
        # "@$%$&?/#"
        output = self.run_student_program("@$%$&?/#")
        self.assertInOutput("Total Characters   : 7", output, "Total count")
        self.assertInOutput("Uppercase Letters  : 0", output, "Uppercase")
        self.assertInOutput("Lowercase Letters  : 0", output, "Lowercase")
        self.assertInOutput("Digits             : 0", output, "Digits")

    @weight(0.1)
    def test_case3_only_spaces(self):
        """Test Case 3: String with only spaces"""
        # "    #" (4 spaces)
        output = self.run_student_program("    #")
        self.assertInOutput("Total Characters   : 4", output, "Total count")
        self.assertInOutput("Uppercase Letters  : 0", output, "Uppercase")
        self.assertInOutput("Lowercase Letters  : 0", output, "Lowercase")
        self.assertInOutput("Digits             : 0", output, "Digits")

    @weight(0.1)
    def test_case4_empty_string(self):
        """Test Case 4: Empty String"""
        # "#"
        output = self.run_student_program("#")
        self.assertInOutput("Total Characters   : 0", output, "Total count")
        self.assertInOutput("Uppercase Letters  : 0", output, "Uppercase")
        self.assertInOutput("Lowercase Letters  : 0", output, "Lowercase")
        self.assertInOutput("Digits             : 0", output, "Digits")

    @weight(0.1)
    def test_case5_two_lines(self):
        """Test Case 5: String with 2 lines (newline character)"""
        # "C++\nProgramming#"
        output = self.run_student_program("C++\nProgramming#")
        self.assertInOutput("Total Characters   : 15", output, "Total count")
        self.assertInOutput("Uppercase Letters  : 2", output, "Uppercase")
        self.assertInOutput("Lowercase Letters  : 10", output, "Lowercase")
        self.assertInOutput("Digits             : 0", output, "Digits")

    @weight(0.1)
    def test_case6_with_tab(self):
        """Test Case 6: String with tab character"""
        # "CSE\t100#"
        output = self.run_student_program("CSE\t100#")
        self.assertInOutput("Total Characters   : 7", output, "Total count")
        self.assertInOutput("Uppercase Letters  : 3", output, "Uppercase")
        self.assertInOutput("Lowercase Letters  : 0", output, "Lowercase")
        self.assertInOutput("Digits             : 3", output, "Digits")