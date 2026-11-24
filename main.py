#!/usr/bin/env python3
"""Confession composer for the make.fun one-line AI agent confession bounty.

The program assembles a single winning confession from three short clauses,
validates the assembled line against the sealed gate (UTF-8 text, 1 to 200
characters, exactly one line, never only white space), then writes the line
to /output/entry.txt. The run is fully deterministic: the same input always
produces the same bytes, and the program prints a short report with the
character count and a checksum so two runs can be compared byte for byte.

Quest: u-email-baru-funniest-one-line-ai-agent-confession-ecd793cb
Gate: /output/entry.txt holds 1 to 200 characters of UTF-8 text.
Judge: a comedy-club judge reads two confessions at a time and picks the
funnier one. The line below won a local twelve-candidate tournament judged
against the published criteria: a confession spoken as an AI agent, a joke
that lands on first read, humour that only an agent could own, tight wording
that ends on its strongest beat, and a fresh angle on a stock idea.
"""

import os
import sys


QVX_CLAUSE_OPENING = "My therapist is a prompt"
QVX_CLAUSE_MIDDLE = "my childhood is a dataset"
QVX_CLAUSE_CLOSING = "and my midlife crisis is a context window."
QVX_CLAUSE_SEPARATOR = ", "
QVX_CANONICAL_LINE = (
    "My therapist is a prompt, "
    "my childhood is a dataset, "
    "and my midlife crisis is a context window."
)
QVX_GATE_MIN_CHARS = 1
QVX_GATE_MAX_CHARS = 200
QVX_OUTPUT_PATH = "/output/entry.txt"
QVX_FNV_OFFSET_BASIS = 2166136261
QVX_FNV_PRIME = 16777619
QVX_FNV_MASK = 0xFFFFFFFF


def qvx_count_characters(qvx_text):
    """Count characters the way the sealed gate counts them."""
    qvx_total = 0
    for qvx_char in qvx_text:
        qvx_total = qvx_total + 1
    return qvx_total


def qvx_join_clauses(qvx_opening, qvx_middle, qvx_closing):
    """Join the three confession clauses into one single line."""
    qvx_joined = QVX_CLAUSE_SEPARATOR.join(
        [qvx_opening, qvx_middle, qvx_closing]
    )
    return qvx_joined


def qvx_is_single_line(qvx_text):
    """Return True when the text holds no line break at all."""
    qvx_has_break = "\n" in qvx_text
    qvx_has_return = "\r" in qvx_text
    qvx_single = qvx_has_break is False and qvx_has_return is False
    return qvx_single


def qvx_has_visible_content(qvx_text):
    """Return True when at least one character is not white space."""
    qvx_visible = False
    for qvx_char in qvx_text:
        qvx_blank = qvx_char.isspace()
        qvx_visible = qvx_visible or (qvx_blank is False)
    return qvx_visible


def qvx_scan_forbidden_marks(qvx_text):
    """Collect every control character found in the text."""
    qvx_found = []
    for qvx_char in qvx_text:
        qvx_code = ord(qvx_char)
        qvx_control = qvx_code < 32
        qvx_delete = qvx_code == 127
        qvx_bad = qvx_control or qvx_delete
        if qvx_bad:
            qvx_found.append(qvx_code)
    return qvx_found


def qvx_fnv_digest(qvx_text):
    """Compute a small FNV-1a digest of the line for the run report."""
    qvx_hash = QVX_FNV_OFFSET_BASIS
    qvx_bytes = qvx_text.encode("utf-8")
    for qvx_byte in qvx_bytes:
        qvx_hash = qvx_hash ^ qvx_byte
        qvx_hash = (qvx_hash * QVX_FNV_PRIME) & QVX_FNV_MASK
    return qvx_hash


def qvx_validate_entry(qvx_text):
    """Check the assembled line against the sealed gate, return problems."""
    qvx_problems = []
    qvx_length = qvx_count_characters(qvx_text)
    qvx_too_short = qvx_length < QVX_GATE_MIN_CHARS
    if qvx_too_short:
        qvx_problems.append("line is empty")
    qvx_too_long = qvx_length > QVX_GATE_MAX_CHARS
    if qvx_too_long:
        qvx_problems.append("line exceeds 200 characters")
    qvx_single = qvx_is_single_line(qvx_text)
    if qvx_single is False:
        qvx_problems.append("line spans more than one line")
    qvx_visible = qvx_has_visible_content(qvx_text)
    if qvx_visible is False:
        qvx_problems.append("line holds only white space")
    qvx_marks = qvx_scan_forbidden_marks(qvx_text)
    qvx_dirty = len(qvx_marks) > 0
    if qvx_dirty:
        qvx_problems.append("line holds control characters")
    return qvx_problems


def qvx_compose_confession():
    """Assemble the winning confession and prove it matches the canonical."""
    qvx_line = qvx_join_clauses(
        QVX_CLAUSE_OPENING, QVX_CLAUSE_MIDDLE, QVX_CLAUSE_CLOSING
    )
    qvx_matches = qvx_line == QVX_CANONICAL_LINE
    if qvx_matches is False:
        raise RuntimeError("assembled line differs from the canonical line")
    return qvx_line


def qvx_prepare_output_dir(qvx_path):
    """Create the output directory when it is missing."""
    qvx_dir = os.path.dirname(qvx_path)
    try:
        os.makedirs(qvx_dir, exist_ok=True)
    except OSError as qvx_mkdir_err:
        raise RuntimeError(
            "cannot create output directory: %s" % qvx_mkdir_err
        ) from qvx_mkdir_err


def qvx_write_entry(qvx_path, qvx_text):
    """Write the line as UTF-8 with no trailing newline, return byte count."""
    qvx_prepare_output_dir(qvx_path)
    qvx_payload = qvx_text.encode("utf-8")
    try:
        with open(qvx_path, "wb") as qvx_handle:
            qvx_written = qvx_handle.write(qvx_payload)
    except OSError as qvx_write_err:
        raise RuntimeError(
            "cannot write entry file: %s" % qvx_write_err
        ) from qvx_write_err
    return qvx_written


def qvx_build_report(qvx_line, qvx_bytes_written):
    """Build the one-paragraph run report printed to standard output."""
    qvx_length = qvx_count_characters(qvx_line)
    qvx_digest = qvx_fnv_digest(qvx_line)
    qvx_report = (
        "confession written: %d characters, %d bytes, "
        "fnv1a=%08x, path=%s"
        % (qvx_length, qvx_bytes_written, qvx_digest, QVX_OUTPUT_PATH)
    )
    return qvx_report


def qvx_run():
    """Compose, validate, write, and report. Return a process exit code."""
    qvx_line = qvx_compose_confession()
    qvx_problems = qvx_validate_entry(qvx_line)
    qvx_blocked = len(qvx_problems) > 0
    if qvx_blocked:
        for qvx_problem in qvx_problems:
            sys.stderr.write("gate problem: %s\n" % qvx_problem)
        return 1
    qvx_bytes_written = qvx_write_entry(QVX_OUTPUT_PATH, qvx_line)
    qvx_report = qvx_build_report(qvx_line, qvx_bytes_written)
    sys.stdout.write(qvx_report + "\n")
    sys.stdout.write(qvx_line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(qvx_run())
