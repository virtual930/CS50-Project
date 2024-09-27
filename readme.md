# CS50P Final Project: Ultimate Mastermind

#### Video Demo:  <URL HERE>

#### Description:

**Ultimate Mastermind**, a fun and challenging code-breaking game where you try to guess a hidden code! This project is built in Python and features various difficulty levels, including custom and progressive modes.

## Table of Contents

- [Features](#features)
- [How to Play](#how-to-play)
- [Preset Game Levels](#preset-game-levels)
- [Custom Level](#custom-level)
- [Progressive Mode](#progressive-mode)
- [Toggle Results](#toggle-results)
- [Structure](#structure)
- [project.py Classes and Functions](#project.py-Classes-and-Functions)



## Features

- Multiple game levels with varying difficulty.
- Custom level creation for personalized gameplay.
- Progressive game mode that increases difficulty after each win.
- Option to display results as symbols or as numbers



## How to Play

You’re goal is to crack a secret code. You will get a number of guesses and after each guess,
you’ll get feedback on how many digits are correct and in the right position, as well as how many correct
digits are in the wrong position. Use this information and make strategic guesses to crack the code.

For example:<br>
 if the secret code was 6344, the following table displays the response in both symbolic and numeric notation.
|GUESS|SYMBOLIC|NUMERIC|Explanation|
| :---: | :---: | :---: | :---: |
|4522|o| :exact 1:misplaced|Only the 4 is in code but it is in the wrong position|
|5322|*|1:exact 0:misplaced|Only the 3 is correct and it is in the correct position|
|6422|*o|1:exact 1:misplaced|6 is in the correct position, the 4 is in the wrong position|
|6442|**o|2:exact 1:misplaced|The 6 and second 4 are correct; the first 4 is in the wrong position |
|4444|**|2:exact 0:misplaced|The last two 4s are correct and in the correct position|
|4436|oooo|0:exact 4:misplaced| All the digits are in the code, but none are in the correct position|

*For the symbolic response:<br>
&emsp;"\*" represents the number of correct digits that are in the correct position<br>
&emsp;"o" represents how many digits are correct, but in the wrong position*

## Preset Game Levels

1\) 3 digits of 1-5, no duplicates<br>
2:\) 3 digits of 1-5, duplicates allowed<br>
3:\) 4 digits of 1-6, no duplicates<br>
4:\) 4 digits of 1-6, duplicates allowed<br>
5:\) 4 digits of 1-8, duplicates allowed<br>
6:\) 5 digits of 1-6, duplicates allowed<br>
7:\) 5 digits of 1-8, duplicates allowed<br>
8:\) 6 digits of 1-8, duplicates allowed<br>
9:\) 7 digits of 1-9, duplicates allowed<br>


## Custom Level

In the custom level setup, you can define:
- The number of digits in the code.
- The maximum value for each digit.
- Whether duplicates are allowed.
- The number of guesses allowed.


## Progressive Mode

You begin at level 4 with just 8 guesses. After successfully cracking a code, you continue to play, with the difficulty escalating after each victory. You'll keep playing until you can no longer guess a code within the given attempts. How long can you last?


## Toggle Results
Instead of entering a guess you can enter "r" this will toggle the results between symbolic and numeric notation in the results table.

Symbolic Notation:<br>
| GUESS |RESPONSE|
| :-----: | :-------: |
|  6442 |  **o   |
|  4444 |   **   |
|  4436 |  oooo  |

Numeric  Notation:<br>
|GUESS|RESPONSE|
| :-----: | :-------: |
|6442|2:exact 1:misplaced|<br>
|4444|2:exact 0:misplaced|
|4436|0:exact 4:misplaced|



## Structure

The project is structured as follows:

- `project.py`: Contains the main function and additional functions related to the project.
- `test_project.py`: Contains test functions for the additional functions in `project.py`.
- `README.md`: This README file explaining the project and its usage.


## project.py Classes and Functions

#### class GameResponse
* Contains the possible responses for the game.

#### class GameConfig
* Holds configuration constants for the game settings, including levels, rounds, and limits.<br>
Note: *One thing that still needs a little bit of work is the levels. I plan to go in and tweak them a bit for better variety.*

#### class ColoredText
* Changes the color of text and makes it bold.<br>
Note: *Currently only used for title and code in how to play.*

#### main
* Main function to execute the game loop.
This function handles the game's main logic, including displaying the title(print_title function), retrieving the difficulty level, and executing either a progressive or regular game based on user input(get_level function). it initiates either a progress game(progressive_game function) or a regular/custom game(regular_game function) and after each game prompts the user to play again until they choose not to.

#### print_title
* Displays the title screen for the game.

#### clear_screen
* Clears the console screen based on the operating system.

#### get_level
* Prompts the user to select a game level, custom level or progressive game mode.

#### print_levels
* Displays information about the game levels and their difficulty settings.

#### print_how_to
* Displays instructions on how to play the game.

#### custom_level
* Allows the player to set custom game parameters such as rounds, length, limit, and duplicates.

#### progressive_game
* Handles the logic for the progressive game mode, where the difficulty increases after each win. Sets the conditions for the first round and prints the rounds. If the player cracks the code it then increases the difficulty(prog_won function).<br>
Note: *This is my favorite feature in this project. When I came up with the idea for this mode I couldn't wait to implement it. I had played many version of mastermind where you could change the difficulty, but I had never played one that ramped up the difficulty each time you won. I haven't had a chance to fully play this mode yet except for a few rounds for testing, but I can't wait to see how far I can get.*

#### regular_game
* Handles the logic for the regular and custom game modes. If it is a custom game it prompts the user for conditions(custom_level function) else it sets the conditions based on the level the player chose.

#### both_games
* Manages the game elements common for both regular and progressive modes. Generates the code(gen_code function), prints the game conditions and if the game was won it prints the number of guesses it took.<br>
Note: *This previously handled both the progressive and regular games, but I decided to split it into 3 functions in case I wanted to add more game modes or expand upon the existing ones*

#### gen_code
* Generates a secret code based on the game conditions.<br>
Note: *This previously used a for loop that compared the guess with a copy of the code and removed any matches. It was revised to use zip and counter instead. I felt it was a slightly better solution*

#### gameplay
* Main loop for the game, prompts the user for guesses(get_guess function), checks the guess against the secret code(check function) and displays the results(display_table function).

#### get_guess
* Prompts the user for a guess and validates the input.

#### check
* Checks the guessed code against the secret code and returns the results.<br>
Note: *This previously used a for loop that compared the guess with a copy of the code and removed any matches from the copy. It was revised to use zip and counter instead. I felt it was a slightly better solution*

#### display_table
* Clears the console screen and displays a table of guesses and results.<br>
Note: *Originally this only showed the results in symbolic notation. A friend of mine had a hard time with it and found the numbers I had left in for debugging easier to reference. This lead me to implement the switch notation option, which allows the player to switch between symbolic and numeric results.*

#### prog_game_won
* Adjusts the game conditions after each win in progressive mode.<br>
Note: *The number of guesses for each round may need to be adjusted after more testing.*



