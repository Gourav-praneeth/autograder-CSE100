import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

class TestPhoneBillProgram(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0.2)
    def test_Compile(self):
        """Clean Compile: Program compiles without errors"""
        compile_process = subprocess.Popen(
            ["g++", "-o", "Lab4_Q1.out", "Lab4_Question1.cpp"],
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
        """Run student program and return full output as string"""
        test = subprocess.Popen(
            ["./Lab4_Question1.out"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, _ = test.communicate(input=input_data.encode("utf-8"))
        test.kill()
        test.terminate()
        return output.decode("utf-8").strip()

    def assertInOutput(self, expected, output, section=""):
        """Check if expected string is in output, else show closest match"""
        if expected not in output:
            closest = difflib.get_close_matches(expected, output.split(), n=1)
            wrong = closest[0] if closest else output
            self.fail(
                f"{section} check failed.\nExpected: '{expected}'\nFound:    '{wrong}'"
            )

    # ====== Test Cases ======

    @weight(0.05)
    def test_Header(self):
        """Test Case 1: Program Header"""
        output = self.run_student_program("R\n408-897-8978\n100\nN\n")
        self.assertInOutput("Phone Bill Generation Software", output, "Program header")

    @weight(0.05)
    def test_RegularWithinLimit(self):
        """Test Case 2: Regular customer under 200 min"""
        output = self.run_student_program("R\n668-897-8578\n150\nN\n")
        self.assertInOutput("Total Cost: $29.99", output, "Regular under 200 min bill")

    @weight(0.05)
    def test_RegularStage1(self):
        """Test Case 3: Regular customer Stage1 overage"""
        output = self.run_student_program("R\n408-897-8978\n300\nN\n")
        # Extra = 100 * 0.55 = 55.0 -> 29.99+55.0 = 84.99
        self.assertInOutput("Total Cost: $84.99", output, "Regular Stage1 bill")

    @weight(0.05)
    def test_BusinessWithinLimit(self):
        """Test Case 4: Business customer under 600 min"""
        output = self.run_student_program("B\n+14808977988\n476\nN\n")
        self.assertInOutput("Total Cost: $99.99", output, "Business under 600 min bill")

    @weight(0.05)
    def test_BusinessStage1(self):
        """Test Case 5: Business customer Stage1 overage"""
        output = self.run_student_program("B\n+14808977988\n650\nN\n")
        # Extra = 50*0.45 = 22.5 + base 99.99 = 122.49
        self.assertInOutput("Total Cost: $122.49", output, "Business Stage1 bill")

    @weight(0.05)
    def test_InvalidType(self):
        """Test Case 6: Invalid customer type (3 attempts exit)"""
        output = self.run_student_program("X\nY\nZ\n")
        self.assertInOutput("Invalid customer type!", output, "Invalid type handling")

    @weight(0.05)
    def test_InvalidMinutes(self):
        """Test Case 7: Invalid minutes (3 attempts exit)"""
        output = self.run_student_program("R\n123456\n-5\n-10\n-20\n")
        self.assertInOutput("Invalid phone usage!", output, "Invalid minutes handling")

    @weight(0.05)
    def test_ExitMessage(self):
        """Test Case 8: Program exit message"""
        output = self.run_student_program("R\n6692088345\n476\nN\n")
        self.assertInOutput("Exiting the program.........", output, "Exit message")
