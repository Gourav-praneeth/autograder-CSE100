import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib
import re
from typing import List, Optional, Tuple

BINARY = "./Lab9_Question1.out"
SOURCE = "Lab9_Question1.cpp"

_ROSTER_CHUNK = re.compile(
    r"([A-Za-z][^,\t\n]{1,80},\s+[^\t\n]+\t\d+\t[^\t\r\n]+)"
)


def _strip_prompt_prefix_name(name_field: str) -> Optional[str]:
    """Recover 'Last, First' when prompts are merged into the name field (piped I/O)."""
    idx = name_field.rfind(", ")
    if idx < 0:
        return None
    head = name_field[:idx].strip()
    rest = name_field[idx + 2 :].strip()
    if not head or not rest:
        return None
    first_token = rest.split()[0]
    last_tokens = head.split()
    if not last_tokens:
        return None
    last_name = last_tokens[-1]
    return f"{last_name}, {first_token}"


def _normalize_roster_chunk(chunk: str) -> Optional[str]:
    parts = chunk.split("\t")
    if len(parts) != 3 or not parts[1].strip().isdigit():
        return None
    name_field = parts[0]
    if ":" in name_field:
        cleaned = _strip_prompt_prefix_name(name_field)
        if cleaned is None:
            return None
        name_field = cleaned
    if "Enter" in name_field:
        return None
    return f"{name_field}\t{parts[1]}\t{parts[2]}"


def _roster_lines(output: str) -> List[str]:
    rows: List[str] = []
    for ln in output.splitlines():
        last_good: Optional[str] = None
        for m in _ROSTER_CHUNK.finditer(ln):
            normalized = _normalize_roster_chunk(m.group(1).strip())
            if normalized is not None:
                last_good = normalized
        if last_good is not None:
            rows.append(last_good)
    return rows


def _parse_last_first(full_name: str) -> Tuple[str, str]:
    """Lab format '<last name>, <first name>[ ...]'."""
    idx = full_name.find(", ")
    if idx < 0:
        return full_name.strip(), ""
    last = full_name[:idx].strip()
    rest = full_name[idx + 2 :].strip()
    first = rest.split()[0] if rest else ""
    return last, first


def _assert_ascending_lab8_name_order(rows: List[str], msg: str) -> None:
    """Last name ascending; tie-break by first name (Lab 8 output rule)."""
    keys: List[Tuple[str, str]] = []
    for line in rows:
        name = line.split("\t")[0]
        keys.append(_parse_last_first(name))
    for a, b in zip(keys, keys[1:]):
        if a > b:
            raise AssertionError(
                f"{msg}: expected non-decreasing (last, first), got {a!r} then {b!r}"
            )


class TestLab9Question1(unittest.TestCase):
    def compile_program(self):
        proc = subprocess.Popen(
            ["g++", "-std=gnu++17", "-O2", "-Wall", "-o", BINARY, SOURCE],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        return out.decode("utf-8"), err.decode("utf-8")

    def run_program(self, input_data: str) -> str:
        proc = subprocess.Popen(
            [BINARY],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, _ = proc.communicate(input=input_data.encode("utf-8"))
        return out.decode("utf-8").strip()

    def assertContains(self, expected: str, output: str, title: str):
        if expected not in output:
            nearest = difflib.get_close_matches(
                expected, output.splitlines(), n=1
            )
            found = (
                nearest[0]
                if nearest
                else (output[:500] + ("..." if len(output) > 500 else ""))
            )
            self.fail(
                f"{title} failed.\nExpected: {expected}\nFound:    {found}"
            )

    @weight(0.2)
    def test_compile(self):
        """Compilation"""
        _, err = self.compile_program()
        self.assertEqual(err.strip(), "", msg="Compilation failed:\n" + err)

    @weight(0.1)
    def test_1_all_valid_inputs(self):
        """Test Case 1"""
        #"""1. All valid inputs; count is final roster size (here 3 students)."""
        input_data = (
            "3\n"
            "Doe, Jane\n"
            "1001\n"
            "Freshman\n"
            "Smith, John\n"
            "1002\n"
            "Senior\n"
            "Brown, Alice\n"
            "1003\n"
            "Junior\n"
        )
        out = self.run_program(input_data)
        lines = _roster_lines(out)
        self.assertEqual(
            lines,
            [
                "Brown, Alice\t1003\tJunior",
                "Doe, Jane\t1001\tFreshman",
                "Smith, John\t1002\tSenior",
            ],
        )

    @weight(0.1)
    def test_2_invalid_id_three_attempts(self):
        """Test Case 2"""
        #"""2. Invalid student ID only; exit after 3 attempts."""
        input_data = "1\nHall, Ethan\n0\n-5\n-1\n"
        out = self.run_program(input_data)
        self.assertContains(
            "Invalid input! ID should be positive.",
            out,
            "ID validation message",
        )
        self.assertContains("Too many Invalid Attempts!", out, "Exit message")
        self.assertEqual(_roster_lines(out), [])

    @weight(0.1)
    def test_invalid_student_count_shows_typed_value(self):
        """Test Case 3"""
        #"""Invalid count message includes the number the user entered."""
        input_data = "-1\n0\n101\n"
        out = self.run_program(input_data)
        self.assertContains(
            "Invalid input! -1 should be positive.",
            out,
            "Negative count message",
        )
        self.assertContains(
            "Invalid input! 0 should be positive.",
            out,
            "Zero count message",
        )
        self.assertContains(
            "Invalid input! 101 should be positive.",
            out,
            "Too-large count message",
        )
        self.assertContains("Too many Invalid Attempts!", out, "Exit message")
        self.assertEqual(_roster_lines(out), [])

    @weight(0.1)
    def test_3_invalid_name_three_attempts(self):
        """Test Case 4"""
        #"""3. Invalid names only; exit after 3 attempts (shared counter)."""
        input_data = (
            "2\n"
            "King\n"
            "King,Wain\n"
            "King Wain\n"
        )
        out = self.run_program(input_data)
        self.assertContains(
            "Invalid name! Attempt 1 of 3.", out, "Name attempt 1"
        )
        self.assertContains(
            "Invalid name! Attempt 2 of 3.", out, "Name attempt 2"
        )
        self.assertContains(
            "Invalid name! Attempt 3 of 3.", out, "Name attempt 3"
        )
        self.assertContains("Too many Invalid Attempts!", out, "Exit message")
        self.assertEqual(_roster_lines(out), [])

    @weight(0.1)
    def test_4_ascending_order_by_last_name(self):
        """Test Case 5"""
        #"""4. Roster ascending by last name; tie-break by first name (Lab 8)."""
        input_data = (
            "3\n"
            "Smith, John\n"
            "10\n"
            "Sophomore\n"
            "Smith, Alice\n"
            "20\n"
            "Freshman\n"
            "Adams, Zoe\n"
            "30\n"
            "Junior\n"
        )
        out = self.run_program(input_data)
        lines = _roster_lines(out)
        self.assertEqual(len(lines), 3, msg="Expected 3 roster lines")
        _assert_ascending_lab8_name_order(lines, "Last/first name order")
        self.assertEqual(
            lines[0].split("\t")[0],
            "Adams, Zoe",
            "Adams should sort before Smith",
        )
        self.assertEqual(
            lines[1].split("\t")[0],
            "Smith, Alice",
            "Same last name: Alice before John",
        )
        self.assertEqual(lines[2].split("\t")[0], "Smith, John")

    # @weight(0.1)
    # def test_5_sorted_elements_correct(self):
    #     """Test Case 5"""
    #     #"""5. Names entered unsorted; output matches correct full sort order."""
    #     input_data = (
    #         "3\n"
    #         "Zebra, Zed\n"
    #         "3\n"
    #         "Senior\n"
    #         "Adams, Amy\n"
    #         "1\n"
    #         "Freshman\n"
    #         "Miller, Max\n"
    #         "2\n"
    #         "Sophomore\n"
    #     )
    #     out = self.run_program(input_data)
    #     lines = _roster_lines(out)
    #     names = [ln.split("\t")[0] for ln in lines]
    #     self.assertEqual(
    #         names,
    #         ["Adams, Amy", "Miller, Max", "Zebra, Zed"],
    #         "Selection sort + insert should yield this order",
    #     )

    @weight(0.1)
    def test_6_insert_in_middle_of_sorted_array(self):
        """Test Case 6"""
        #"""6. New student belongs strictly between min and max after sort."""
        input_data = (
            "3\n"
            "Adams, Amy\n"
            "1\n"
            "Freshman\n"
            "Zebra, Zed\n"
            "99\n"
            "Senior\n"
            "Miller, Max\n"
            "50\n"
            "Junior\n"
        )
        out = self.run_program(input_data)
        lines = _roster_lines(out)
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0].split("\t")[0], "Adams, Amy")
        self.assertEqual(lines[1].split("\t")[0], "Miller, Max")
        self.assertEqual(lines[2].split("\t")[0], "Zebra, Zed")
