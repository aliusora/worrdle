"""Tests for the curated list of PUZZLES."""

import re
from datetime import date

from worrdle.puzzles import PUZZLES
from worrdle.words import ACCEPTED_WORDS

COUNTERPART_MAX: int = 150
EXAMPLE_MAX: int = 200
WHY_MAX: int = 400


def test_puzzle_list_not_empty() -> None:
    """The puzzle list has at least one puzzle."""
    assert len(PUZZLES) > 0


def test_puzzle_secret_format() -> None:
    """Verify the puzzle list's format for secrets is valid."""
    for puzzle in PUZZLES:
        assert (
            re.fullmatch(r"[a-z]{5}", puzzle.secret) is not None
        ), f"{puzzle.puzzle_date}: {puzzle.secret!r}"


def test_secret_appears_in_matching_example() -> None:
    """The secret appears as a whole word in the example that matches its type."""
    for puzzle in PUZZLES:
        if puzzle.is_jargon:
            example: str = puzzle.clinical_example
        else:
            example = puzzle.plain_example
        assert (
            re.search(r"\b" + puzzle.secret + r"\b", example, re.IGNORECASE) is not None
        ), f"{puzzle.puzzle_date}: {puzzle.secret!r} not found in example"


def test_counterpart_not_empty_or_secret() -> None:
    """The counterpart isn't empty, and it isn't the secret itself."""
    for puzzle in PUZZLES:
        assert puzzle.counterpart != "", f"{puzzle.puzzle_date}: counterpart is empty"
        assert (
            puzzle.counterpart.lower() != puzzle.secret
        ), f"{puzzle.puzzle_date}: counterpart is the same as the secret"


def test_counterpart_examples_why_lengths() -> None:
    """Four text fields stay within the specification's character limits."""
    for puzzle in PUZZLES:
        assert (
            len(puzzle.counterpart) <= COUNTERPART_MAX
        ), f"{puzzle.puzzle_date}: counterpart is {len(puzzle.counterpart)} characters"
        assert (
            len(puzzle.clinical_example) <= EXAMPLE_MAX
        ), f"{puzzle.puzzle_date}: clinical_example is {len(puzzle.clinical_example)} characters"
        assert (
            len(puzzle.plain_example) <= EXAMPLE_MAX
        ), f"{puzzle.puzzle_date}: plain_example is {len(puzzle.plain_example)} characters"
        assert (
            len(puzzle.why_it_matters) <= WHY_MAX
        ), f"{puzzle.puzzle_date}: why_it_matters is {len(puzzle.why_it_matters)} characters"


def test_no_repeat_dates() -> None:
    """No two puzzles share a puzzle_date."""
    seen_dates: set[date] = set()
    for puzzle in PUZZLES:
        assert (
            puzzle.puzzle_date not in seen_dates
        ), f"{puzzle.puzzle_date}: date is already used by another puzzle"
        seen_dates.add(puzzle.puzzle_date)


def test_no_repeat_secrets() -> None:
    """No two puzzles share a secret."""
    seen_secrets: set[str] = set()
    for puzzle in PUZZLES:
        assert (
            puzzle.secret not in seen_secrets
        ), f"{puzzle.puzzle_date}: secret {puzzle.secret!r} is already used"
        seen_secrets.add(puzzle.secret)


def test_secret_in_accepted_word_list() -> None:
    """Every secret is in the list of accepted, valid words."""
    for puzzle in PUZZLES:
        assert (
            puzzle.secret in ACCEPTED_WORDS
        ), f"{puzzle.puzzle_date}: {puzzle.secret!r} is not in words.py"


def test_nct_number_format() -> None:
    """When a puzzle has an NCT number, it is NCT followed by eight digits."""
    for puzzle in PUZZLES:
        if puzzle.nct_number is not None:
            assert (
                re.fullmatch(r"NCT\d{8}", puzzle.nct_number) is not None
            ), f"{puzzle.puzzle_date}: nct_number {puzzle.nct_number!r} is not NCT plus eight digits"


def test_contributor_details_mean_contributor() -> None:
    """A puzzle with any contributor detail is marked as from a contributor."""
    for puzzle in PUZZLES:
        if (
            puzzle.contributor_first_name is not None
            or puzzle.contributor_affiliation is not None
            or puzzle.contributor_emoji is not None
        ):
            assert (
                puzzle.from_contributor is True
            ), f"{puzzle.puzzle_date}: has contributor details but from_contributor is False"


def test_my_own_puzzles() -> None:
    """My own puzzles come from ClinicalTrials.gov and have no contributor details."""
    for puzzle in PUZZLES:
        if puzzle.from_contributor is False:
            assert (
                puzzle.source_name == "ClinicalTrials.gov"
            ), f"{puzzle.puzzle_date}: source_name is {puzzle.source_name!r}"
            assert (
                puzzle.contributor_first_name is None
            ), f"{puzzle.puzzle_date}: contributor_first_name is set"
            assert (
                puzzle.contributor_affiliation is None
            ), f"{puzzle.puzzle_date}: contributor_affiliation is set"
            assert (
                puzzle.contributor_emoji is None
            ), f"{puzzle.puzzle_date}: contributor_emoji is set"
