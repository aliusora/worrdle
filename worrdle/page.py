"""Page code for Worrdle: connects the game to the web page."""

import asyncio
import importlib
from datetime import date

from pyscript import document, storage, Storage, web, when, window
from pyscript.ffi import to_js

import worrdle.puzzles

from worrdle.game import (
    ABSENT,
    CORRECT,
    MAX_GUESSES,
    PRESENT,
    WORD_LENGTH,
    Game,
    Puzzle,
    find_puzzle,
    share_text,
)
from worrdle.puzzles import PUZZLES
from worrdle.words import ACCEPTED_WORDS

KEYBOARD_ROWS: list[str] = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]

MARK_DISPLAY: dict[str, dict[str, str]] = {
    CORRECT: {"color": "#4B9CD3", "symbol": "\u2713"},
    PRESENT: {"color": "#FFD340", "symbol": "\u25cf"},
    ABSENT: {"color": "#A2AAAD", "symbol": "\u2013"},
}

MESSAGES: dict[str, str] = {
    "too_short": "Not enough letters.",
    "duplicate": "You already guessed that word.",
    "not_in_list": "Not in word list.",
}

HINT_JARGON: str = "Today's answer is a jargon term."
HINT_PLAIN: str = "Today's answer is a plain-language term."

LOSS_LINE: str = "You didn't solve today's puzzle. The answer is below."

STUDY_LINK_BASE: str = "https://clinicaltrials.gov/study/"
ANONYMOUS_CREDIT: str = "from a contributor \U0001f48c"

MESSAGE_SECONDS: int = 2
SCROLL_DELAY_SECONDS: float = 0.3

STORAGE_NAME: str = "worrdle"
PUZZLES_URL: str = "./worrdle/puzzles.py"

game: Game | None = None
loaded_day: date | None = None
typed: list[str] = []
message_number: int = 0
store: Storage | None = None


def build_board() -> None:
    """Add six empty rows of five tiles to the board."""
    board = web.page["board"]
    for row in range(MAX_GUESSES):
        row_div = web.div(classes=["row"])
        for col in range(WORD_LENGTH):
            row_div.append(web.div(id=f"tile-{row}-{col}", classes=["tile"]))
        board.append(row_div)


def build_keyboard() -> None:
    """Add the on-screen QWERTY keyboard, with Enter and Delete on the last row."""
    keyboard = web.page["keyboard"]
    for idx in range(len(KEYBOARD_ROWS)):
        row_div = web.div(classes=["key-row"])
        if idx == len(KEYBOARD_ROWS) - 1:
            row_div.append(web.button("Enter", id="key-enter", classes=["key"]))
        for letter in KEYBOARD_ROWS[idx]:
            row_div.append(web.button(letter, id=f"key-{letter}", classes=["key"]))
        if idx == len(KEYBOARD_ROWS) - 1:
            row_div.append(web.button("Delete", id="key-delete", classes=["key"]))
        keyboard.append(row_div)


def show_typed() -> None:
    """Show the typed letters in the current row's tiles."""
    if game is None:
        return
    row: int = len(game.guesses)
    for col in range(WORD_LENGTH):
        if col < len(typed):
            web.page[f"tile-{row}-{col}"].innerText = typed[col]
        else:
            web.page[f"tile-{row}-{col}"].innerText = ""


def show_marks(row: int) -> None:
    """Color one row's tiles and add each tile's symbol, from that guess's marks."""
    if game is None:
        return
    marks: list[str] = game.marks[row]
    for col in range(WORD_LENGTH):
        display: dict[str, str] = MARK_DISPLAY[marks[col]]
        tile = web.page[f"tile-{row}-{col}"]
        tile.style["background-color"] = display["color"]
        tile.append(web.span(display["symbol"], classes=["symbol"]))


def show_key_colors() -> None:
    """Color each guessed key by the strongest mark its letter has earned."""
    if game is None:
        return

    for letter in game.letter_status:
        mark: str = game.letter_status[letter]
        key = web.page[f"key-{letter}"]
        key.style["background-color"] = MARK_DISPLAY[mark]["color"]


def update_hint_button() -> None:
    """Show the Hint button only while the game says a hint is available."""
    if game is None:
        return

    web.page["hint-button"].hidden = not game.hint_available


def show_result() -> None:
    """Show the result line and the shareable grid when the round ends."""
    if game is None:
        return

    if game.state == "won":
        web.page["result-line"].innerText = (
            f"You solved it in {len(game.guesses)} of {MAX_GUESSES} guesses."
        )
    else:
        web.page["result-line"].innerText = LOSS_LINE

    web.page["share-grid"].innerText = share_text(
        game.puzzle.puzzle_date, game.state, game.marks
    )

    web.page["result"].hidden = False


def show_optional(element_id: str, label: str, value: str | None) -> None:
    """Show a labeled line only when its value exists; otherwise keep it hidden."""
    if value is None:
        web.page[element_id].hidden = True
    else:
        web.page[element_id].innerText = label + value
        web.page[element_id].hidden = False


def credit_line(puzzle: Puzzle) -> str | None:
    """Return the contributor credit for a puzzle, or None when there is none."""
    if puzzle.from_contributor is False:
        return None

    if puzzle.contributor_first_name is None or puzzle.contributor_emoji is None:
        return ANONYMOUS_CREDIT

    credit: str = f"from {puzzle.contributor_first_name} {puzzle.contributor_emoji}"
    if puzzle.contributor_affiliation is not None:
        credit += f", {puzzle.contributor_affiliation}"
    return credit


def find_word(sentence: str, word: str) -> int:
    """Return where word first appears as a whole word in sentence, ignoring case."""
    lower_sentence: str = sentence.lower()
    lower_word: str = word.lower()
    start: int = lower_sentence.find(lower_word)
    while start != -1:
        end: int = start + len(lower_word)
        letter_before: bool = start > 0 and lower_sentence[start - 1].isalpha()
        letter_after: bool = end < len(lower_sentence) and lower_sentence[end].isalpha()
        if not letter_before and not letter_after:
            return start
        start = lower_sentence.find(lower_word, start + 1)
    return -1


def show_example(element_id: str, sentence: str, word: str | None) -> None:
    """Show an example sentence, with word in bold when it is given and appears."""
    paragraph = web.page[element_id]
    paragraph.innerText = ""
    start: int = -1
    if word is not None:
        start = find_word(sentence, word)

    if start == -1:
        paragraph.innerText = sentence
        return

    end: int = start + len(word)
    paragraph.append(web.span(sentence[:start]))
    paragraph.append(web.strong(sentence[start:end]))
    paragraph.append(web.span(sentence[end:]))


def show_card() -> None:
    """Fill in and show the teaching card for today's puzzle."""
    if game is None:
        return

    puzzle: Puzzle = game.puzzle
    web.page["card-secret"].innerText = puzzle.secret
    if puzzle.is_jargon:
        web.page["clinical-term"].innerText = puzzle.secret
        web.page["plain-term"].innerText = puzzle.counterpart
        web.page["clinical-today"].hidden = False
        show_example("clinical-example", puzzle.clinical_example, puzzle.secret)
        show_example("plain-example", puzzle.plain_example, None)
    else:
        web.page["clinical-term"].innerText = puzzle.counterpart
        web.page["plain-term"].innerText = puzzle.secret
        web.page["plain-today"].hidden = False
        show_example("clinical-example", puzzle.clinical_example, None)
        show_example("plain-example", puzzle.plain_example, puzzle.secret)

    web.page["why-it-matters"].innerText = puzzle.why_it_matters

    show_optional("study-title", "", puzzle.study_title)
    show_optional("source-name", "Source: ", puzzle.source_name)

    if puzzle.nct_number is not None:
        link = web.page["nct-link"]
        link.innerText = puzzle.nct_number
        link.href = STUDY_LINK_BASE + puzzle.nct_number
        web.page["nct-line"].hidden = False

    has_study: bool = (
        puzzle.study_title is not None
        or puzzle.source_name is not None
        or puzzle.nct_number is not None
    )
    web.page["study-entry"].hidden = not has_study

    show_optional("credit", "", credit_line(puzzle))

    web.page["card"].hidden = False


def hide_message() -> None:
    """Hide the gameplay message."""
    web.page["message"].hidden = True


async def hide_message_later(number: int) -> None:
    """Wait, then hide the message if no newer message has replaced it."""
    await asyncio.sleep(MESSAGE_SECONDS)
    if number == message_number:
        hide_message()


def show_message(text: str) -> None:
    """Show a gameplay message that hides itself after MESSAGE_SECONDS."""
    global message_number
    message_number += 1
    web.page["message"].innerText = text
    web.page["message"].hidden = False
    asyncio.create_task(hide_message_later(message_number))


async def scroll_to_result_later() -> None:
    """Wait a moment, then scroll so the result sits at the top of the window."""
    await asyncio.sleep(SCROLL_DELAY_SECONDS)
    document.getElementById("result").scrollIntoView(True)


def finish_round() -> None:
    """Hide the keyboard, show the result and teaching card, and scroll to them."""
    web.page["keyboard"].hidden = True
    show_result()
    show_card()
    asyncio.create_task(scroll_to_result_later())


def open_how_to_play() -> None:
    """Show the How to play modal and move keyboard focus into it."""
    web.page["how-to-play"].hidden = False
    web.page["how-dialog"].focus()


def close_how_to_play() -> None:
    """Hide the How to play modal and release keyboard focus."""
    web.page["how-to-play"].hidden = True
    document.activeElement.blur()


def how_to_play_is_open() -> bool:
    """Return True while the How to play modal is showing."""
    return not web.page["how-to-play"].hidden


def start_round(puzzle: Puzzle, saved_words: list[str]) -> None:
    """Start a round, replay any saved words, and draw the board to match."""
    global game
    game = Game(puzzle, ACCEPTED_WORDS)
    build_board()
    build_keyboard()

    for word in saved_words:
        game.submit_guess(word)

    for row in range(len(game.guesses)):
        for col in range(WORD_LENGTH):
            web.page[f"tile-{row}-{col}"].innerText = game.guesses[row][col]
        show_marks(row)
    show_key_colors()
    update_hint_button()

    if game.state != "playing":
        finish_round()

    web.page["game"].hidden = False


def save_round() -> None:
    """Save today's date and the accepted guesses, if storage is open."""
    if store is None or game is None:
        return

    try:
        store["round"] = {"date": str(game.puzzle.puzzle_date), "guesses": game.guesses}
    except Exception:
        pass


def save_seen_how_to_play() -> None:
    """Remember that How to play has opened once, if storage is open."""
    if store is None:
        return

    try:
        store["seen_how_to_play"] = True
    except Exception:
        pass


def submit_typed() -> None:
    """Send the typed letters to the game and show the result."""
    if game is None or game.state != "playing":
        return
    row: int = len(game.guesses)
    status: str = game.submit_guess("".join(typed))
    if status == "accepted":
        show_marks(row)
        show_key_colors()
        update_hint_button()
        typed.clear()
        hide_message()
        save_round()
        if game.state != "playing":
            finish_round()
    else:
        show_message(MESSAGES[status])


def type_letter(letter: str) -> None:
    """Add a letter to the current row, unless it already holds five."""
    if game is None or game.state != "playing":
        return
    if len(typed) < WORD_LENGTH:
        typed.append(letter)
        show_typed()


def delete_letter() -> None:
    """Remove the last letter from the current row, if there is one."""
    if game is None or game.state != "playing":
        return
    if len(typed) > 0:
        typed.pop()
        show_typed()


@when("click", "#copy-button")
async def on_copy_click(event) -> None:
    """Copy the result text to the clipboard, with a message if it worked."""
    if game is None:
        return
    text: str = share_text(game.puzzle.puzzle_date, game.state, game.marks)
    try:
        await window.navigator.clipboard.writeText(text)
        web.page["copy-status"].innerText = "Copied"
    except Exception:
        pass


@when("click", "#how-button")
def on_how_click(event) -> None:
    """Open How to play when the player presses the button."""
    open_how_to_play()


@when("click", "#how-close")
def on_how_close(event) -> None:
    """Close How to play when the player presses the close control."""
    close_how_to_play()


@when("click", "#how-got-it")
def on_how_got_it(event) -> None:
    """Close How to play when the player presses Got it."""
    close_how_to_play()


@when("click", "#hint-button")
def on_hint_click(event) -> None:
    """Reveal the hint, which then stays visible for the rest of the round."""
    if game is None:
        return

    if game.puzzle.is_jargon:
        web.page["hint-text"].innerText = HINT_JARGON
    else:
        web.page["hint-text"].innerText = HINT_PLAIN

    web.page["hint-text"].hidden = False


@when("click", "#keyboard")
def on_key_click(event) -> None:
    """Handle a tap or click on the on-screen keyboard."""
    key_id: str = event.target.id
    if key_id == "key-delete":
        delete_letter()
    elif key_id == "key-enter":
        submit_typed()
    elif key_id.startswith("key-"):
        type_letter(key_id[4:])


@when("keydown", document)
def on_key_down(event) -> None:
    """Handle a key press on a physical keyboard."""
    if how_to_play_is_open():
        if event.key == "Escape":
            close_how_to_play()
        return
    if event.ctrlKey or event.metaKey or event.altKey:
        return
    key: str = event.key
    if key == "Backspace":
        delete_letter()
    elif key == "Enter":
        submit_typed()
    elif len(key) == 1 and key.lower() >= "a" and key.lower() <= "z":
        type_letter(key.lower())


def local_today() -> date:
    """Return today's date where the player is, read from the browser's clock."""
    now = window.Date.new()
    return date(now.getFullYear(), now.getMonth() + 1, now.getDate())


async def fresh_puzzles() -> list[Puzzle]:
    """Download puzzles.py again, skipping the browser cache, and reload it.

    The browser may keep an old copy of puzzles.py that is missing today's
    puzzle. If the download fails, the puzzles already loaded are returned.
    """
    try:
        response = await window.fetch(PUZZLES_URL, to_js({"cache": "no-store"}))
        if not response.ok:
            return PUZZLES
        text: str = await response.text()
        with open(worrdle.puzzles.__file__, "w") as file:
            file.write(text)
        importlib.invalidate_caches()
        importlib.reload(worrdle.puzzles)
        return worrdle.puzzles.PUZZLES
    except Exception:
        return PUZZLES


async def find_todays_puzzle(today: date) -> Puzzle | None:
    """Find today's puzzle, checking a fresh copy of the list before giving up."""
    puzzle: Puzzle | None = find_puzzle(PUZZLES, today)
    if puzzle is None:
        puzzle = find_puzzle(await fresh_puzzles(), today)
    return puzzle


async def open_store() -> Storage | None:
    """Open the browser storage, or return None if the browser blocks it."""
    try:
        return await storage(STORAGE_NAME)
    except Exception:
        return None


def saved_words_for(puzzle: Puzzle) -> list[str]:
    """Return the saved guesses for this puzzle, clearing any older or broken round."""
    if store is None:
        return []

    try:
        saved = store.get("round")
        if saved is None:
            return []
        if saved["date"] == str(puzzle.puzzle_date):
            return list(saved["guesses"])
    except Exception:
        pass

    try:
        del store["round"]
    except Exception:
        pass
    return []


def reload_if_new_day() -> None:
    """Reload the page when the date has changed since it loaded."""
    if loaded_day is not None and local_today() != loaded_day:
        window.location.reload()


@when("visibilitychange", document)
def on_visibility_change(event) -> None:
    """Check the date when the player comes back to this tab."""
    if document.visibilityState == "visible":
        reload_if_new_day()


@when("pageshow", window)
def on_page_show(event) -> None:
    """Check the date when the browser shows this page again from its history."""
    reload_if_new_day()


async def main() -> None:
    """Find today's puzzle, restore any saved round, and show the page."""
    global store, loaded_day
    loaded_day = local_today()
    puzzle: Puzzle | None = await find_todays_puzzle(loaded_day)
    web.page["loading"].hidden = True

    if puzzle is None:
        web.page["no-puzzle"].hidden = False
        return

    store = await open_store()
    saved_words: list[str] = saved_words_for(puzzle)

    start_round(puzzle, saved_words)

    if store is None or store.get("seen_how_to_play") is None:
        open_how_to_play()
        save_seen_how_to_play()


if __name__ == "__main__":
    await main()
