from project import get_level, custom_level, gen_code, check, prog_game_won
import itertools


def test_get_level(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda x: "p")
    assert get_level() == 10

    monkeypatch.setattr("builtins.input", lambda x: "c")
    assert get_level() == 0

    monkeypatch.setattr("builtins.input", lambda x: "1")
    assert get_level() == 1

    inputs = iter(["x", "3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = get_level()
    assert result == 3


def test_custom_level(monkeypatch):
    inputs = iter(["3", "y", "4", "5",])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = custom_level()
    assert result == (5, 3, 4, True)

    inputs = iter(["3", "n", "4", "5",])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = custom_level()
    assert result == (5, 3, 4, False)

    inputs = iter(["9", "n", "5",])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = custom_level()
    assert result == (5, 9, 9, False)

    inputs = iter(["x", "3", "x", "n", "x", "4", "x", "5",])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = custom_level()
    assert result == (5, 3, 4, False)


def test_gen_code():
    conditions = (12, 3, 1, True)
    assert gen_code(conditions) == (1, 1, 1)
    conditions = (12, 5, 1, True)
    assert gen_code(conditions) == (1, 1, 1, 1, 1)
    conditions = (12, 9, 1, True)
    assert gen_code(conditions) == (1, 1, 1, 1, 1, 1, 1, 1, 1)
    conditions = (12, 3, 3, False)
    expected_results = {tuple(perm) for perm in itertools.permutations((1, 2, 3))}
    assert tuple(gen_code(conditions)) in expected_results


def test_check():
    assert check([1, 1, 1], [0, 0, 0]) == (0, 0)
    assert check([1, 1, 1], [1, 1, 1]) == (3, 0)
    assert check([1, 1, 0], [1, 1, 1]) == (2, 0)
    assert check([1, 1, 1], [1, 1, 0]) == (2, 0)
    assert check([1, 1, 0, 0], [0, 0, 1, 1]) == (0, 4)
    assert check([1, 1, 0, 0], [0, 1, 1, 0]) == (2, 2)
    assert check([1, 2, 2, 2], [0, 2, 0, 0]) == (1, 0)
    assert check([1, 2, 2, 2], [1, 1, 1, 0]) == (1, 0)
    assert check([1, 2, 2, 2], [0, 1, 1, 1]) == (0, 1)


def test_prog_game_won1():
    conditions = (8, 8, 9, True)
    assert prog_game_won(conditions, 1) == (10, 9, 9, True)
    assert prog_game_won(conditions, 2) == (11, 9, 9, True)
    conditions = (8, 9, 9, True)
    assert prog_game_won(conditions, 1) == (10, 10, 9, True)
    assert prog_game_won(conditions, 2) == (11, 10, 9, True)
    conditions = (8, 4, 9, True)
    assert prog_game_won(conditions, 1) == (10, 5, 6, True)
    assert prog_game_won(conditions, 2) == (11, 5, 6, True)
    conditions = (8, 4, 6, True)
    assert prog_game_won(conditions, 1) == (8, 4, 7, True)
    assert prog_game_won(conditions, 2) == (9, 4, 7, True)
