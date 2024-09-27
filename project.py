import random
import os
import sys
from typing import List, Tuple
from collections import Counter


class GameResponse:
    """
    Contains the possible responses for the game.
    """
    YES = ("y", "yes", "yeah", "yup", "sure", "ok")
    NO = ("n", "no", "nah", "net", "nope")
    EXIT = ("e")


class GameConfig:
    """
    Holds configuration constants for the game settings, including levels, guesses, and limits.
    """
    MIN_GUESSES = 3
    MAX_GUESSES = 99
    MIN_LENGTH = 3
    MAX_LENGTH = 9
    MIN_LIMIT = 3
    MAX_LIMIT = 9
    MIN_LEVEL = 1
    MAX_LEVEL = 9
    MIN_PADDING = 7  # Padding for results table
    NUMERIC_PADDING = 20  # Padding for results table
    PROG_CONDITIONS = (8, 4, 6, True)
    CUSTOM_LEVEL = (0, 0, 0, None)
    DR = 12  # Default guesses
    LEVELS = {
        # Defines each level (guesses, length, limit, duplicates)
        1: (DR, 3, 5, False),
        2: (DR, 3, 5, True),
        3: (DR, 4, 6, False),
        4: (DR, 4, 6, True),  # Standard level
        5: (DR, 4, 8, True),
        6: (DR, 5, 6, True),
        7: (DR, 5, 8, True),
        8: (DR, 6, 8, True),
        9: (DR, 7, 9, True),
    }
    OTHER_LEVEL = {
        "c": 0,  # Custom level
        "p": 10,  # Progressive level
    }

    symbolic = True  # Display type: True=symbols, False=numbers

    @classmethod
    def flip_symbolic(cls):
        """
        Toggles between symbolic and numeric representation of results.
        """
        cls.symbolic = not cls.symbolic


class ColoredText:
    """
    Changes the color of text and makes it bold. Currently only used for title and code in how to play.
    """
    colors = {
        "red": "\033[31m\033[1m",
        "green": "\033[32m\033[1m",
        "yellow": "\033[33m\033[1m",
        "blue": "\033[34m\033[1m",
        "magenta": "\033[35m\033[1m",
        "cyan": "\033[36m\033[1m",
        "white": "\033[37m\033[1m",
        "reset": "\033[0m\033[1m",
    }

    @classmethod
    def print(cls, text, color) -> None:
        color_code = cls.colors.get(color, cls.colors["reset"])
        print(f"{color_code}{text}{cls.colors['reset']}", end="")


def main() -> None:
    """
    Main function to execute the game loop.

    This function handles the game's main logic, including displaying the title,
    retrieving the difficulty level, and executing either a progressive or regular
    game based on user input. It continues to prompt the user to play again until
    they choose not to.

    :returns: None
    :raises ValueError: If an invalid input is encountered when retrieving the game level.
    :raises Exception: For any unexpected errors during game execution.
    """
    print_title()
    continue_playing = True

    while continue_playing:
        try:
            prog_round = None
            level = get_level()

            clear_screen()

            if level == GameConfig.OTHER_LEVEL["p"]:
                code, won, prog_round = progressive_game()
            else:
                code, won = regular_game(level)

            if not won:
                print("Game Over! You failed to guess the code, it was ", *code, sep='')

            if prog_round:
                print(f"You cracked {prog_round} {'code' if prog_round == 1 else 'codes'}")

            continue_playing = input("\nWould you like to play again? ").lower() in GameResponse.YES

            clear_screen()

        except ValueError:
            print("Invalid Input!")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    print("Thank you for playing!\n")


def print_title() -> None:
    """
    Clears the console screen and displays the title screen for the game.

    :returns: None
    """
    clear_screen()
    ColoredText.print(r"""               __  ______  _                 __
              / / / / / /_(_)___ ___  ____ _/ /____
             / / / / / __/ / __ `__ \/ __ `/ __/ _ \
            / /_/ / / /_/ / / / / / / /_/ / /_/  __/
            \____/_/\__/_/_/ /_/ /_/\__,_/\__/\___/

    __  ___           __                      _           __
   /  |/  /___ ______/ /____  _________ ___  (_)___  ____/ /
  / /|_/ / __ `/ ___/ __/ _ \/ ___/ __ `__ \/ / __ \/ __  /
 / /  / / /_/ (__  ) /_/  __/ /  / / / / / / / / / / /_/ /
/_/  /_/\__,_/____/\__/\___/_/  /_/ /_/ /_/_/_/ /_/\__,_/

""", "yellow")


def clear_screen() -> None:
    """
    Clears the console screen based on the operating system.

    :returns: None
    """
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except OSError:
        pass


def get_level() -> int:
    """
    Prompts the user to select a game level, custom level or progressive game mode.

    :returns: The selected level or game type.
    :raises ValueError: If the input is invalid.
    """
    while True:
        try:
            match input("""              1-9) Start a game at that level
                C) Start a custom game
                P) Start a progressive game
                L) Show level information
                ?) How to play
                E) Exit\n
Please select an option: """).strip().lower():
                case "l":
                    print_levels()
                    continue
                case "?":
                    print_how_to()
                    continue
                # Sets the level if the user enters 1-9
                case num if num.isdigit() and GameConfig.MIN_LEVEL <= int(num) <= GameConfig.MAX_LEVEL:
                    return int(num)
                # Sets the level if user enters any other valid level "c" for custom or "p" for progressive
                case key if key in GameConfig.OTHER_LEVEL:
                    return GameConfig.OTHER_LEVEL[key]
                case word if word in GameResponse.EXIT:
                    sys.exit()
                case _:
                    raise ValueError
        except (Exception, ValueError):
            print("Please enter a number between 1-9, 'C' for custom, 'P' for progressive, or '?' for help.")


def print_levels() -> None:
    """
    Clears the console screen and displays information about the
    game levels and their difficulty settings.

    :returns: None
    """
    clear_screen()
    print("""\nThere are 4 variables that can change to make the game more or less difficult:
  Digits: How long is the code. The longer the code the harder it is to solve.
  Numbers: What numbers are allowed in the code. The more numbers the harder it is to solve.
  Duplicates: Can a number be used more than once in a code. No duplicates make the code easier to solve.
  Guesses: How many guesses you have to crack the code for levels 1-9 you always have 12 guesses

LEVELS:""")
    # Gets the level conditions and prints them
    for level, details in GameConfig.LEVELS.items():
        _, length, limit, duplicates = details
        print(f"  {level}) {length} digits of 1-{limit}, {'no duplicates' if not duplicates else 'duplicates allowed'}")
    print("""  C) You choose the length, numbers, rounds, and decide if duplicates are allowed
  P) You start on level 4 but with only 8 guesses and after solving a code you play again. The difficulty
     increases after each win. You play until you fail to guess a code. How long can you last?\n""")


def print_how_to() -> None:
    """
    Clears the console screen and displays instructions on how to play the game.

    :returns: None
    """
    clear_screen()
    print("""\nYou’re goal is to crack a secret code. You will get a number of guesses and after each guess,
you’ll get feedback on how many digits are correct and in the right position, as well as how many correct
digits are in the wrong position. Use this information and make strategic guesses to crack the code.

For example:
 if the secret code was""", end="")
    ColoredText.print(" 6344", "green")
    print(""", the following table displays the response in both symbolic and numeric notation.
+-------+--------+---------------------+----------------------------------------+-----------------------------+
|       |RESPONSE|       RESPONSE      |                                                                      |
| GUESS |SYMBOLIC|        NUMERIC      |                             Explanation                              |
+-------+--------+---------------------+----------------------------------------------------------------------+
|  4522 |   o    | 0:exact 1:misplaced | Only the 4 is in code but it is in the wrong position                |
+----------------+---------------------+----------------------------------------------------------------------+
|  5322 |   *    | 1:exact 0:misplaced | Only the 3 is correct and it is in the correct position              |
+----------------+---------------------+----------------------------------------------------------------------+
|  6422 |   *o   | 1:exact 1:misplaced | 6 is in the correct position, the 4 is in the wrong position         |
+----------------+---------------------+----------------------------------------------------------------------+
|  6442 |  **o   | 2:exact 1:misplaced | The 6 and second 4 are correct; the first 4 is in the wrong position |
+----------------+---------------------+----------------------------------------------------------------------+
|  4444 |   **   | 2:exact 0:misplaced | The last two 4s are correct and in the correct position              |
+----------------+---------------------+----------------------------------------------------------------------+
|  4436 |  oooo  | 0:exact 4:misplaced | All the digits are in the code, but none are in the correct position |
+----------------+---------------------+----------------------------------------------------------------------+
\x1B[3mFor the symbolic response:
    "*" represents the number of correct digits that are in the correct position
    "o" represents how many digits are correct, but in the wrong position\x1B[0m\n""")


def custom_level() -> Tuple[int, int, int, bool]:
    """
    Allows the player to set custom game parameters such as rounds, length, limit, and duplicates.

    :returns: A tuple containing the custom game settings.
    """
    # Sets the following to 0, 0, 0, None
    rounds, length, limit, duplicates = GameConfig.CUSTOM_LEVEL

    # Sets the number of digits in the code
    while length == 0:
        try:
            l = input(F"How many digits({GameConfig.MIN_LENGTH}-{GameConfig.MAX_LENGTH}): ").strip()
            if l.isdigit() and GameConfig.MIN_LENGTH <= int(l) <= GameConfig.MAX_LENGTH:
                length = int(l)
            else:
                raise ValueError
        except (Exception, ValueError):
            print(f"Please enter a number {GameConfig.MIN_LENGTH}-{GameConfig.MAX_LENGTH}.")

    # Sets if duplicates are allowed
    while duplicates is None:
        try:
            min_limit = GameConfig.MIN_LIMIT  # Sets min_limit to 3
            d = input("Duplicates(y/n): ").strip().lower()
            if d in GameResponse.YES:
                duplicates = True
            elif d in GameResponse.NO:  # If Duplicates aren't allowed sets min to the number of digits in the code
                min_limit = length
                duplicates = False
            else:
                raise ValueError
        except (Exception, ValueError):
            print("Please enter y or n.")
    # If the min is equal to 9 set it to 9, which will skip the limit option
    if min_limit == GameConfig.MAX_LIMIT:
        limit = GameConfig.MAX_LIMIT

    # Sets the highest possible number in the code
    while limit == 0:
        try:
            h = input(f"What is the largest each digit could be({min_limit}-{GameConfig.MAX_LIMIT}): ").strip()
            if h.isdigit() and min_limit <= int(h) <= GameConfig.MAX_LIMIT:
                limit = int(h)
            else:
                raise ValueError
        except (Exception, ValueError):
            print(f"Please enter a number {min_limit}-{GameConfig.MAX_LIMIT}.")

    # Sets how many guesses the player gets
    while rounds == 0:
        try:
            r = input(F"How many guesses({GameConfig.MIN_GUESSES}-{GameConfig.MAX_GUESSES}): ").strip()
            if r.isdigit() and GameConfig.MIN_GUESSES <= int(r) <= GameConfig.MAX_GUESSES:
                rounds = int(r)
            else:
                raise ValueError
        except (Exception, ValueError):
            print(f"Please enter a number {GameConfig.MIN_GUESSES}-{GameConfig.MAX_GUESSES}.")

    return rounds, length, limit, duplicates


def progressive_game() -> Tuple[Tuple[int, ...], bool, int]:
    """
    Handles the logic for the progressive game mode, where the difficulty increases after each win.

    :returns: The secret code and a boolean indicating if the game was won.
    """
    prog_round = 1
    won = True
    conditions = GameConfig.PROG_CONDITIONS

    while won:
        print(f"\nRound {prog_round}:", end="")

        code, won = both_games(conditions)

        if won:
            prog_round += 1
            conditions = prog_game_won(conditions, prog_round)
    return code, won, (prog_round - 1)


def regular_game(level: int) -> Tuple[Tuple[int, ...], bool]:
    """
    Handles the logic for the regular game mode.

    :param level: The difficulty level for the game.
    :returns: The secret code and a boolean indicating if the game was won.
    """
    if level == GameConfig.OTHER_LEVEL["c"]:
        conditions = custom_level()
    else:
        conditions = GameConfig.LEVELS[level]

    code, won = both_games(conditions)

    return code, won


def both_games(conditions: Tuple[int, int, int, bool]) -> Tuple[Tuple[int, ...], bool]:
    """
    Manages the game elements common for both regular and progressive modes.

    :param conditions: The game settings (guesses, length, limit, duplicates).
    :returns: The secret code and a boolean indicating if the game was won.
    """
    guesses, length, limit, duplicates = conditions

    code = gen_code(conditions)

    print(f"\nYou have {guesses} attempts to guess a {length}-digit code composed of numbers 1-{limit}, {'with repeated numbers allowed.' if duplicates else 'with no repeated numbers.'} \n")

    won, tries = gameplay(conditions, code)

    if won:
        print(f"You guessed the code in {tries} tries.")

    return code, won


def gen_code(conditions: Tuple[int, int, int, bool]) -> Tuple[int, ...]:
    """
    Generates a secret code based on the game conditions.

    :param conditions: The game settings (guesses, length, limit, duplicates).
    :returns: A tuple representing the generated secret code.
    """
    _, length, limit, duplicates = conditions

    if duplicates:

        return tuple(random.randrange(1, (limit + 1)) for _ in range(length))
    else:
        return tuple(random.sample(range(1, limit + 1), length))


def gameplay(conditions: Tuple[int, int, int, bool], code: Tuple[int, ...]) -> Tuple[bool, int]:
    """
    Main loop for the game, prompts the user for guesses, checks guess against the secret code and displays they results.

    :param conditions: The game conditions (guesses, length, limit, duplicates).
    :param code: The secret code to be guessed.
    :returns: A boolean indicating if the game was won and the number of tries taken.
    """
    remaining_guesses, _, limit, _ = conditions
    data: list = []

    while True:

        remaining_guesses -= 1

        guess = get_guess(data, limit, len(code), remaining_guesses)
        guessed = [int(n) for n in str(guess)]

        exact, misplaced = check(code, guessed)

        data.append((guess, exact, misplaced))
        display_table(data, remaining_guesses, limit)

        if exact == len(code):
            display_table(data, remaining_guesses, limit, hide=True)
            return True, (conditions[0] - remaining_guesses)

        if remaining_guesses == 0:
            return False, 0


def get_guess(data: list[Tuple[int, ...]], limit: int, code_length: int, remaining_guesses: int) -> str:
    """
    Prompts the user for a guess and validates the input.

    :param data: The previous guesses and their results.
    :param limit: The maximum digit value allowed in the guess.
    :param code_length: The required length of the guess.
    :param guesses: The number of guesses remaining.
    :returns: A valid guess input by the user.
    """
    while True:
        try:
            guess = input("guess: ").replace(" ", "")
            if guess.lower() == "r" and data:
                GameConfig.flip_symbolic()
                display_table(data, (remaining_guesses + 1), limit)
                continue
            if guess.lower() in GameResponse.EXIT:
                sys.exit()
            if not guess.isdigit():
                print("Invalid guess! Please enter only numbers.")
                continue
            if ("0" in guess) or any(int(x) > limit for x in guess):
                print(f"Invalid guess! Please enter only numbers between 1 and {limit}.")
                continue
            if len(guess) != code_length:
                print(f"Invalid guess! Please enter exactly {code_length} digits")
                continue
            return guess
        except (Exception, ValueError):
            print("Invalid guess!")


def check(code: Tuple[int, ...], guess: List[int]) -> Tuple[int, int]:
    """
    Checks the guessed code against the secret code and returns the results.

    :param code: The secret code.
    :param guess: The guessed code.
    :returns: A tuple with counts of exact matches and misplaced matches.
    """
    exact = sum(g == c for g, c in zip(guess, code))

    code_counter = Counter(code)
    guess_counter = Counter(guess)

    total_matches = sum((code_counter & guess_counter).values())

    misplaced = total_matches - exact

    return exact, misplaced


def display_table(data: List[Tuple[int, ...]], remaining_guesses: int, limit: int, hide: bool = False) -> None:
    """
     Clears the console screen and displays a table of guesses and results.

    :param data: The previous guesses and their results.
    :param guesses: The number of guesses remaining.
    :param limit: The maximum digit value allowed.
    :param subtract: Adjusts the displayed number of remaining guesses.
    :param hide: If True, hides the detailed results.
    :returns: None
    """
    clear_screen()
    min_padding = GameConfig.MIN_PADDING
    digits = len(str(data[0][0]))
    guess_padding = max(digits, min_padding)

    if GameConfig.symbolic:
        results_padding = guess_padding
        print("Enter 'r' to switch results to show numbers (*=Exact o=Misplaced)") if not hide else None
    else:
        results_padding = GameConfig.NUMERIC_PADDING
        print("Enter 'r' to switch results to show symbols") if not hide else None

    print(f"+-{'-'*guess_padding}---{'-'*results_padding}-+")
    print(f"| {'GUESS':^{guess_padding}} | {'RESULTS':^{results_padding}} |")
    print(f"+-{'-'*guess_padding}---{'-'*results_padding}-+")
    for guess, exact, misplaced in data:
        if GameConfig.symbolic:
            results = '*' * exact + 'o' * misplaced
        else:
            results = f'{exact}:exact  {misplaced}:misplaced'
        print(f"| {guess:^{guess_padding}} | {results:^{results_padding}} |")
        print(f"+-{'-'*guess_padding}---{'-'*results_padding}-+")
    if not hide and remaining_guesses > 0:
        print("\033[93mLast Chance!\033[0m" if remaining_guesses == 1 else f"{remaining_guesses} guesses:", end="")
        print(f" {digits} digits(1-{limit})")


def prog_game_won(conditions: Tuple[int, int, int, bool], round: int) -> Tuple[int, int, int, bool]:
    """
    Adjusts the game conditions after each win in progressive mode.

    :param conditions: The game conditions (guesses, length, limit, duplicates).
    :param round_num: The current round number.
    :returns: The game conditions for the next round.
    """
    guesses, length, limit, duplicates = conditions

    if round % 2 == 0:
        guesses += 1
    if limit == GameConfig.MAX_LIMIT and length >= GameConfig.MAX_LIMIT - 1:
        length += 1
        guesses += 2
    elif limit == GameConfig.MAX_LIMIT:
        length += 1
        limit = length + 1
        guesses += 2
    else:
        limit += 1
    return (guesses, length, limit, duplicates)


if __name__ == "__main__":
    main()
