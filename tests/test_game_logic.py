from logic_utils import check_guess


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


def test_too_high_tells_player_to_go_lower():
    # Bug: a guess above the secret told the player to go HIGHER.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_too_low_tells_player_to_go_higher():
    # Bug: a guess below the secret told the player to go LOWER.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"


def test_single_digit_guess_below_a_string_secret_is_too_low():
    # Bug: the string fallback compared "9" > "50" lexicographically and called
    # a guess of 9 "Too High". Comparison must always be numeric.
    assert check_guess(9, "50") == ("Too Low", "📈 Go HIGHER!")


def test_string_secret_is_compared_numerically():
    assert check_guess(60, "50") == ("Too High", "📉 Go LOWER!")
    assert check_guess(40, "50") == ("Too Low", "📈 Go HIGHER!")
    assert check_guess(50, "50") == ("Win", "🎉 Correct!")


def test_three_digit_guess_above_a_string_secret_is_too_high():
    # "100" < "99" lexicographically, so this was reported as "Too Low".
    assert check_guess(100, "99") == ("Too High", "📉 Go LOWER!")
