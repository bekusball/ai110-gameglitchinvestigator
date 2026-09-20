# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

## 📸 Demo Walkthrough

1. Run `python -m streamlit run app.py` and open the local URL shown in the terminal.
2. Choose **Easy**, **Normal**, or **Hard** in the sidebar. The sidebar shows that difficulty's number range and attempt limit.
3. Open **Developer Debug Info** to reveal the secret number for the demo.
4. Enter a number and select **Submit Guess 🚀**. A valid guess is recorded and the game responds with **Go HIGHER!**, **Go LOWER!**, or a win message. Empty or non-numeric input shows an error without using an attempt.
5. Enter the secret number to win and see the final score. Select **New Game 🔁** to reset the score, attempt count, history, and secret number for another round.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ .venv/bin/python -m pytest tests/ -q
...................                                                      [100%]
19 passed in 10.83s
```

The test suite checks guess outcomes and hints, numeric comparison with string secrets, input validation, attempt counting, and New Game reset behavior.

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
