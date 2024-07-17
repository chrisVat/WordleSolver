import argparse
import numpy as np
from WordleSolver import WordleSolver
from tqdm import tqdm

best_starting_words_general = ['adieu', 'cramp', 'crane', 'crate', 'raise', 'roate', 
                               'salet', 'saucy', 'soare', 'stare', 'trace']
best_starting_words_hard_mode = ['zizit'] #, 'salet']
# alert, stare, mouse, train


# best_starting_words_hard_mode = ['plate']

# use list is the starting words that will all be used
USE_LIST = best_starting_words_hard_mode
#USE_LIST = ["mouse"]

DISPLAY_PER_WORD = False

# list of targets to solve for
TARGETS = ["polyp", "puree", "regal", "demon", "evict"]

# latch, shake, mound

TARGETS = ["match"]

argparser = argparse.ArgumentParser()
argparser.add_argument("--target_words", type=list, default=TARGETS, help="The word to solve for.")
argparser.add_argument("--start_guesses", type=list, default=USE_LIST, help="The starting guess.")
argparser.add_argument("--word_source", type=str, default="data/minimal_wordle_list.txt", help="The source of the word list.")
argparser.add_argument("--verbose", type=bool, default=False, help="Whether to print verbose output.")
argparser.add_argument("--display_guesses", type=bool, default=False, help="Whether to print guesses.")



def display_results(guesses, extra=""):
    guesses = np.array(guesses)
    print(f"Wordle Guesses for {extra}:\n\tMin: {guesses.min()}\n\tMax: {guesses.max()}\n\tMean: {guesses.mean()}\n\tMedian: {np.median(guesses)}")


def search_hardest(args):    
    args = argparser.parse_args()
    target_words = args.target_words
    start_guesses = args.start_guesses
    word_source = args.word_source
    verbose = args.verbose
    display_guesses = args.display_guesses
    DISPLAY_PER_WORD = True
    full_results = []

    # """
    # load data/minimal_wordle_list.txt
    word_source = "data/minimal_wordle_list.txt"
    with open(word_source, 'r') as file:
        all_words = file.read().splitlines()
    target_words = all_words[:]
    verbose = False
    display_guesses = False
    worst_performance = 0
    DISPLAY_PER_WORD = False
    worst_words = []
    # target_words = target_words[:560]
    # """



    for target_word in tqdm(target_words):
        #print(f"Solving for {target_word}")
        for start_guess in start_guesses:
            solver = WordleSolver(start_guess=start_guess, word_source=word_source, display_guesses=display_guesses, verbose=verbose)
            solver.initialize()
            # solver.test_dad()
            # exit()
            result = solver.solve_wordle(target_word)
            full_results += result
            if DISPLAY_PER_WORD:
                display_results(result, extra=f"Starting Guess {start_guess} for {target_word}")
        average = np.mean(result)
        
        # """
        if average >= worst_performance:
            worst_performance = average
            worst_words.append(target_word)
            print(f"New worst performance: {worst_performance} for {target_word}")        
        elif average >= 6:
            print(f"Performance: {average} for {target_word}")
            worst_words.append(target_word)
        # display_results(np.array(full_results), extra="All Starting Guesses for {target_word}")
        
        # postfix of worst performance and word
        tqdm.postfix = f"Worst performance: {worst_performance} for {worst_words}"

    print("Worst performance: ", worst_performance, " for ", worst_words)


if __name__ == "__main__":
    search_hardest(argparser)
    exit()
    
    args = argparser.parse_args()
    target_words = args.target_words
    start_guesses = args.start_guesses
    word_source = args.word_source
    verbose = args.verbose
    display_guesses = args.display_guesses
    DISPLAY_PER_WORD = True
    full_results = []


    for target_word in tqdm(target_words):
        #print(f"Solving for {target_word}")
        for start_guess in start_guesses:
            solver = WordleSolver(start_guess=start_guess, word_source=word_source, display_guesses=display_guesses, verbose=verbose)
            solver.initialize()
            # solver.test_dad(['penis', 'there', 'baker'], target_word)
            result = solver.solve_wordle(target_word)
            full_results += result
            if DISPLAY_PER_WORD:
                display_results(result, extra=f"Starting Guess {start_guess} for {target_word}")
        average = np.mean(full_results)



# hatch 
# stain, peddle, actor, catty, hatch

# daunt 

# boxer 

# catch
