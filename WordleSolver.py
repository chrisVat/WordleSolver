import numpy as np
from collections import Counter
import math

class WordleSolver:
    def __init__(self, start_guess="salet", verbose=False, display_guesses=False, word_source="minimal_wordle_list.txt"):
        self.technique = "entropy"
        self.word_source = word_source
        self.start_guess = start_guess
        self.verbose = verbose
        self.display_guesses = display_guesses
        self.initialize()

    def initialize(self):
        self.all_words = self.load_words()
        self.possible_words = self.all_words[:]

    def load_words(self):
        with open(self.word_source, 'r') as file:
            words = file.read().splitlines()
        return words

    def evaluate_guess(self, guess, target):
        feedback = []
        target_letters = list(target)
        for i in range(len(guess)):
            if guess[i] == target[i]:
                feedback.append(1)  # Green
            elif guess[i] in target_letters:
                feedback.append(0) # Yellow
                target_letters[target_letters.index(guess[i])] = None
            else:
                feedback.append(-1) # Black/Grey
        return feedback


    def reduce_possible_words(self, guess, feedback, possible_words):
        new_possible_words = []
        count_per_letter = {}
        for i in range(len(feedback)):
            count_per_letter[guess[i]] = count_per_letter.get(guess[i], 0) + min(feedback[i]+1, 1)

        for word in possible_words:
            match = True
            for i in range(len(feedback)):
                if feedback[i] == 1: # green, needs to match at index
                    if word[i] != guess[i]:
                        match = False
                        break
                elif feedback[i] == 0: # yellow, needs to be found in word
                    if word[i] == guess[i] or guess[i] not in word:
                        match = False
                        break
                elif feedback[i] == -1: # black, should be found less than count
                    count = count_per_letter.get(guess[i])
                    # extra count logic because you can guess letters multiple times
                    if count is not None and word.count(guess[i]) > count:
                        match = False
                        break
            if match:
                new_possible_words.append(word)
        return new_possible_words

    def calculate_entropy(self, guess, possible_words):
        feedback_counts = Counter()
        for word in possible_words:
            feedback = tuple(self.evaluate_guess(guess, word))
            feedback_counts[feedback] += 1
        entropy = 0
        total_words = len(possible_words)
        for count in feedback_counts.values():
            p = count / total_words
            entropy -= p * math.log2(p)
        return entropy

    def entropy_selection(self, possible_words):
        entropies = []
        for guess in possible_words:
            entropy = self.calculate_entropy(guess, possible_words)
            entropies.append(entropy)
        
        entropies = np.array(entropies)
        max_entropy = entropies.max()
        tolerance = 1e-6  # Adjust the tolerance as needed
        best_guesses = np.where(np.isclose(entropies, max_entropy, atol=tolerance))[0]
        best_guesses = [possible_words[i] for i in best_guesses]
        if len(best_guesses) > 1 and self.verbose:
            print("Multiple guesses with max entropy detected: ", best_guesses)
        return best_guesses

    def choose_best_guess(self, possible_words, technique="entropy"):
        if technique == "entropy":
            best_guesses = self.entropy_selection(possible_words)
        return best_guesses

    def feedback_to_string(self, feedback):
        return "".join(["G" if f == 1 else "Y" if f == 0 else "B" for f in feedback])

    def flatten(self, nested_list):
        flattened = []
        stack = nested_list[::-1]
        while stack:
            item = stack.pop()
            if isinstance(item, list):
                stack.extend(item[::-1])
            else:
                flattened.append(item)
        return flattened

    def solve_wordle(self, target_word):
        return self.flatten(self.solve_wordle_recursive(target_word, self.possible_words, self.start_guess, 0))


    def perform_guess(self, guess, target_word, possible_words):
        feedback = self.evaluate_guess(guess, target_word)
        possible_words = self.reduce_possible_words(guess, feedback, possible_words)
        return possible_words

    def test_dad(self, word_list, target):        
        possible_words = self.possible_words.copy()
        for word in word_list:
            possible_words = self.perform_guess(word, target, possible_words)
        print(possible_words)
        exit()

        guesses = self.choose_best_guess(possible_words, self.technique)

        print(possible_words)
        print(len(possible_words))
        #exit()

        guess = "ocean"
        feedback = self.evaluate_guess(guess, target)
        possible_words = self.reduce_possible_words(guess, feedback, possible_words)
        print(possible_words)




    def solve_wordle_recursive(self, target_word, possible_words, guess, guess_num=0):        
        if possible_words is None:
            possible_words = self.possible_words.copy()
        else:
            self.possible_words = possible_words.copy()
        
        guess_num = guess_num + 1
        feedback = self.evaluate_guess(guess, target_word)
        if self.display_guesses:
            print(f"Guess {guess_num}: {guess} - {self.feedback_to_string(feedback)}")
        if feedback == [1] * 5:
            return [guess_num]
        
        possible_words = self.reduce_possible_words(guess, feedback, possible_words)
        
        if self.verbose:
            print(f"Possible words left: {possible_words}")
        
        if not possible_words:
            raise ValueError("No possible words left, something went wrong with filtering.")
        guesses = self.choose_best_guess(possible_words, self.technique)
        
        return [self.solve_wordle_recursive(target_word, possible_words, guess, guess_num) for guess in guesses]


