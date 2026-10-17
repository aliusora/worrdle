"""Game rules for Worrdle, including scoring and puzzle selection."""

__author__ = "Ali Sora"


from datetime import date

WORD_LENGTH: int = 5
MAX_GUESSES: int = 6
HINT_AFTER: int = 4

CORRECT: str = "correct"
PRESENT: str = "present"
ABSENT: str = "absent"

CAROLINA_BLUE_BOX: str = "\U0001f7e6"
YELLOW_BOX: str = "\U0001f7e8"
WHITE_BOX: str = "\U00002b1c"


class Puzzle:
    """One day's puzzle and all its contents."""

    puzzle_date: date
    secret: str
    is_jargon: bool
    counterpart: str
    clinical_example: str
    plain_example: str
    why_it_matters: str
    source_name: str | None
    nct_number: str | None
    study_title: str | None
    contributor_first_name: str | None
    contributor_affiliation: str | None
    contributor_emoji: str | None
    from_contributor: bool

    def __init__(
        self,
        puzzle_date: date,
        secret: str,
        is_jargon: bool,
        counterpart: str,
        clinical_example: str,
        plain_example: str,
        why_it_matters: str,
        source_name: str | None = None,
        nct_number: str | None = None,
        study_title: str | None = None,
        contributor_first_name: str | None = None,
        contributor_affiliation: str | None = None,
        contributor_emoji: str | None = None,
        from_contributor: bool = False,
    ) -> None:

        self.puzzle_date = puzzle_date
        self.secret = secret
        self.is_jargon = is_jargon
        self.counterpart = counterpart
        self.clinical_example = clinical_example
        self.plain_example = plain_example
        self.why_it_matters = why_it_matters
        self.source_name = source_name
        self.nct_number = nct_number
        self.study_title = study_title
        self.contributor_first_name = contributor_first_name
        self.contributor_affiliation = contributor_affiliation
        self.contributor_emoji = contributor_emoji
        self.from_contributor = from_contributor


def find_puzzle(puzzles: list[Puzzle], today: date) -> Puzzle | None:
    """Locates and loads the day's puzzle for gameplay, or `None` if there is none."""

    for puzzle in puzzles:
        if puzzle.puzzle_date == today:
            return puzzle

    return None


def score_guess(guess: str, secret: str) -> list[str]:
    """
    Scores a guess in two passes:
    - Pass #1: Finds exact matches; counts unmatched letters.
    - Pass #2: Finds shared letters from unmatched set; leaves all other letters as is.
    """
    # Pass #1
    idx: int = 0
    marks: list[str] = []
    counts: dict[str, int] = {}
    while idx < WORD_LENGTH:
        if guess[idx] == secret[idx]:
            marks.append(CORRECT)
        else:
            marks.append(ABSENT)
            unmatched: str = secret[idx]
            if unmatched in counts:
                counts[unmatched] += 1
            else:
                counts[unmatched] = 1

        idx += 1
    # Pass #2
    idx = 0
    while idx < WORD_LENGTH:
        guessed: str = guess[idx]
        # Skip any position already marked CORRECT (perfect match).
        # If guessed letter appears in the secret one or more times, mark PRESENT.
        if marks[idx] != CORRECT and guessed in counts and counts[guessed] > 0:
            marks[idx] = PRESENT
            counts[guessed] -= 1

        idx += 1

    return marks


def share_text(puzzle_date: date, state: str, marks: list[list[str]]) -> str:
    """
    Produces shareable text for the player after a complete game.

    Includes:
    - A title line 'Worrdle', date, and number of attempts or guesses.
    - One row of emoji squares per guess.

    This is the only player-facing text that `game.py` produces. It was included
    in this module so that testing could be done without needing browser access.
    """
    if state == "won":
        count: str = str(len(marks))
    else:
        count = "X"

    text: str = f"Worrdle {puzzle_date} {count}/{MAX_GUESSES}"

    for row in marks:
        squares: str = ""
        for mark in row:
            if mark == CORRECT:
                squares += CAROLINA_BLUE_BOX
            elif mark == PRESENT:
                squares += YELLOW_BOX
            else:
                squares += WHITE_BOX
        text += "\n" + squares

    return text


class Game:
    """Records a players round during gameplay."""

    puzzle: Puzzle
    accepted_words: set[str]
    state: str
    guesses: list[str]
    marks: list[list[str]]
    letter_status: dict[str, str]
    hint_available: bool

    def __init__(self, puzzle: Puzzle, accepted_words: set[str]) -> None:

        self.puzzle = puzzle
        self.accepted_words = accepted_words
        self.state = "playing"
        self.guesses = []
        self.marks = []
        self.letter_status = {}
        self.hint_available = False

    def submit_guess(self, guess: str) -> str:
        """
        Standardizes then checks a guess upon submission and either:
        1. Accepts and record it, or
        2. Rejects it, in which case Return a statement.

        Submitted guesses, once accepted and recorded, are then scored.
        """

        guess = guess.lower()

        if self.state != "playing":
            return "round_over"

        if len(guess) < WORD_LENGTH:
            return "too_short"

        if guess in self.guesses:
            return "duplicate"

        if guess not in self.accepted_words:
            return "not_in_list"

        self.guesses.append(guess)
        new_marks: list[str] = score_guess(guess, self.puzzle.secret)
        self.marks.append(new_marks)

        idx: int = 0
        while idx < WORD_LENGTH:
            letter: str = guess[idx]
            mark: str = new_marks[idx]
            if letter not in self.letter_status:
                self.letter_status[letter] = mark
            elif mark == CORRECT:
                self.letter_status[letter] = CORRECT
            elif mark == PRESENT and self.letter_status[letter] == ABSENT:
                self.letter_status[letter] = PRESENT

            idx += 1

        if self.puzzle.secret == guess:
            self.state = "won"
        elif len(self.guesses) == MAX_GUESSES:
            self.state = "lost"

        self.hint_available = (
            len(self.guesses) >= HINT_AFTER and self.state == "playing"
        )

        return "accepted"
