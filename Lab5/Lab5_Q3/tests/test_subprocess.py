import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

SOURCE = "Lab5_Question3.cpp"    
BINARY = "Lab5_Question3.out"     

class TestSalesArrayProgram(unittest.TestCase):
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
        """Run student program and return full stdout as a single string.

        We DO NOT split lines because prompts may not include trailing newlines.
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
        """Check if expected substring is in output, else show a helpful snippet."""
        if expected not in output:
            closest = difflib.get_close_matches(expected, output.splitlines(), n=1)
            wrong = closest[0] if closest else (output[:500] + ("..." if len(output) > 500 else ""))
            self.fail(f"{section} check failed.\nExpected: '{expected}'\nFound:    '{wrong}'")

    # ===================== Test Cases (4 x 0.1) =====================

    @weight(0.1)
    def test_all_valid_increasing(self):
        """Test Case 1: All valid inputs""" # (10,20,...,100): high=100 at 9, low=10 0, avg=55.00
        inputs = "\n".join(str(10 * (i + 1)) for i in range(10)) + "\n"
        output = self.run_student_program(inputs)

        self.assertInOutput("Highest Sale: 100.00 at Store 9", output, "Highest sale")
        self.assertInOutput("Lowest Sale: 10.00 at Store 0", output, "Lowest sale")
        self.assertInOutput("Average Sale: 55.00", output, "Average")

    @weight(0.1)
    def test_single_invalid_then_valid(self):
        """Test Case 2: One invalid""" # (-1) for a store, then a valid value; stats reflect valid numbers
        # Stores: 5,7,9,(store3: -1 then 30),1,2,3,4,6,8  -> highest=30 3, lowest=1 4, avg=7.50
        inputs = "5\n7\n9\n-1\n30\n1\n2\n3\n4\n6\n8\n"
        output = self.run_student_program(inputs)

        # Ensure the invalid message appeared at least once
        self.assertInOutput("Invalid sale amount! Please enter a non-negative number.", output, "Invalid prompt")

        self.assertInOutput("Highest Sale: 30.00 at Store 3", output, "Highest sale")
        self.assertInOutput("Lowest Sale: 1.00 at Store 4", output, "Lowest sale")
        self.assertInOutput("Average Sale: 7.50", output, "Average")

    @weight(0.1)
    def test_three_invalids_sets_zero(self):
        """Test Case 3: Three invalid attempts for one store""" # -> set to 0; verify message and stats
        # Stores: 10,20,30,40,50,(store5: -1,-2,-3 -> 0),60,70,80,90
        inputs = "10\n20\n30\n40\n50\n-1\n-2\n-3\n60\n70\n80\n90\n"
        output = self.run_student_program(inputs)

        self.assertInOutput("Too many invalid attempts. Sale for store 5 set to 0.", output, "3 invalids message")
        self.assertInOutput("Highest Sale: 90.00 at Store 9", output, "Highest sale")
        self.assertInOutput("Lowest Sale: 0.00 at Store 5", output, "Lowest sale")
        self.assertInOutput("Average Sale: 45.00", output, "Average")

    @weight(0.1)
    def test_all_zero(self):
        """Test Case 4: All zeros""" 
        inputs = ("0\n" * 10)
        output = self.run_student_program(inputs)

        self.assertInOutput("Highest Sale: 0.00 at Store 0", output, "Highest sale")
        self.assertInOutput("Lowest Sale: 0.00 at Store 0", output, "Lowest sale")
        self.assertInOutput("Average Sale: 0.00", output, "Average")
