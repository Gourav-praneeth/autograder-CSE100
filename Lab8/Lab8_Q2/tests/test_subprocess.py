import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess

BINARY = "./Lab8_Question2.out"
SOURCE = "Lab8_Question2.cpp"

def grid_to_input(grid):
    """Convert 2D list (matrix) to stdin string: first line 'm n', then m lines of n space-separated integers."""
    m = len(grid)
    n = len(grid[0]) if m else 0
    lines = [f"{m} {n}"]
    for row in grid:
        lines.append(" ".join(str(x) for x in row))
    return "\n".join(lines) + "\n"


def multi_header_and_grid_input(headers, grid):
    """
    Build input where multiple (m, n) pairs are tried before finally providing the grid.
    headers: list of (m, n) tuples; last one must match grid shape.
    """
    lines = []
    for m, n in headers:
        lines.append(f"{m} {n}")
    m = len(grid)
    n = len(grid[0]) if m else 0
    for row in grid:
        lines.append(" ".join(str(x) for x in row))
    return "\n".join(lines) + "\n"

def get_count_from_output(out):
    """Extract count from 'Number of negative numbers in the grid: 1' line."""
    for line in out.strip().split("\n"):
        line = line.strip()
        if "Number of negative numbers in the grid:" in line:
            tokens = line.split()
            return tokens[-1] if tokens else None
    return None

class TestCountNegatives(unittest.TestCase):
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

    @weight(0.2)
    def test_compile(self):
        """Compilation (0.2)"""
        _, err = self.compile_program()
        self.assertEqual(err.strip(), "", msg="Compilation failed:\n" + err)

    @weight(0.1)
    def test_example_1(self):
        """Test Case 1"""
        # First try invalid sizes: (-4,4), (4,0), then valid (4,4).
        grid = [
            [4, 3, 2, -1],
            [3, 2, 1, -1],
            [1, 1, -1, -2],
            [-1, -1, -2, -3]
        ]
        headers = [(-4, 4), (4, 0), (4, 4)]
        input_data = multi_header_and_grid_input(headers, grid)
        out = self.run_program(input_data)
        # Two invalid size messages, then correct result.
        self.assertTrue(
            "Invalid number of rows" in out or "Invalid number of columns" in out,
            msg="Expected invalid rows/columns message. Output: " + out[:400]
        )
        self.assertEqual(get_count_from_output(out), "8", msg="Expected count 8. Output: " + out)

    @weight(0.1)
    def test_example_2_no_negatives(self):
        """Test Case 2"""
        #"""Test 2: Example 2 - no negative numbers, output 0."""
        grid = [[3, 2], [1, 0]]
        input_data = grid_to_input(grid)
        out = self.run_program(input_data)
        self.assertEqual(get_count_from_output(out), "0", msg="Expected count 0. Output: " + out)

    @weight(0.1)
    def test_all_negatives(self):
        """Test Case 3"""
        #"""Test 3: Edge - all elements negative."""
        grid = [[-1, -2], [-3, -4]]
        input_data = grid_to_input(grid)
        out = self.run_program(input_data)
        self.assertEqual(get_count_from_output(out), "4", msg="Expected count 4. Output: " + out)

    @weight(0.1)
    def test_single_row(self):
        """Test Case 4"""
        #"""Test 4: Edge - single row with mix of positive and negative."""
        grid = [[5, 2, -1, -3]]
        input_data = grid_to_input(grid)
        out = self.run_program(input_data)
        self.assertEqual(get_count_from_output(out), "2", msg="Expected count 2. Output: " + out)

    @weight(0.1)
    def test_single_element_negative(self):
        """Test Case 5"""
        #"""Test 5: Edge - single element matrix, negative."""
        grid = [[-5]]
        input_data = grid_to_input(grid)
        out = self.run_program(input_data)
        self.assertEqual(get_count_from_output(out), "1", msg="Expected count 1. Output: " + out)

    @weight(0.1)
    def test_unsorted_then_sorted(self):
        """Test Case 6"""
        #"""Test 6: Unsorted matrix triggers message, then sorted matrix accepted; 1x2."""
        # First give 1x2 unsorted [3, -1] (ascending), then same size sorted [3, -1] (descending)
        input_data = (
            "1\n2\n"
            "-1 3\n"   # row 1: ascending (invalid)
            "3 -1\n"   # second attempt: descending, valid; one negative
        )
        out = self.run_program(input_data)
        self.assertIn("Elements should be in descending order!", out,
                      "Expected descending-order message when matrix not sorted")
        self.assertIn("Number of negative numbers in the grid:", out, "Expected count line after retry")
        self.assertEqual(get_count_from_output(out), "1", msg="Expected 1 negative. Output: " + out)