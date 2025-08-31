'''
Each Test Case has Five Main Parts:
    1. Weight
    2. Name  
    3. Subprocess
    4. Python Unit Test
    5. Error Message  
    
'''

'''
Weight: This is how many points the test case is worth and is defined using a precondition before the function

Name:   There are two names for every test case. 
        A Python unit test name and Gradescope test name (Shown to the students). 
        The Python function name must start with test_ to indictate that it is to be tested. 
        Every Test Case must have a different name.

Subprocess: This is the multithreaded component. 
            Here we use Popen to create a new thread running our students code. 
            Denote the parameter requires a list of strings therefore any command line input must be placed within their own string.

Python Test Case: Compare the students output to an expected output using python operators.

Error Message (Optional but Recommended): This allows you to give your students more descriptive feedback based on their output 
                                            or give them common troubleshooting techniques
'''

import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess


class TestDiff(unittest.TestCase):
    def setUp(self):
        pass 

    # Associated point value within GradeScope
    # @weight(0)
    # def test_Compile(self):
    #     #Title used by Gradescope 
    #     """Clean Compile"""

    #     # Create a subprocess to run the students make file to ensure it compiles 
    #     test = subprocess.Popen(["make"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     output = test.stderr.read().strip().decode('utf-8')
    #     test.kill()

    #     # Standard unit test case with an associated error message 
    #     self.assertTrue( output == "", msg=output)
    #     test.terminate()

    # Associated point value within GradeScope
    @weight(5)
    def test_RunOutput(self):
        #Title used by Gradescope 
        """Run: Output Matching"""

        # Create a subprocess to run the students code to obtain an output 
        test = subprocess.Popen(["./test1.out"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = test.stdout.read().strip().decode('utf-8')
        test.kill()

        # Standard unit test case with an associated error message 
        self.assertTrue( output == "Hello World!", msg=("Expected: Hello World!\nFound: "+output))
        test.terminate()

    # Associated point value within GradeScope
    @weight(5)
    def test_RunCharCount(self):
        #Title used by Gradescope 
        """Run: Character Count"""

        # Create a subprocess to run the students code to obtain an output 
        test = subprocess.Popen(["./test1.out"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = test.stdout.read().strip().decode('utf-8')
        test.kill()

        # Standard unit test case with an associated error message 
        self.assertTrue( len(output) == 12, msg=("Expected: 12 characters\nFound: "+str(len(output))))
        test.terminate()

