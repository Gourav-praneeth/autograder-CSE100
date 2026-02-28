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
            ["g++", "-o", "Lab5_Q1.out", "Lab5_Question1.cpp"],
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
            ["./Lab5_Q1.out"],
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

    @weight(0.1)
    def test_case1_regular_650_minutes(self):
        """Test Case 1: Regular customer with 650 minutes"""
        # R, valid phone number, 650, n
        # Extra = 650 - 200 = 450 min
        # Stage1 = 250 * 0.55 = 137.5
        # Stage2 = 200 * 0.88 = 176.0
        # Total = 29.99 + 137.5 + 176.0 = 343.49
        output = self.run_student_program("R\n408-897-8978\n650\nn\n")
        self.assertInOutput("Total Cost: $343.49", output, "Regular 650 min bill")

    @weight(0.1)
    def test_case2_business_500_minutes(self):
        """Test Case 2: Business customer (lowercase) with 500 minutes"""
        # b, valid phone num, 500, n
        # 500 <= 600, no overage
        # Total = 99.99
        output = self.run_student_program("b\n650-123-4567\n500\nn\n")
        self.assertInOutput("Total Cost: $99.99", output, "Business 500 min bill")

    @weight(0.1)
    def test_case3_invalid_customer_type(self):
        """Test Case 3: Invalid customer type (g, t, C - 3 invalid entries)"""
        output = self.run_student_program("g\nt\nC\n")
        self.assertInOutput("Invalid customer type!", output, "Invalid type handling")

    @weight(0.1)
    def test_case4_invalid_minutes_then_valid(self):
        """Test Case 4: Business with invalid minutes (-10, -100) then valid (100)"""
        # B, valid phone number, -10, -100, 100
        # 100 <= 600, no overage
        # Total = 99.99
        output = self.run_student_program("B\n408-123-4567\n-10\n-100\n100\nn\n")
        self.assertInOutput("Total Cost: $99.99", output, "Business after invalid minutes")

    @weight(0.1)
    def test_case5_multiple_bills(self):
        """Test Case 5: Multiple bills - Regular 800 min then Business 300 min"""
        # r, valid phone number, 800, y, B, valid num, 300
        # First: Regular 800 min -> 29.99 + 250*0.55 + 350*0.88 = 29.99 + 137.5 + 308.0 = 475.49
        # Second: Business 300 min -> 99.99
        output = self.run_student_program("r\n650-987-6543\n800\ny\nB\n408-111-2222\n300\nn\n")
        self.assertInOutput("Total Cost: $475.49", output, "Regular 800 min bill")
        self.assertInOutput("Total Cost: $99.99", output, "Business 300 min bill")

    @weight(0.1)
    def test_case6_invalid_phone_number(self):
        """Test Case 6: Invalid US phone number for 3 entries"""
        # R, then 3 invalid phone numbers
        output = self.run_student_program("R\n12345\nabcdefghij\n123-45-6789\n")
        self.assertInOutput("Invalid phone number!", output, "Invalid phone handling")