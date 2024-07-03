import argparse
import numpy as np
from WordleSolver import WordleSolver

best_starting_words_general = ['adieu', 'cramp', 'crane', 'crate', 'raise', 'roate', 
                               'salet', 'saucy', 'soare', 'stare', 'trace']
best_starting_words_hard_mode = ['cramp', 'salet']

# use list is the starting words that will all be used
USE_LIST = best_starting_words_general

DISPLAY_PER_WORD = False

# list of targets to solve for
TARGETS = ["zebra", "buddy", "adage", "inlay", "thigh"]

argparser = argparse.ArgumentParser()
argparser.add_argument("--target_words", type=list, default=TARGETS, help="The word to solve for.")
argparser.add_argument("--start_guesses", type=list, default=USE_LIST, help="The starting guess.")
argparser.add_argument("--word_source", type=str, default="data/minimal_wordle_list.txt", help="The source of the word list.")
argparser.add_argument("--verbose", type=bool, default=False, help="Whether to print verbose output.")
argparser.add_argument("--display_guesses", type=bool, default=False, help="Whether to print guesses.")


def display_results(guesses, extra=""):
    guesses = np.array(guesses)
    print(f"Wordle Guesses for {extra}:\n\tMin: {guesses.min()}\n\tMax: {guesses.max()}\n\tMean: {guesses.mean()}\n\tMedian: {np.median(guesses)}")


if __name__ == "__main__":
    args = argparser.parse_args()
    target_words = args.target_words
    start_guesses = args.start_guesses
    word_source = args.word_source
    verbose = args.verbose
    display_guesses = args.display_guesses

    full_results = []

    for target_word in target_words:
        print(f"Solving for {target_word}")
        for start_guess in start_guesses:
            solver = WordleSolver(start_guess=start_guess, word_source=word_source, display_guesses=display_guesses, verbose=verbose)
            solver.initialize()
            result = solver.solve_wordle(target_word)
            full_results += result
            if DISPLAY_PER_WORD:
                display_results(result, extra=f"Starting Guess {start_guess} for {target_word}")
        display_results(np.array(full_results), extra="All Starting Guesses for {target_word}")
