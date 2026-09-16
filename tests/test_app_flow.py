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


def test_a_fresh_game_has_used_no_attempts():
    at = start_app()
    assert at.session_state["attempts"] == 0


def test_a_fresh_normal_game_offers_all_eight_attempts():
    at = start_app()
    assert "Attempts left: 8" in at.info[0].value


def test_an_empty_guess_does_not_cost_an_attempt():
    at = start_app()
    at = guess(at, "")
    assert at.session_state["attempts"] == 0


def test_an_unparseable_guess_does_not_cost_an_attempt():
    at = start_app()
    at = guess(at, "abc")
    assert at.session_state["attempts"] == 0
    assert at.error[0].value == "That is not a number."


def test_a_valid_guess_costs_exactly_one_attempt():
    at = start_app(secret=50)
    at = guess(at, 10)
    assert at.session_state["attempts"] == 1


def test_normal_difficulty_allows_eight_real_guesses():
    at = start_app(secret=50)

    for n, wrong in enumerate([10, 11, 12, 13, 14, 15, 16], start=1):
        at = guess(at, wrong)
        assert at.session_state["status"] == "playing", (
            f"game ended after only {n} guesses"
        )

    at = guess(at, 17)
    assert at.session_state["status"] == "lost"
