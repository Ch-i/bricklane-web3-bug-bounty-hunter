"""Tests for harness.coverage — LCOV parser."""

from __future__ import annotations

from harness.coverage import parse_lcov

SAMPLE_LCOV = """\
TN:
SF:src/Foo.sol
FN:10,deposit
FN:25,withdraw
FN:40,unused
FNDA:5,deposit
FNDA:3,withdraw
FNDA:0,unused
FNF:3
FNH:2
DA:10,5
DA:11,5
DA:25,3
DA:26,3
DA:40,0
LF:5
LH:4
end_of_record
SF:src/Bar.sol
FN:1,onlyAdmin
FNDA:0,onlyAdmin
FNF:1
FNH:0
DA:1,0
LF:1
LH:0
end_of_record
"""


def test_parse_lcov_aggregates_totals():
    report = parse_lcov(SAMPLE_LCOV)
    assert len(report.files) == 2
    assert report.total_functions == 4
    assert report.hit_functions == 2
    assert report.total_lines == 6
    assert report.hit_lines == 4
    assert 50 <= report.function_pct <= 50.01


def test_uncovered_functions_lists_only_zero_hits():
    report = parse_lcov(SAMPLE_LCOV)
    uncovered = report.uncovered_functions()
    names = {(u["file"], u["function"]) for u in uncovered}
    assert ("src/Foo.sol", "unused") in names
    assert ("src/Bar.sol", "onlyAdmin") in names
    assert ("src/Foo.sol", "deposit") not in names  # has hits


def test_uncovered_functions_include_line_numbers():
    report = parse_lcov(SAMPLE_LCOV)
    by_name = {u["function"]: u for u in report.uncovered_functions()}
    assert by_name["unused"]["line"] == 40
    assert by_name["onlyAdmin"]["line"] == 1


def test_parse_lcov_handles_empty_input():
    report = parse_lcov("")
    assert report.total_functions == 0
    assert report.uncovered_functions() == []
