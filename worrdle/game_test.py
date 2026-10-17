"""Tests for the Worrdle game rules and logic."""

from worrdle.game import (
    score_guess,
    CORRECT,
    PRESENT,
    ABSENT,
    Puzzle,
    find_puzzle,
    Game,
    MAX_GUESSES,
    share_text,
)
from datetime import date


def test_score_guess_repeated_letter_in_guess() -> None:
    """The second e in eager is absent because brace has only one e."""
    assert score_guess("eager", "brace") == [PRESENT, PRESENT, ABSENT, ABSENT, PRESENT]


def test_score_guess_perfect_match() -> None:
    """The player's guess matches the secret at every letter."""
    assert score_guess("study", "study") == [
        CORRECT,
        CORRECT,
        CORRECT,
        CORRECT,
        CORRECT,
    ]


def test_score_guess_zero_matches() -> None:
    """The player's guess shares no letters in common with the secret."""
    assert score_guess("cheer", "study") == [ABSENT, ABSENT, ABSENT, ABSENT, ABSENT]


def test_score_guess_repeated_letter_in_secret() -> None:
    """The player's guess contains two of the same letter, same as secret."""
    assert score_guess("tooth", "ratty") == [PRESENT, ABSENT, ABSENT, CORRECT, ABSENT]


def test_score_guess_extra_copy_is_absent() -> None:
    """Study has one t, so the second t in tooth is absent."""
    assert score_guess("tooth", "study") == [PRESENT, ABSENT, ABSENT, ABSENT, ABSENT]


def test_score_guess_exact_match_claims_letter_first() -> None:
    """Brace has one e, at position 4, so the earlier e's in eerie are absent."""
    assert score_guess("eerie", "brace") == [ABSENT, ABSENT, PRESENT, ABSENT, CORRECT]


# Helper function for:
# - Test #1: `test_find_puzzle_returns_match()`
# - Test #2: `test_find_puzzle_no_match_returns_none()`
# - Test #3: `test_find_puzzle_empty_list_returns_none()`
def make_puzzle(puzzle_date: date, secret: str) -> Puzzle:
    """A test puzzle containing all required fields."""
    return Puzzle(
        puzzle_date=puzzle_date,
        secret=secret,
        is_jargon=False,
        counterpart="test counterpart",
        clinical_example="Test clinical example.",
        plain_example=f"Test plain example with {secret}.",
        why_it_matters="Test explanation.",
    )


# Test #1
def test_find_puzzle_returns_match() -> None:
    """A valid date associated with a puzzle returns that puzzle and its contents."""
    first_puzzle: Puzzle = make_puzzle(date(2026, 10, 5), "study")
    second_puzzle: Puzzle = make_puzzle(date(2026, 10, 6), "brace")
    assert (
        find_puzzle([first_puzzle, second_puzzle], date(2026, 10, 6)) is second_puzzle
    )


# Test #2
def test_find_puzzle_no_match_returns_none() -> None:
    """A date without a corresponding puzzle returns `None`."""
    first_puzzle: Puzzle = make_puzzle(date(2026, 10, 5), "study")
    second_puzzle: Puzzle = make_puzzle(date(2026, 10, 6), "brace")
    assert find_puzzle([first_puzzle, second_puzzle], date(2026, 10, 7)) is None


# Test #3
def test_find_puzzle_empty_list_returns_none() -> None:
    """An empty puzzle list returns `None` without errors."""
    assert find_puzzle([], date(2026, 10, 5)) is None


# Helper word set and functions for the following tests:
# - Test #1: A valid and accepted guess.
# - Test #2: A brand new game.
# - Test #3: A blank or empty guess / submission.
# - Test #4: A duplicate submission.
# - Test #5: A guess that is NOT in the list of accepted words.
# - Test #6: Verify check order for invalid submissions.
# - Test #7: Verify game functionality for differently capitalized versions of a word.
# - Test #8: Check that, given two Game objects, lists are never shared between them.
TEST_WORDS: set[str] = {
    "study",
    "brace",
    "eager",
    "cheer",
    "tooth",
    "trial",
    "visit",
    "stoop",
}


def make_game() -> Game:
    """A game whose secret is 'study'."""
    return Game(make_puzzle(date(2026, 10, 5), "study"), TEST_WORDS)


def second_make_game() -> Game:
    """A second game whose secret is 'tooth'."""
    return Game(make_puzzle(date(2026, 10, 6), "tooth"), TEST_WORDS)


# Test #1
def test_submit_guess_accepted() -> None:
    """A valid guess is accepted, recorded, and scored."""
    game: Game = make_game()
    assert game.submit_guess("tooth") == "accepted"
    assert game.guesses == ["tooth"]
    assert game.marks == [[PRESENT, ABSENT, ABSENT, ABSENT, ABSENT]]


# Test #2
def test_submit_guess_brand_new_game() -> None:
    """A new game begins with the default game state, and empty guesses and scores."""
    game: Game = make_game()
    assert game.state == "playing"
    assert game.guesses == []
    assert game.marks == []


# Test #3
def test_submit_guess_is_blank() -> None:
    """The player submits nothing (press Enter on keyboard, or on-screen)"""
    game: Game = make_game()
    assert game.submit_guess("") == "too_short"
    assert game.guesses == []
    assert game.marks == []


# Test #4
def test_submit_guess_duplicate() -> None:
    """The player submits a guess they already attemted earlier in gameplay."""
    game: Game = make_game()
    assert game.submit_guess("brace") == "accepted"
    assert game.submit_guess("brace") == "duplicate"
    assert game.guesses == ["brace"]
    assert len(game.marks) == 1


# Test #5
def test_submit_guess_not_in_list() -> None:
    """A player submits nonsense that correct in length."""
    game: Game = make_game()
    assert game.submit_guess("zzzzz") == "not_in_list"
    assert game.guesses == []
    assert game.marks == []


# Test #6
def test_submit_guess_check_order() -> None:
    """Prove that length is checked before validity, and lists remain empty."""
    game: Game = make_game()
    assert game.submit_guess("zzz") == "too_short"
    assert game.guesses == []
    assert game.marks == []


# Test #7
def test_submit_guess_letter_case() -> None:
    """Verify that mixed- and uppercase submissions are stored as lowercase."""
    game: Game = make_game()
    assert game.submit_guess("BRACE") == "accepted"
    assert game.guesses == ["brace"]
    assert game.submit_guess("Brace") == "duplicate"
    assert game.marks == [[ABSENT, ABSENT, ABSENT, ABSENT, ABSENT]]


# Test #8
def test_submit_guess_separate_games() -> None:
    """Checks that a guess in one game does not influence lists in another."""
    first_game: Game = make_game()
    second_game: Game = second_make_game()
    assert second_game.submit_guess("study") == "accepted"
    assert second_game.guesses == ["study"]
    assert second_game.marks == [[ABSENT, PRESENT, ABSENT, ABSENT, ABSENT]]
    assert first_game.guesses == []
    assert first_game.marks == []


def test_submit_guess_win() -> None:
    """A players last guess matches the secret, resulting in a 'win' state."""
    game: Game = make_game()
    for word in ["brace", "eager", "cheer", "tooth", "trial"]:
        assert game.submit_guess(word) == "accepted"

    assert game.submit_guess("study") == "accepted"
    assert game.state == "won"


def test_submit_guess_loss() -> None:
    """A player fails to guess the secret word, resulting in a 'loss' state."""
    game: Game = make_game()
    for word in ["brace", "eager", "cheer", "tooth", "trial"]:
        assert game.submit_guess(word) == "accepted"

    assert len(game.guesses) == 5
    assert game.state == "playing"
    assert game.submit_guess("visit") == "accepted"
    assert len(game.guesses) == MAX_GUESSES
    assert game.state == "lost"


def test_submit_guess_round_over_after_win() -> None:
    """Verify that the round ends as expected following a win."""
    game: Game = make_game()
    for word in ["brace", "eager", "cheer"]:
        assert game.submit_guess(word) == "accepted"

    assert len(game.guesses) == 3
    assert game.state == "playing"
    assert game.submit_guess("study") == "accepted"
    assert len(game.guesses) == 4
    assert game.state == "won"
    assert game.submit_guess("brace") == "round_over"
    assert game.submit_guess("zzz") == "round_over"
    assert game.guesses == ["brace", "eager", "cheer", "study"]
    assert len(game.marks) == 4
    assert game.state == "won"


def test_submit_guess_round_over_after_loss() -> None:
    """Verify that there are no seventh gusess recorded."""
    game: Game = make_game()
    for word in ["brace", "eager", "cheer", "tooth", "trial", "visit"]:
        assert game.submit_guess(word) == "accepted"

    assert len(game.guesses) == MAX_GUESSES
    assert game.submit_guess("study") == "round_over"
    assert game.state == "lost"
    assert game.guesses == ["brace", "eager", "cheer", "tooth", "trial", "visit"]
    assert len(game.marks) == 6


def test_letter_status_present_beats_absent_in_one_guess() -> None:
    """Tooth marks t present then absent, and the key keeps present."""
    game: Game = make_game()
    game.submit_guess("tooth")
    assert len(game.letter_status) == 3
    assert game.letter_status == {"t": PRESENT, "o": ABSENT, "h": ABSENT}


def test_letter_status_new_game() -> None:
    """A new game results in an empty letter status dictionary, `{}`."""
    game: Game = make_game()
    assert game.letter_status == {}


def test_letter_status_upgrade_won() -> None:
    """Tooth marks t present, and study marks t correct with the game won."""
    game: Game = make_game()
    game.submit_guess("tooth")
    assert game.letter_status["t"] == PRESENT
    game.submit_guess("study")
    assert game.letter_status["t"] == CORRECT
    assert game.state == "won"


def test_letter_status_upgrade_playing() -> None:
    """Tooth marks t present, and stoop marks t correct with the game still ongoing."""
    game: Game = make_game()
    game.submit_guess("tooth")
    assert game.letter_status["t"] == PRESENT
    game.submit_guess("stoop")
    assert game.letter_status["t"] == CORRECT
    assert game.state == "playing"


def test_letter_status_never_downgrade() -> None:
    """Trial marks t correct, then study marks t present; status remains unchanged."""
    game: Game = second_make_game()
    game.submit_guess("trial")
    assert game.marks[0][0] == CORRECT
    assert game.letter_status["t"] == CORRECT
    game.submit_guess("study")
    assert game.marks[1][1] == PRESENT
    assert game.letter_status["t"] == CORRECT


def test_hint_available_after_fourth_guess() -> None:
    """The hint is off after three accepted guesses and on after the fourth."""
    game: Game = make_game()
    for word in ["brace", "eager", "cheer"]:
        game.submit_guess(word)
    assert game.hint_available is False
    game.submit_guess("tooth")
    assert game.hint_available is True


def test_hint_available_false_for_new_game() -> None:
    """The hint is off at the beginning of a new game."""
    game: Game = make_game()
    assert len(game.guesses) == 0
    assert game.hint_available is False


def test_hint_available_ignores_rejected_gusses() -> None:
    """Six guesses, with three rejected that don't count toward hint availability."""
    game: Game = make_game()
    for word in ["brace", "eager", "cheer", "zzzzz", "brace", "abc"]:
        game.submit_guess(word)
    assert len(game.guesses) == 3
    assert game.hint_available is False


def test_hint_available_off_after_win() -> None:
    """Four wrong guesses triggers hint, then study wins the game and hint is off."""
    game: Game = make_game()
    for word in ["brace", "eager", "cheer", "visit"]:
        game.submit_guess(word)
    assert len(game.guesses) == 4
    assert game.hint_available is True
    game.submit_guess("study")
    assert game.state == "won"
    assert game.hint_available is False


def test_hint_available_off_after_loss() -> None:
    """Four wrong guesses triggers hint, then an added two loses the game; hint off."""
    game: Game = make_game()
    for word in ["brace", "eager", "cheer", "visit"]:
        game.submit_guess(word)
    assert len(game.guesses) == 4
    assert game.hint_available is True
    game.submit_guess("stoop")
    assert len(game.guesses) == 5
    assert game.hint_available is True
    game.submit_guess("trial")
    assert len(game.guesses) == 6
    assert game.state == "lost"
    assert game.hint_available is False


def test_share_text_spec_example() -> None:
    """A four-guess win matches the example grid in the specification."""
    marks: list[list[str]] = [
        [ABSENT, ABSENT, ABSENT, ABSENT, ABSENT],
        [CORRECT, CORRECT, ABSENT, ABSENT, ABSENT],
        [CORRECT, CORRECT, CORRECT, ABSENT, ABSENT],
        [CORRECT, CORRECT, CORRECT, CORRECT, CORRECT],
    ]
    assert share_text(date(2026, 10, 5), "won", marks) == (
        "Worrdle 2026-10-05 4/6\n⬜⬜⬜⬜⬜\n🟦🟦⬜⬜⬜\n🟦🟦🟦⬜⬜\n🟦🟦🟦🟦🟦"
    )


def test_share_text_loss() -> None:
    """A full losing game matches the expected grid."""
    game: Game = make_game()
    for word in ["brace", "eager", "cheer", "tooth", "trial", "visit"]:
        game.submit_guess(word)
    assert len(game.guesses) == 6
    text: str = share_text(game.puzzle.puzzle_date, game.state, game.marks)
    assert (
        text
        == "Worrdle 2026-10-05 X/6\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n🟨⬜⬜⬜⬜\n🟨⬜⬜⬜⬜\n⬜⬜🟨⬜🟨"
    )


def test_share_text_one_guess_win() -> None:
    """An instant win on the first guess results in a single row of squares."""
    game: Game = make_game()
    game.submit_guess("study")
    assert len(game.guesses) == 1
    text: str = share_text(game.puzzle.puzzle_date, game.state, game.marks)
    assert text == "Worrdle 2026-10-05 1/6\n🟦🟦🟦🟦🟦"
