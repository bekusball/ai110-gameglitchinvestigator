"""End-to-end tests that drive app.py through Streamlit's AppTest harness."""

import random

from streamlit.testing.v1 import AppTest


def start_app(difficulty="Normal", secret=50):
    """Run the app, select a difficulty, and pin the secret so runs are repeatable."""
    at = AppTest.from_file("app.py", default_timeout=30)
    at.run()

    if difficulty != "Normal":
        at.selectbox[0].set_value(difficulty).run()

    at.session_state["secret"] = secret
    at.run()
    return at


def click(at, label):
    for button in at.button:
        if button.label.startswith(label):
            return button.click().run()
    raise AssertionError(f"no button labelled {label!r}")


def guess(at, value):
    at.text_input[0].set_value(str(value))
    return click(at, "Submit Guess")


def test_new_game_clears_a_finished_game():
    at = start_app(secret=50)
    at = guess(at, 50)
    assert at.session_state["status"] == "won"

    at = click(at, "New Game")
    assert at.session_state["status"] == "playing"


def test_new_game_resets_the_score():
    at = start_app(secret=50)
    at = guess(at, 50)
    assert at.session_state["score"] != 0

    at = click(at, "New Game")
    assert at.session_state["score"] == 0


def test_new_game_clears_the_guess_history():
    at = start_app(secret=50)
    at = guess(at, 20)
    assert at.session_state["history"] == [20]

    at = click(at, "New Game")
    assert at.session_state["history"] == []


def test_new_game_is_playable_after_a_win():
    at = start_app(secret=50)
    at = guess(at, 50)

    at = click(at, "New Game")
    # A fresh game must accept guesses again rather than short-circuiting on
    # the old "you already won" screen.
    at = guess(at, 1)
    assert at.session_state["history"] == [1]


def test_new_game_secret_respects_the_difficulty_range():
    random.seed(20260915)
    at = start_app(difficulty="Easy")

    for _ in range(25):
        at = click(at, "New Game")
        assert 1 <= at.session_state["secret"] <= 20, (
            f"Easy range is 1-20 but New Game drew {at.session_state['secret']}"
        )
