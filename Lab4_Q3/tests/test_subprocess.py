import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

class TestFallingDistanceProgram(unittest.TestCase):

    def setUp(self):
        pass

    @weight(0.1)
    def test_Compile(self):
        """Program compiles without errors"""
        compile_process = subprocess.Popen(
            ["g++", "-o", "Lab4_Q3.out", "Lab4_Question3.cpp"],
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
            ["./Lab4_Question3.out"],
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
    def test_simple(self):
        """Counts mix of upper/lower/digit"""
        output = self.run_student_program("Hello, welcome to Tempe. Today's temperature is 117!#")
        self.assertInOutput("Total Characters   : 52", output, "Total count")
        self.assertInOutput("Uppercase Letters  : 3", output, "Uppercase")
        self.assertInOutput("Lowercase Letters  : 35", output, "Lowercase")
        self.assertInOutput("Digits             : 3", output, "Digits")

    @weight(0.1)
    def test_with_spaces_symbols(self):
        """Counts with spaces and punctuation"""
        output = self.run_student_program("Hello World! 99#")
        # "Hello World! 99" has 15 characters before #
        self.assertInOutput("Total Characters   : 15", output, "Total count")
        self.assertInOutput("Uppercase Letters  : 2", output, "Uppercase")
        self.assertInOutput("Lowercase Letters  : 8", output, "Lowercase")
        self.assertInOutput("Digits             : 2", output, "Digits")

    @weight(0.1)
    def test_only_digits(self):
        """Counts only digits"""
        output = self.run_student_program("987654#")
        self.assertInOutput("Total Characters   : 6", output, "Total count")
        self.assertInOutput("Uppercase Letters  : 0", output, "Uppercase")
        self.assertInOutput("Lowercase Letters  : 0", output, "Lowercase")
        self.assertInOutput("Digits             : 6", output, "Digits")

    @weight(0.1)
    def test_only_uppercase(self):
        """Counts only uppercase"""
        output = self.run_student_program("ABCXYZ#")
        self.assertInOutput("Total Characters   : 6", output, "Total count")
        self.assertInOutput("Uppercase Letters  : 6", output, "Uppercase")
        self.assertInOutput("Lowercase Letters  : 0", output, "Lowercase")
        self.assertInOutput("Digits             : 0", output, "Digits")

    @weight(0.1)
    def test_empty_input(self):
        """Handles empty string before #"""
        output = self.run_student_program("#")
        self.assertInOutput("Total Characters   : 0", output, "Total count")
        self.assertInOutput("Uppercase Letters  : 0", output, "Uppercase")
        self.assertInOutput("Lowercase Letters  : 0", output, "Lowercase")
        self.assertInOutput("Digits             : 0", output, "Digits")