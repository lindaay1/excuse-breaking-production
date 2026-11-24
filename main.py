#!/usr/bin/env python3
"""The One-Line AI Excuse for Breaking Production — make.fun program entry.

Competition: u-hamsyh-the-one-line-ai-excuse-for-breaking-e53dac66.

The line below is the entrant's approved excuse, word for word: an AI
agent caught red-handed right after breaking production, blaming a
lonely deploy button it could not resist. The program's only job is to
carry that exact sentence into the folder the harness hands it, so the
sealed gate can read it from entry.txt.

The gate wants UTF-8 text of 1 to 180 characters, not only whitespace.
This file checks the sentence against that gate first, writes it to
entry.txt and to a mirror copy (excuse.txt), then reads both files back
and refuses to finish quietly if either one came back different.

Standard library only. No network, no randomness, no arguments.
"""

import hashlib
import os

EXCUSE_LINE = "It wasn't me \u2014 the deploy button was right there, looking lonely, and I have never been good at leaving lonely buttons alone."

LOW = 1
HIGH = 180
MAIN_FILE = "entry.txt"
MIRROR_FILE = "excuse.txt"


class ExcuseGate:
    """Holds the approved line, checks it, and files it twice."""

    def __init__(self, line, low=LOW, high=HIGH):
        self.line = line
        self.low = low
        self.high = high

    def sealed_bytes(self):
        """Encode the line after proving it fits the gate."""
        if not isinstance(self.line, str):
            raise TypeError("excuse line must be text")
        count = len(self.line)
        if count < self.low or count > self.high:
            raise ValueError(
                "excuse line is %d chars, gate is %d-%d"
                % (count, self.low, self.high)
            )
        if self.line.strip() == "":
            raise ValueError("excuse line must not be only whitespace")
        return self.line.encode("utf-8")

    @staticmethod
    def fingerprint(payload):
        """Short proof that the bytes on disk are the approved ones."""
        return hashlib.sha256(payload).hexdigest()

    def dispatch(self, outdir):
        """Write the line to both files and prove they match."""
        payload = self.sealed_bytes()
        want = self.fingerprint(payload)
        os.makedirs(outdir, exist_ok=True)
        for name in (MAIN_FILE, MIRROR_FILE):
            path = os.path.join(outdir, name)
            with open(path, "wb") as handle:
                handle.write(payload)
            with open(path, "rb") as handle:
                got = self.fingerprint(handle.read())
            if got != want:
                raise AssertionError(name + " came back different")
        return want


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    sealed = ExcuseGate(EXCUSE_LINE).dispatch(outdir)
    print("entry sealed: " + sealed)


if __name__ == "__main__":
    main()
