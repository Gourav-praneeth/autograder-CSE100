import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

# Adjust these if your filenames differ
SOURCE = "Lab6_Question2.cpp"   # student's C++ file (replace if needed)
BINARY = "Lab6_Question2.out"          # compiled binary name

class TestCityBarGraph(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0.2)
    def test_Compile(self):
        """Clean Compile: Program compiles without errors"""
        compile_process = subprocess.Popen(
            ["g++", "-std=gnu++17", "-O2", "-o", BINARY, SOURCE],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        _, compile_errors = compile_process.communicate()
        compile_process.kill()

        self.assertEqual(
            compile_errors.decode("utf-8").strip(), "",
            msg="Compilation failed. Errors:\n" + compile_errors.decode("utf-8")
        )
        compile_process.terminate()

    def run_student_program(self, input_data):
        """Run student program and return full output as a single string.

        We DO NOT split lines because prompts may not include trailing newlines.
        Substring checks are more robust for typical C++ console I/O.
        """
        test = subprocess.Popen(
            [f"./{BINARY}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, _ = test.communicate(input=input_data.encode("utf-8"))
        test.kill()
        test.terminate()
        return output.decode("utf-8").strip()

    def assertInOutput(self, expected, output, section=""):
        """Check if expected substring is in output; else show a helpful snippet."""
        if expected not in output:
            closest = difflib.get_close_matches(expected, output.splitlines(), n=1)
            wrong = closest[0] if closest else (output[:500] + ("..." if len(output) > 500 else ""))
            self.fail(f"{section} check failed.\nExpected: '{expected}'\nFound:    '{wrong}'")

    # ===================== Test Cases (4 x 0.1) =====================

    @weight(0.1)
    def test_Header_and_BasicBars(self):
        """Test case 1""" # Header printed; bars for 3 cities: 0, 1, 1500 -> 0,1,2 stars
        # numCities=3; populations: 0, 1, 1500
        output = self.run_student_program("3\n0\n1\n1500\n")

        # Header
        self.assertInOutput("City    Population Bar Graph", output, "Header")
        self.assertInOutput("---------------------------------", output, "Separator")

        # Bars: output line is 'setw(2)<<i+1' + 7 spaces + stars
        # City 1: 0 -> 0 stars. We look for the exact spacing followed by newline.
        self.assertInOutput(" 1       \n", output, "City 1 (0 stars)")
        # City 2: 1 -> rounds to 1000 -> 1 star
        self.assertInOutput(" 2       *", output, "City 2 (1 star)")
        # City 3: 1500 -> rounds to 2000 -> 2 stars
        self.assertInOutput(" 3       **", output, "City 3 (2 stars)")

    @weight(0.1)
    def test_RoundingEdges(self):
        """Test case 2""" # Rounding up: 999 -> 1 star, 1001 -> 2 stars
        # numCities=2; populations: 999, 1001
        output = self.run_student_program("2\n999\n1001\n")

        # 999 -> 1000 -> 1 star
        self.assertInOutput(" 1       *", output, "City 1 (999 -> 1 star)")
        # 1001 -> 2000 -> 2 stars
        self.assertInOutput(" 2       **", output, "City 2 (1001 -> 2 stars)")

    @weight(0.1)
    def test_InvalidNumCities(self):
        """Test case 3""" #  Invalid number of cities (< 0) -> error and exit
        output = self.run_student_program("-1\n")
        self.assertInOutput("Invalid number of cities!", output, "Invalid numCities message")

    @weight(0.1)
    def test_TooManyInvalidPopulations(self):
        """Test Case 4""" #Three invalid population inputs trigger exit message
        # numCities=1; provide: -1, 'a' (fail state), -5 -> should hit limit and exit
        output = self.run_student_program("1\n-1\n-4\n-5\n")
        self.assertInOutput("Invalid population!", output, "Invalid population message")
        self.assertInOutput("Too many invalid inputs. Exiting program.", output, "Exit after 3 invalids")

    @weight(0.1)
    def test_ThreeInvalidForDifferentCities(self):
        """Test Case 5"""
        #"""Total 3 invalid, but for different cities: 4, -1, 1234, -2, 4567, -3"""
        # 4 cities; populations: -1 (invalid), 1234 (valid), -2 (invalid), 4567 (valid), -3 (invalid) -> exit
        output = self.run_student_program("4\n-1\n1234\n-2\n4567\n-3\n")
        self.assertInOutput("Invalid population!", output, "Invalid population message")
        self.assertInOutput("Too many invalid inputs. Exiting program.", output, "Exit after 3 invalids")

    @weight(0.1)
    def test_LessThanThreeInvalid(self):
        """Test Case 6"""
        #"""Less than 3 invalid: 4, 123, -100, 4567, 8901, -20, 34567"""
        # 4 cities; 123, -100 (invalid), 4567, 8901, -20 (invalid), 34567 -> completes with 4 cities
        output = self.run_student_program("4\n123\n-100\n4567\n8901\n-20\n34567\n")
        self.assertInOutput("City    Population Bar Graph", output, "Header")
        self.assertInOutput("---------------------------------", output, "Separator")
        self.assertNotIn("Too many invalid inputs. Exiting program.", output,
                         "Program should complete when fewer than 3 invalid inputs")
        # Bar graph for 4 cities: 123->1*, 4567->5*, 8901->9*, 34567->35*
        self.assertInOutput(" 1       *", output, "City 1 (123 -> 1 star)")
        self.assertInOutput(" 2       *****", output, "City 2 (4567 -> 5 stars)")
        self.assertInOutput(" 3       *********", output, "City 3 (8901 -> 9 stars)")
        self.assertInOutput(" 4       ***********************************", output, "City 4 row present")
