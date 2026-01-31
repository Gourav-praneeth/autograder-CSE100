import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

# string comparison joining all output lines into a single string to check for substring match
class TestIdealWeightProgram(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0.2)
    def test_Compile(self):
        """Clean Compile: Program compiles without errors"""
        compile_process = subprocess.Popen(
            ["g++", "-o", "Lab3_Question1.out", "Lab3_Question1.cpp"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        _, compile_errors = compile_process.communicate()
        compile_process.kill()

        self.assertEqual(
            compile_errors.decode("utf-8").strip(), "",
            msg="Compilation failed. Please check your C++ syntax.\nErrors:\n" + compile_errors.decode("utf-8")
        )
        compile_process.terminate()

    def run_student_program(self, input_data="5 3\nFemale"):
        """Helper method to run the compiled program and capture output lines"""
        test = subprocess.Popen(
            ["./Lab3_Question1.out"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, _ = test.communicate(input=input_data.encode("utf-8"))
        test.kill()
        test.terminate()
        return output.decode("utf-8").splitlines()

    def assertInOutput(self, expected, output, section=""):
        """Helper to provide clearer error messages with suggestions"""
        # Join all output lines into a single string to check for substring match
        full_output = " ".join(output)
        
        if expected not in full_output:
            closest = difflib.get_close_matches(expected, output, n=1)
            suggestion = f"\nClosest match found: '{closest[0]}'" if closest else ""
            
            # Show the actual output with repr() to reveal hidden characters
            actual_lines = "\n".join([f"  [{i}]: {repr(line)}" for i, line in enumerate(output)])
            self.fail(
                f"{section} check failed.\n"
                f"Expected to find: '{expected}'\n"
                f"Actual output lines:\n{actual_lines}{suggestion}"
            )

    # ====== Test Cases ======
    @weight(0.1)
    def test_case1_female_5_3(self):
        """Test Case 1: height: 5 3, gender: Female"""
        output = self.run_student_program("5 3\nFemale")
        expected = "Your ideal weight should be 115 pounds."
        self.assertInOutput(expected, output, "Test Case 1")

    @weight(0.1)
    def test_case2_female_4_8(self):
        """Test Case 2: height: 4 8, gender: FEMALE"""
        output = self.run_student_program("4 8\nFEMALE")
        expected = "Your ideal weight should be 80 pounds."
        self.assertInOutput(expected, output, "Test Case 2")
        
    @weight(0.1)
    def test_case3_male_5_9(self):
        """Test Case 3: height: 5 9, gender: male"""
        output = self.run_student_program("5 9\nmale")
        expected = "Your ideal weight should be 160 pounds."
        self.assertInOutput(expected, output, "Test Case 3")
        
    @weight(0.1)
    def test_case4_male_6_3(self):
        """Test Case 4: height: 6 3, gender: MaLe"""
        output = self.run_student_program("6 3\nMaLe")
        expected = "Your ideal weight should be 196 pounds."
        self.assertInOutput(expected, output, "Test Case 4")

    @weight(0.1)
    def test_case5_invalid_height(self):
        """Test Case 5: height: -6 3, gender: Fmale (Invalid height)"""
        output = self.run_student_program("-6 3\nFmale")
        expected = "Invalid height!"
        self.assertInOutput(expected, output, "Test Case 5")

    @weight(0.1)
    def test_case6_invalid_gender(self):
        """Test Case 6: height: 4 3, gender: 2 (Invalid gender)"""
        output = self.run_student_program("4 3\n2")
        expected = "Invalid gender entered."
        self.assertInOutput(expected, output, "Test Case 6")
