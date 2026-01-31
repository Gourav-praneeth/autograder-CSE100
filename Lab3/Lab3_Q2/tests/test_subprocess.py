import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

class TestBrowniePanProgram(unittest.TestCase):
    """
    This class contains all the tests for the Brownie Pan program.
    Each method starting with 'test_' is a separate test case.
    """

    def setUp(self):
        """This runs before each test (we don't need to do anything here)"""
        pass

    @weight(0.2)  
    def test_Compile(self):
        """Clean Compile: Program compiles without errors"""
        
        # Try to compile the student's C++ file using g++ compiler
        # This is like clicking "Build" in an IDE
        compile_process = subprocess.Popen(
            ["g++", "-o", "Lab3_Question2.out", "Lab3_Question2.cpp"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        _, compile_errors = compile_process.communicate()
        compile_process.kill()

        # If there are any error messages, the test fails
        self.assertEqual(
            compile_errors.decode("utf-8").strip(), "",
            msg="Compilation failed. Please check your C++ syntax.\nErrors:\n" + compile_errors.decode("utf-8")
        )
        compile_process.terminate()
    
    # HELPER FUNCTION - Runs the student's program with given input
    def run_student_program(self, input_data="8\n4\n1"):
        """
        This helper function runs the compiled program and captures what it prints.
        
        Parameters:
            input_data: The values to type in, separated by newlines (\n)
                        Example: "8\n4\n1" means type 8, then 4, then 1
        
        Returns:
            A list of lines that the program printed out
        """
        # Start the compiled program
        test = subprocess.Popen(
            ["./Lab3_Question2.out"],
            stdin=subprocess.PIPE,   # We'll send input to the program
            stdout=subprocess.PIPE,  # We'll capture what it prints
            stderr=subprocess.PIPE
        )
        
        # Send the input and get the output
        output, _ = test.communicate(input=input_data.encode("utf-8"))
        test.kill()
        test.terminate()
        
        # Split the output into separate lines and return
        return output.decode("utf-8").splitlines()

    # HELPER FUNCTION - Checks if expected text appears in the output
    def assertInOutput(self, expected, output, section=""):
        """
        Checks if the expected text appears somewhere in the program's output.
        
        Why we join all lines together:
            Sometimes program output appears on one long line instead of 
            separate lines (depends on how the student uses endl vs \n).
            By joining all lines, we can find the expected text regardless
            of how the output is formatted.
        
        Parameters:
            expected: The text we're looking for (e.g., "32 small brownies")
            output: List of lines the program printed
            section: Name of the test (for error messages)
        """
        # Combine all output lines into one big string
        # This way we can find text even if it's split across lines
        full_output = " ".join(output)
        
        # Check if the expected text appears anywhere in the output
        if expected not in full_output:
            # If not found, try to find something similar to help the student
            closest = difflib.get_close_matches(expected, output, n=1)
            suggestion = f"\nClosest match found: '{closest[0]}'" if closest else ""
            
            # Show exactly what the program printed (with hidden characters visible)
            # repr() shows things like tabs (\t) and spaces explicitly
            actual_lines = "\n".join([f"  [{i}]: {repr(line)}" for i, line in enumerate(output)])
            
            # Fail the test with a helpful error message
            self.fail(
                f"{section} check failed.\n"
                f"Expected to find: '{expected}'\n"
                f"Actual output lines:\n{actual_lines}{suggestion}"
            )
    
    @weight(0.1)  
    def test_case1_small_brownies(self):
        """Test Case 1: length: 8, width: 4, size: 1"""
        # Run program with: length=8, width=4, size=1 (small brownies)
        output = self.run_student_program("8\n4\n1")
        
        # The program should output this exact text somewhere
        # Calculation: (8/1) * (4/1) = 8 * 4 = 32 small brownies
        expected = "A 8 x 4 pan can hold 32 small brownies."
        self.assertInOutput(expected, output, "Test Case 1")

    @weight(0.1) 
    def test_case2_large_brownies(self):
        """Test Case 2: length: 17, width: 8, size: 2"""
        # Run program with: length=17, width=8, size=2 (large brownies)
        output = self.run_student_program("17\n8\n2")
        
        # Calculation: (17/2) * (8/2) = 8 * 4 = 32 large brownies
        expected = "A 17 x 8 pan can hold 32 large brownies."
        self.assertInOutput(expected, output, "Test Case 2")
        
    @weight(0.1) 
    def test_case3_invalid_size_negative(self):
        """Test Case 3: length: 10, width: 6, size: -2 (Invalid brownie size)"""
        # Run program with a NEGATIVE brownie size (invalid!)
        output = self.run_student_program("10\n6\n-2")
        
        # Program should reject this and show error message
        expected = "Invalid brownie size!"
        self.assertInOutput(expected, output, "Test Case 3")
        
    @weight(0.1) 
    def test_case4_invalid_length(self):
        """Test Case 4: length: -13, width: 11, size: 1 (Invalid length)"""
        # Run program with a NEGATIVE pan length (invalid!)
        output = self.run_student_program("-13\n11\n1")
        
        # Program should reject this and show error message
        expected = "Invalid length of pan!"
        self.assertInOutput(expected, output, "Test Case 4")

    @weight(0.1)  
    def test_case5_invalid_width(self):
        """Test Case 5: length: 11, width: 0, size: 2 (Invalid width)"""
        # Run program with ZERO pan width (invalid!)
        output = self.run_student_program("11\n0\n2")
        
        # Program should reject this and show error message
        expected = "Invalid width of pan!"
        self.assertInOutput(expected, output, "Test Case 5")

    @weight(0.1)
    def test_case6_invalid_size_zero(self):
        """Test Case 6: length: 15, width: 7, size: 0 (Invalid brownie size)"""
        # Run program with ZERO brownie size (invalid!)
        output = self.run_student_program("15\n7\n0")
        
        # Program should reject this and show error message
        expected = "Invalid brownie size!"
        self.assertInOutput(expected, output, "Test Case 6")
