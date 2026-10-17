# Worrdle

Worrdle is a daily word game about the language of research recruitment and retention. Each day there's one five-letter word to guess in six tries. The word is always a term people use when they recruit or keep research participants. Some days it's a piece of jargon, and some days it's the plain-language word that could replace it.

The double r in the name is on purpose. One r stands for recruitment and the other for retention.

**Play at [aliusora.github.io/worrdle](https://aliusora.github.io/worrdle/)**

I built Worrdle to practice what I learned in COMP 110 at UNC-Chapel Hill. It's a personal project, not an official university product. It's inspired by Wordle, which is a trademark of The New York Times Company, and it isn't affiliated with Wordle or the Times.

## How to play

Type a five-letter word and press Enter. Each guess has to be a word in the game's word list. After each guess, every tile shows how its letter fits:

| Tile | Meaning |
| --- | --- |
| Carolina blue with ✓ | The letter is in the word and in the right spot. |
| Yellow with ● | The letter is in the word but in a different spot. |
| Gray with – | The letter is not in the word. |

After your fourth guess, a Hint button appears. Using it is optional. It tells you whether today's word is the jargon term or the plain-language one.

When the round ends, you get your result as a grid of colored squares that you can copy and share. The grid doesn't give away the word. Below it, a short card shows both terms of the pair, each used in an example sentence, and explains why the choice of words matters. When the example comes from a study on ClinicalTrials.gov, the card links to the study record.

There's one puzzle per date, and the game uses the date on your own device. On a day with no puzzle, the page says so and links to the form for suggesting one.

## Suggest a puzzle

Anyone can suggest a puzzle through the [Worrdle submission form](https://forms.cloud.microsoft/r/U8JYDXJ1qz). The form asks for:

- a five-letter word, and whether it's the jargon term or the plain-language term
- the other term in the pair
- one example sentence in clinical or technical language and one in plain language
- optionally, why the wording matters, where the example comes from, and details for a credit line

I review every entry before it goes into the game. I may edit or adapt an entry to fit Worrdle, and I choose the date it runs. If you give a first name and an emoji, the card credits you by name. If not, the credit reads "from a contributor 💌".

## Your data

Worrdle has no accounts and doesn't send your guesses anywhere. Your browser keeps today's guesses, so reloading the page doesn't lose your place, and it remembers that you've already seen How to play. Clearing your browser's site data resets both. The page loads PyScript from pyscript.net and its fonts from Google Fonts.

## How it's built

Worrdle runs Python in the browser with [PyScript](https://pyscript.net/) 2026.7.3. The game is a set of static files served by GitHub Pages, with no server code.

```
index.html           the page and its styles
pyscript.json        tells PyScript which Python files to load
worrdle/
    game.py          game rules: scoring, puzzle lookup, the shareable result
    puzzles.py       the puzzles, one per date
    words.py         the accepted guesses
    page.py          connects the game to the page
    game_test.py     tests for the game rules
    puzzles_test.py  tests for the puzzle content
```

`game.py` has no browser code, so the rules can be tested with pytest. `page.py` handles everything the player sees and does.

Puzzles are added by hand. Each one is an entry in `puzzles.py` with its own date. The tests check every entry, including that the word is exactly five lowercase letters, that it appears in the matching example sentence, and that no two puzzles share a date or a word.

### Running it locally

PyScript pages have to be served from a web address, so opening `index.html` directly won't work. From the top folder of the repository, run:

```
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

To run the tests, install pytest and run this from the same folder:

```
python -m pytest worrdle
```

## License

The code is released under the [MIT License](LICENSE).

The license covers the code only. It doesn't cover the puzzle text, meaning the words, example sentences and explanations in `puzzles.py`. Contributors keep ownership of the entries they submit and give Worrdle permission to use, edit, adapt and publish them.

The accepted guesses in `words.py` come from a word list made with the English Speller Database (ESDB, previously SCOWL) by Kevin Atkinson. Its copyright notice, permission notice and the settings used are in [NOTICE](NOTICE).
