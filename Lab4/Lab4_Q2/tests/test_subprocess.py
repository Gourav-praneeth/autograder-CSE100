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
            ["g++", "-o", "Lab4_Q2.out", "Lab4_Question2.cpp"],
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
            ["./Lab4_Question2.out"],
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
    def test_Header(self):
        """Check header is displayed correctly"""
        output = self.run_student_program("3\n100\n")
        self.assertInOutput("Time (s)\tDistance (m)", output, "Header")

    @weight(0.1)
    def test_ValidTable(self):
        """Check falling distance table is correct up to given time"""
        output = self.run_student_program("4\n100\n")
        self.assertInOutput("    0\t\t0", output, "Row for t=0")
        self.assertInOutput("    1\t\t4.9", output, "Row for t=1")
        self.assertInOutput("    2\t\t19.6", output, "Row for t=2")
        self.assertInOutput("    3\t\t44.1", output, "Row for t=3")
        self.assertInOutput("    4\t\t78.4", output, "Row for t=4")

    @weight(0.1)
    def test_WarningExceededHeight(self):
        """Check warning when distance exceeds bridge height"""
        output = self.run_student_program("10\n20\n")
        self.assertInOutput("Warning - Bad Data: The distance fallen exceeds the height of the bridge.", output, "Exceeded warning")

    @weight(0.05)
    def test_InvalidTime(self):
        """Check invalid time input exits after 3 attempts"""
        output = self.run_student_program("-1\n-2\n-3\n")
        self.assertInOutput("Invalid time!", output, "Invalid time handling")

    @weight(0.05)
    def test_InvalidHeight(self):
        """Check invalid height input exits after 3 attempts"""
        output = self.run_student_program("2\n-1\n-2\n-3\n")
        self.assertInOutput("Invalid height!", output, "Invalid height handling")
