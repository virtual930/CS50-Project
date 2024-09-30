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
    EXIT = "end"


class Mastermind:
    """
    Holds configuration constants for the game settings, including levels, guesses, and limits.
    """
    MIN_GUESSES = 3
    MAX_GUESSES = 99
    MIN_LENGTH = 3
    MAX_LENGTH = 9
    MIN_LIMIT = 3
    MAX_LIMIT = 9
    MIN_REPEATED = 2
    MIN_PADDING = 7  # Padding for results table
    NUMERIC_PADDING = 20  # Padding for results table
    PROG_CONDITIONS = (8, 4, 6, True)
    CUSTOM_LEVEL = (0, 0, 0, None)
    DR = 12  # Default guesses
    MIN_LEVEL = 1
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
    MAX_LEVEL = 9
    OTHER_LEVELS = {
        "c": 0,  # Custom level
        "p": 99,  # Progressive level
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
        "reset": "\033[0m",
    }

    @classmethod
    def print(cls, text, color) -> None:
        color_code = cls.colors.get(color, cls.colors["reset"])
        print(f"{color_code}{text}{cls.colors['reset']}", end="")


def main() -> None:
    """
    Run the main game loop.

    This function orchestrates the primary game flow, which includes:
    - Displaying the game title.
    - Retrieving the difficulty level from the user.
    - Executing either a progressive or regular game based on the selected level.
    - Continuously prompting the user to play again until they opt out.

    :returns: None
    :raises EOFError: If end-of-file is reached during input.
    :raises ValueError: If the user provides an invalid input while selecting the game level.
    :raises Exception: For any unexpected errors that occur during game execution.
    """
    print_title()
    continue_playing = True

    while continue_playing:
        try:
            prog_round = None
            level = get_level()

            clear_screen()

            if level == Mastermind.OTHER_LEVELS["p"]:
                code, won, prog_round = progressive_game()
            else:
                code, won = regular_game(level)

            if not won:
                print(" Game Over! You failed to guess the code, it was ", *code, sep='')

            if prog_round:
                print(f" You cracked {prog_round} {'code' if prog_round == 1 else 'codes'}")

            while True:
                try:
                    confirm = input("\n Would you like to play again? (y/n): ").lower()
                    if confirm and confirm in GameResponse.NO:
                        continue_playing = False
                        break
                    elif confirm and confirm in GameResponse.YES:
                        break
                    else:
                        print(" Please enter 'y' or 'n'")
                        continue
                except KeyboardInterrupt:
                    print(" Input was cancelled.")
                except EOFError:
                    print(" Exiting due to EOF.")
                    sys.exit()
                except ValueError:
                    print(" Invalid Input!")

            clear_screen()
        except Exception as e:
            print(f" An unexpected error occurred: {e}")

    print(" Thank you for playing!\n")


def print_title() -> None:
    """
    Clears the console screen and displays the title screen for the game.

    :returns: None
    """
    clear_screen()
    ColoredText.print(r"""                __  ______  _                 __
               / / / / / /_(_)___ ___  ____ _/ /____
              / / / / / __/ / __ `__ \/ __ `/ __/ _ \
             / /_/ / / /_/ / / / / / / /_/ / /_/  __/
             \____/_/\__/_/_/ /_/ /_/\__,_/\__/\___/
 
     __  ___           __                      _           __
    /  |/  /___ ______/ /____  _________ ___  (_)___  ____/ /
   / /|_/ / __ `/ ___/ __/ _ \/ ___/ __ `__ \/ / __ \/ __  /
  / /  / / /_/ (__  ) /_/  __/ /  / / / / / / / / / / /_/ /
 /_/  /_/\__,_/____/\__/\___/_/  /_/ /_/ /_/_/_/ /_/\__,_/
""", "cyan")


def clear_screen() -> None:
    """
    Clears the console screen based on the operating system.

    :returns: None
    """
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except OSError:
        pass
    print()

def get_level() -> int:
    """
    Prompts the user to select a game level, custom level or progressive game mode.

    :returns: The selected level or game type.
    :raises ValueError: If the input is invalid.
  """
    print_title()
    print_menu()
    while True:

        try:
            match input(" Please select an option: ").strip().lower():
                case "l":
                    print_levels()
                    continue
                case "?":
                    print_how_to()
                    continue
                case "":
                    raise ValueError
                # Sets the level if the user enters 1-9
                case number if number.isdigit() and int(number) in Mastermind.LEVELS:
                    return int(number)
                # Sets the level if user enters any other valid level "c" for custom or "p" for progressive
                case key if key in Mastermind.OTHER_LEVELS:
                    return Mastermind.OTHER_LEVELS[key]
                case word if word in GameResponse.EXIT:
                    exit_game()
                    continue
                case _:
                    raise ValueError
        except ValueError:
            print(f"\n Please enter a number between {Mastermind.MIN_LEVEL}-{Mastermind.MAX_LEVEL}, 'C' for custom, 'P' for progressive, '?' for help or 'end' to exit")
        except KeyboardInterrupt:
            print(" Input was cancelled.")
        except EOFError:
            print(" Exiting due to EOF.")
            sys.exit()


def print_menu():

    print(f"""            ┌─────┬────────────────────────────┐
            │ OPT │       DESCRIPTION          │
            ├─────┼────────────────────────────┤
            │ \033[36m{Mastermind.MIN_LEVEL}-{Mastermind.MAX_LEVEL}\033[0m │ \033[36mStart a game at that level\033[0m │
            │  \033[33mC\033[0m  │ \033[33mStart a custom game\033[0m        │
            │  \033[36mP\033[0m  │ \033[36mStart a progressive game\033[0m   │
            │  \033[33mL\033[0m  │ \033[33mShow Level Information\033[0m     │
            │  \033[36m?\033[0m  │ \033[36mHow to play\033[0m                │
            │ \033[33mend\033[0m │ \033[33mEnd program\033[0m                │
            └─────┴────────────────────────────┘""")

def print_levels() -> None:
    """
    Clears the console screen and displays information about the
    game levels and their difficulty settings.

    :returns: None
    """
    clear_screen()
    print(f""" There are 4 variables that can change to make the game more or less difficult:
   Guesses: How many guesses you have to crack the code for levels {Mastermind.MIN_LEVEL}-{Mastermind.MAX_LEVEL} you always have 12 guesses
   Digits: How long is the code. The longer the code the harder it is to solve.
   Numbers: What numbers are allowed in the code. The more numbers the harder it is to solve.
   Duplicates: Can a number be used more than once in a code. No duplicates make the code easier to solve.
     \x1B[3m*If duplicates are allowed in games with a 3-5 digit code a number can only be repeated at most twice. In games with 6+ digit codes
     a number cannot appear more than half the length of the code. For example, in a 7-digit code, a number can appear at most three times.

 LEVELS:""")
    # Gets the level conditions and prints them
    for level, details in Mastermind.LEVELS.items():
        _, length, limit, duplicates = details
        print(f"   {level}) {length} digits of 1-{limit}, {'no duplicates' if not duplicates else 'duplicates allowed'}")
    print("""   C) You choose the length, numbers, rounds, and decide if duplicates are allowed
   P) You start on level 4 but with only 8 guesses and after solving a code you play again. The difficulty
      increases after each win. You play until you fail to guess a code. How long can you last?\x1B[0m""")
    print_menu()

def print_how_to() -> None:
    """
    Clears the console screen and displays instructions on how to play the game.

    :returns: None
    """
    clear_screen()
    print(""" You’re goal is to crack a secret code. You will get a number of guesses and after each guess,
 you’ll get feedback on how many digits are correct and in the right position, as well as how many correct
 digits are in the wrong position. Use this information and make strategic guesses to crack the code.

 For example:
  if the secret code was""", end="")
    ColoredText.print(" 6344", "green")
    print(""", the following table displays the response in both symbolic and numeric notation.
 ┌───────┬────────┬─────────────────────┬──────────────────────────────────────────────────────────────────────┐
 │       │RESPONSE│       RESPONSE      │                                                                      │
 │ GUESS │SYMBOLIC│        NUMERIC      │                             Explanation                              │
 ├───────┼────────┼─────────────────────┼──────────────────────────────────────────────────────────────────────┤
 │  4522 │   o    │ 0:exact 1:misplaced │ Only the 4 is in code but it is in the wrong position                │
 ├───────┼────────┼─────────────────────┼──────────────────────────────────────────────────────────────────────┤
 │  5322 │   *    │ 1:exact 0:misplaced │ Only the 3 is correct and it is in the correct position              │
 ├───────┼────────┼─────────────────────┼──────────────────────────────────────────────────────────────────────┤
 │  6422 │   *o   │ 1:exact 1:misplaced │ 6 is in the correct position, the 4 is in the wrong position         │
 ├───────┼────────┼─────────────────────┼──────────────────────────────────────────────────────────────────────┤
 │  6442 │  **o   │ 2:exact 1:misplaced │ The 6 and second 4 are correct; the first 4 is in the wrong position │
 ├───────┼────────┼─────────────────────┼──────────────────────────────────────────────────────────────────────┤
 │  4444 │   **   │ 2:exact 0:misplaced │ The last two 4s are correct and in the correct position              │
 ├───────┼────────┼─────────────────────┼──────────────────────────────────────────────────────────────────────┤
 │  4436 │  oooo  │ 0:exact 4:misplaced │ All the digits are in the code, but none are in the correct position │
 └───────┴────────┴─────────────────────┴──────────────────────────────────────────────────────────────────────┘
 \x1B[3mFor the symbolic response:
     "*" represents the number of correct digits that are in the correct position
     "o" represents how many digits are correct, but in the wrong position\x1B[0m""")
    print_menu()



def custom_level() -> Tuple[int, int, int, bool]:
    """
    Allows the player to set custom game parameters such as rounds, length, limit, and duplicates.

    :returns: A tuple containing the custom game settings.
    """
    # Sets the following to 0, 0, 0, None
    rounds, length, limit, duplicates = Mastermind.CUSTOM_LEVEL

    # Sets the number of digits in the code
    while length == 0:
        try:
            l = input(F" How many digits({Mastermind.MIN_LENGTH}-{Mastermind.MAX_LENGTH}): ").strip()
            if l.isdigit() and Mastermind.MIN_LENGTH <= int(l) <= Mastermind.MAX_LENGTH:
                length = int(l)
            else:
                raise ValueError(f" Please enter a number between {Mastermind.MIN_LENGTH}-{Mastermind.MAX_LENGTH}.")
        except ValueError as e:
            print(e)

    # Sets if duplicates are allowed
    min_limit = Mastermind.MIN_LIMIT  # Sets min_limit to 3
    while duplicates is None:
        try:
            d = input(" Duplicates(y/n): ").strip().lower()
            if d in GameResponse.YES:
                duplicates = True
            elif d in GameResponse.NO:  # If Duplicates aren't allowed sets min to the number of digits in the code
                min_limit = length
                duplicates = False
            else:
                raise ValueError(" Please enter y or n.")
        except ValueError as e:
            print(e)

    # If the min is equal to 9 set it to 9, which will skip the limit option
    if min_limit == Mastermind.MAX_LIMIT:
        limit = Mastermind.MAX_LIMIT

    # Sets the highest possible number in the code
    while limit == 0:
        try:
            h = input(f" What is the largest each digit could be({min_limit}-{Mastermind.MAX_LIMIT}): ").strip()
            if h.isdigit() and min_limit <= int(h) <= Mastermind.MAX_LIMIT:
                limit = int(h)
            else:
                raise ValueError(f" Please enter a number between {min_limit}-{Mastermind.MAX_LIMIT}.")
        except ValueError as e:
            print(e)

    # Sets how many guesses the player gets
    while rounds == 0:
        try:
            r = input(F" How many guesses({Mastermind.MIN_GUESSES}-{Mastermind.MAX_GUESSES}): ").strip()
            if r.isdigit() and Mastermind.MIN_GUESSES <= int(r) <= Mastermind.MAX_GUESSES:
                rounds = int(r)
            else:
                raise ValueError(f" Please enter a number between{Mastermind.MIN_GUESSES}-{Mastermind.MAX_GUESSES}.")
        except ValueError as e:
            print(e)

    return rounds, length, limit, duplicates


def exit_game():
    """
    Prompt the user to confirm whether they want to exit the game.

    This function enters a loop asking the user to confirm their desire
    to exit. If the user responds with 'y' or any affirmative response
    defined in GameResponse.YES, the program will terminate. If the user
    responds with 'n' or any response defined in GameResponse.NO,
    the function will return and allow the user to continue playing.

    :raises SystemExit: If the user confirms they want to exit the game.
    """
    while True:
        confirm = input(" Are you sure you want to exit? (y/n): ").lower()
        if confirm and confirm in GameResponse.NO:
            return
        elif confirm and confirm in GameResponse.YES:
            sys.exit()


def progressive_game() -> Tuple[Tuple[int, ...], bool, int]:
    """
    Handles the logic for the progressive game mode, where the difficulty increases after each win.

    :returns: The secret code and a boolean indicating if the game was won.
    """
    prog_round = 1
    won = True
    conditions = Mastermind.PROG_CONDITIONS

    while won:
        print(f"\n Round {prog_round}:", end="")

        code, won = both_games(conditions)

        prog_round += 1
        conditions = prog_game_won(conditions, prog_round)

        if not won:
            return code, won, (prog_round - 1)


def regular_game(level: int) -> Tuple[Tuple[int, ...], bool]:
    """
    Handles the logic for the regular game mode.

    :param level: The difficulty level for the game.
    :returns: The secret code and a boolean indicating if the game was won.
    """
    if level == Mastermind.OTHER_LEVELS["c"]:
        conditions = custom_level()
    else:
        conditions = Mastermind.LEVELS[level]

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

    print(f"\n You have {guesses} attempts to guess a {length}-digit code composed of numbers 1-{limit}, {'with repeated numbers allowed.' if duplicates else 'with no repeated numbers.'} \n")

    won, tries = gameplay(conditions, code)

    if won:
        print(f" You guessed the code in {tries} tries.")

    return code, won


def gen_code(conditions: Tuple[int, int, int, bool]) -> Tuple[int, ...]:
    """
    Generates a secret code based on the game conditions.

    :param conditions: The game settings (guesses, length, limit, duplicates).
    :returns: A tuple representing the generated secret code.
    """
    _, length, limit, duplicates = conditions

    if duplicates:
        half = max(length // 2, Mastermind.MIN_REPEATED)
        # Create a list with each number from 1 to limit appearing half of the length rounded down
        numbers = [num for num in range(1, (limit + 1)) for _ in range(half)]
        # Shuffle the numbers to randomize their order
        random.shuffle(numbers)
        # Select the numbers from the start of the shuffled list until there's an equal amount to the length and convert to a tuple
        return tuple(numbers[:length])
        # Previous version:
        #   return tuple(random.randrange(1, (limit + 1)) for _ in range(length))
    else:
        return tuple(random.sample(range(1, limit + 1), length))


def gameplay(conditions: Tuple[int, int, int, bool], code: Tuple[int, ...]) -> Tuple[bool, int]:
    """
    Main loop for the game, prompts the user for guesses, checks guess against the secret code and displays the results.

    :param conditions: The game conditions (guesses, length, limit, duplicates).
    :param code: The secret code to be guessed.
    :returns: A boolean indicating if the game was won and the number of tries taken.
    """
    remaining_guesses, _, limit, _ = conditions
    data: list = []

    while remaining_guesses > 0:
        remaining_guesses -= 1

        guess = get_guess(data, limit, len(code), remaining_guesses)
        guessed = [int(n) for n in str(guess)]

        exact, misplaced = check(code, guessed)

        data.append((guess, exact, misplaced))
        display_table(data, remaining_guesses, limit)

        if exact == len(code):
            display_table(data, remaining_guesses, limit, hide=True)
            return True, (conditions[0] - remaining_guesses)
    return False, 0


def get_guess(data: list[Tuple[int, ...]], limit: int, code_length: int, remaining_guesses: int) -> str:
    """
    Prompts the user for a guess and validates the input.

    :param data: The previous guesses and their results.
    :param limit: The maximum digit value allowed in the guess.
    :param code_length: The required length of the guess.
    :param remaining_guesses: The number of guesses remaining.
    :returns: A valid guess input by the user.
    """
    while True:
        try:
            guess = input(" guess: ").replace(" ", "")
            if guess.lower() == "r" and data:
                Mastermind.flip_symbolic()
                display_table(data, (remaining_guesses + 1), limit)
                continue
            if not guess:
                print(" Invalid guess! Must enter numbers.")
                continue
            if guess.lower() in GameResponse.EXIT:
                exit_game()
                continue
            if not guess.isdigit():
                print(" Invalid guess! Please enter only numbers.")
                continue
            if ("0" in guess) or any(int(x) > limit for x in guess):
                print(f" Invalid guess! Please enter only numbers between 1 and {limit}.")
                continue
            if len(guess) != code_length:
                print(f" Invalid guess! Please enter exactly {code_length} digits")
                continue
            return guess
        except KeyboardInterrupt:
            print(" Input was cancelled.")
        except EOFError:
            print(" Exiting due to EOF.")
            sys.exit()
        except ValueError:
            print(" Invalid guess!")


def check(code: Tuple[int, ...], guess: List[int]) -> Tuple[int, int]:
    """
    Checks the guessed code against the secret code and returns the results.

    :param code: The secret code.
    :param guess: The guessed code.
    :returns: A tuple with counts of exact matches and misplaced matches.
    """
    exact = sum(g == c for g, c in zip(guess, code))
    total_matches = sum((Counter(code) & Counter(guess)).values())
    misplaced = total_matches - exact

    return exact, misplaced


def display_table(data: List[Tuple[int, ...]], remaining_guesses: int, limit: int, hide: bool = False) -> None:
    """
     Clears the console screen and displays a table of guesses and results.

    :param data: The previous guesses and their results.
    :param remaining_guesses: The number of guesses remaining.
    :param limit: The maximum digit value allowed.
    :param hide: If True, hides the detailed results.
    :returns: None
    """
    clear_screen()
    min_padding = Mastermind.MIN_PADDING
    digits = len(str(data[0][0]))
    guess_padding = max(digits, min_padding)

    if Mastermind.symbolic:
        results_padding = guess_padding
        print(" Enter 'r' to switch results to show numbers (*=Exact o=Misplaced)") if not hide else None
    else:
        results_padding = Mastermind.NUMERIC_PADDING
        print(" Enter 'r' to switch results to show symbols") if not hide else None

    print(f" ┌─{'─'*guess_padding}─┬─{'─'*results_padding}─┐")
    print(f" │ {'GUESS':^{guess_padding}} | {'RESULTS':^{results_padding}} │")
    for guess, exact, misplaced in data:
        if Mastermind.symbolic:
            results = '*' * exact + 'o' * misplaced
        else:
            results = f'{exact}:exact  {misplaced}:misplaced'
        print(f" ├─{'─'*guess_padding}─┼─{'─'*results_padding}─┤")
        print(f" │ {guess:^{guess_padding}} │ {results:^{results_padding}} │")

    print(f" └─{'─'*guess_padding}─┴─{'─'*results_padding}─┘")
    if not hide and remaining_guesses > 0:
        print(" \033[93mLast Chance!\033[0m" if remaining_guesses == 1 else f" {remaining_guesses} guesses:", end="")
        print(f" {digits} digits(1-{limit})")


def prog_game_won(conditions: Tuple[int, int, int, bool], round_num: int) -> Tuple[int, int, int, bool]:
    """
    Adjusts the game conditions after each win in progressive mode.

    :param conditions: The game conditions (guesses, length, limit, duplicates).
    :param round_num: The current round number.
    :returns: The game conditions for the next round.
    """
    guesses, length, limit, duplicates = conditions

    if round_num % 2 == 0:
        guesses += 1
    if limit == Mastermind.MAX_LIMIT and length >= Mastermind.MAX_LIMIT - 1:
        length += 1
        guesses += 2
    elif limit == Mastermind.MAX_LIMIT:
        length += 1
        limit = length + 1
        guesses += 2
    else:
        limit += 1

    return guesses, length, limit, duplicates


if __name__ == "__main__":
    main()
