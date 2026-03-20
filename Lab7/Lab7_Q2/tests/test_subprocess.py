import unittest
import random
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib

BINARY = "./Lab7_Question2.out"
SOURCE = "Lab7_Question2.cpp"

class TestMatrixOperations(unittest.TestCase):
    def compile_program(self):
        proc = subprocess.Popen(
            ["g++", "-std=gnu++17", "-O2", "-o", BINARY, SOURCE],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = proc.communicate()
        return out.decode("utf-8"), err.decode("utf-8")

    def run_program(self, input_data: str) -> str:
        proc = subprocess.Popen(
            [f"./{BINARY}"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, _ = proc.communicate(input=input_data.encode("utf-8"))
        return out.decode("utf-8").strip()

    def assertContains(self, expected: str, output: str, title: str):
        if expected not in output:
            nearest = difflib.get_close_matches(expected, output.splitlines(), n=1)
            found = nearest[0] if nearest else (output[:500] + ("..." if len(output) > 500 else ""))
            self.fail(f"{title} failed.\nExpected: {expected}\nFound:    {found}")

    @weight(0.2)
    def test_compile(self):
        """Compilation (0.2)"""
        _, err = self.compile_program()
        self.assertEqual(err.strip(), "", msg="Compilation failed:\n" + err)

    @weight(0.15)
    def test_case_1_invalid_then_3x3(self):
        """Test Case 1"""
        # 0, -1, 3 then matrix {{-1,-2,4}, {6,-3,7}, {-10,8,9}}; total 18.
        # Invalid sizes 0, -1 (two "Size must be positive!"), then n=3, 3x3 matrix
        input_data = (
            "0\n-1\n3\n"
            "-1\n-2\n4\n"
            "6\n-3\n7\n"
            "-10\n8\n9\n"
        )
        out = self.run_program(input_data)
        self.assertContains("Size must be positive!", out, "Invalid size message")
        self.assertContains("Matrix computations Validated!", out, "Validation message")
        self.assertContains("18", out, "Total sum 18")

    @weight(0.15)
    def test_case_2_all_invalid_sizes(self):
        """Test Case 2"""
        # 0, -10, 0 -> three invalid sizes, exit.
        input_data = "0\n-10\n0\n"
        out = self.run_program(input_data)
        self.assertContains("Size must be positive!", out, "Invalid size message")
        count = out.count("Size must be positive!")
        self.assertGreaterEqual(count, 3, "Size must be positive! should appear at least 3 times")

    @weight(0.15)
    def test_case_3_4x4_matrix(self):
        """Test Case 3"""
        # n=4, matrix {{11,-2,10,-3}, {20,15,-13,4}, {-2,5,16,8}, {-1,-4,-6,12}}; total 70.
        input_data = (
            "4\n"
            "11\n-2\n10\n-3\n"
            "20\n15\n-13\n4\n"
            "-2\n5\n16\n8\n"
            "-1\n-4\n-6\n12\n"
        )
        out = self.run_program(input_data)
        self.assertContains("Matrix computations Validated!", out, "Validation message")
        self.assertContains("70", out, "Total sum 70")
        self.assertContains("11", out, "Element 1,1 present")

    @weight(0.15)
    def test_case_4_random_matrix(self):
        """Test Case 4"""
        # Random n and matrix; compare output total to Python-computed total
        random.seed(42)
        n = random.randint(2, 8)
        matrix = [[random.randint(-15, 15) for _ in range(n)] for _ in range(n)]
        expected_total = sum(matrix[i][j] for i in range(n) for j in range(n))

        # Build input: n, then row-major elements
        input_lines = [str(n)]
        for i in range(n):
            for j in range(n):
                input_lines.append(str(matrix[i][j]))
        input_data = "\n".join(input_lines) + "\n"

        out = self.run_program(input_data)
        self.assertContains("Matrix computations Validated!", out, "Validation message")
        self.assertContains(
            str(expected_total), out,
            f"Total sum (expected {expected_total} from random {n}x{n} matrix)"
        )
