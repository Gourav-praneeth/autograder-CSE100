import unittest
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import difflib
import re

BINARY = "./Lab8.out"     # adjust if needed
SOURCE = "Lab8.cpp"       # adjust if needed

class TestRPSBlackBox(unittest.TestCase):
    # --------------- helpers ---------------
    def compile_program(self):
        proc = subprocess.Popen(
            ["g++", "-std=gnu++17", "-O2", "-o", BINARY, SOURCE],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = proc.communicate()
        return out.decode("utf-8"), err.decode("utf-8")

    def run_program(self, input_data: str) -> str:
        """Run compiled binary with simulated stdin; capture stdout as string."""
        proc = subprocess.Popen(
            [BINARY],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, _ = proc.communicate(input=input_data.encode("utf-8"))
        return out.decode("utf-8")

    def _normalize(self, s: str) -> str:
        """Collapse all whitespace to single spaces and lowercase for flexible matching."""
        return re.sub(r"\s+", " ", s).strip().lower()

    def assertContainsFlex(self, expected: str, output: str, title: str):
        """Case/whitespace-insensitive substring check."""
        if self._normalize(expected) not in self._normalize(output):
            snippet = output[:500] + ("..." if len(output) > 500 else "")
            self.fail(f"{title} failed.\nExpected (flex): {expected}\nOutput (partial):\n{snippet}")

    def assertNotContainsFlex(self, unexpected: str, output: str, title: str):
        if self._normalize(unexpected) in self._normalize(output):
            snippet = output[:500] + ("..." if len(output) > 500 else "")
            self.fail(f"{title} failed.\nDid not expect (flex): {unexpected}\nOutput (partial):\n{snippet}")

    # --------------- tests ---------------

    @weight(0.2)
    def test_00_compile(self):
        """Test 0: Program compiles successfully"""
        _, err = self.compile_program()
        self.assertEqual(err.strip(), "", msg="Compilation failed:\n" + err)

    @weight(0.2)
    def test_01_single_round_then_stop(self):
        """Test 1: Single Round"""
        # initial rounds=1; choose 'r'; play again? -> 'n'
        out = self.run_program("1\nr\nn\n")
        self.assertContainsFlex("enter your choice", out, "Choice prompt")
        self.assertContainsFlex("player chose", out, "Round result header")
        self.assertContainsFlex("computer chose", out, "Computer choice header")
        self.assertContainsFlex("result:", out, "Round outcome header")
        self.assertContainsFlex("final score", out, "Final summary")

    @weight(0.2)
    def test_02_extension_prompt_declined(self):
        """Test 2: Extension prompt decline"""
        # initial=1; play 1 round '1'; play again? 'y'; extension prompt -> 'n' to decline
        out = self.run_program("1\n1\ny\nn\n")
        self.assertContainsFlex("you set 1 round(s). do you want to play more? (y/n):", out, "Extension prompt")
        self.assertContainsFlex("final score", out, "Final summary")

    @weight(0.2)
    def test_03_getPositiveInt_invalid_then_valid(self):
        """Test 3: Invalid Integer"""
        out = self.run_program("-1\n0\n3\nq\n")
        self.assertContainsFlex("invalid input type", out, "Reject non-numeric")
        self.assertContainsFlex("value must be a positive integer", out, "Reject zero")
        self.assertContainsFlex("you chose to quit. ending the game early.", out, "Quit sentinel")
        self.assertContainsFlex("final score", out, "Final summary shown")

    @weight(0.2)
    def test_04_invalid_choice_then_valid(self):
        """Test 4: Invalid Choice"""
        out = self.run_program("1\n\nrockk\nr\nn\n")
        self.assertContainsFlex("no input detected", out, "Empty choice rejected")
        self.assertContainsFlex("invalid input. please enter r/p/s (or 1/2/3), or 'q' to quit.", out, "Bad token rejected")
        self.assertContainsFlex("player chose", out, "Round completed")
        self.assertContainsFlex("final score", out, "Final summary")

    @weight(0.2)
    def test_05_extend_by_additional_rounds(self):
        """Test 5: Extend by 2 rounds after first; per-round results shown"""
        # initial=1
        # R1: 'p'; play again? -> 'y'
        # Extension prompt -> 'y', additional rounds=2
        # R2: 's'; play again? -> 'y'
        # R3: 'r'; play again? -> 'n'
        out = self.run_program("1\np\ny\ny\n2\ns\ny\nr\nn\n")
        self.assertContainsFlex("you set 1 round(s). do you want to play more? (y/n):", out, "Extension prompt")
        self.assertContainsFlex("how many additional rounds would you like to add?", out, "Additional rounds prompt")
        self.assertContainsFlex("per-round results (1=win, 0=draw, -1=loss):", out, "Per-round results")
        self.assertContainsFlex("final score", out, "Final summary")

    @weight(0.2)
    def test_06_quit_sentinel_early(self):
        """Test 6: Quit with 'q' immediately on first choice"""
        out = self.run_program("2\nq\n")
        self.assertContainsFlex("you chose to quit. ending the game early.", out, "Quit sentinel")
        self.assertContainsFlex("final score", out, "Final summary")

    @weight(0.2)
    def test_07_large_number_then_valid(self):
        """Test 7: Very large number, overflow path"""
        out = self.run_program("99999999999999999999999999999\n1\nr\nn\n")
        self.assertContainsFlex("number too large or invalid. try again.", out, "Overflow detected")
        self.assertContainsFlex("enter your choice", out, "Continued to first round")
        self.assertContainsFlex("final score", out, "Final summary")

    @weight(0.2)
    def test_08_case_insensitive_full_word(self):
        """Test 8: Case-insensitive full-word choice 'Rock' accepted"""
        out = self.run_program("1\nRock\nn\n")
        self.assertContainsFlex("player chose", out, "Full-word choice recognized")
        self.assertContainsFlex("final score", out, "Final summary")