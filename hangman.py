import random
import string
import hangman_wordbank
from hangman_prints import gallow_prints, title_screen



class HangmanGame():
    def __init__(self):
        self.current_try = 0
        self.max_tries = 7
        self.wordbank = hangman_wordbank.fruits_and_veggies
        self.alphabet = list(string.ascii_lowercase)
        self.guessed_letters = set()
        self.word = ''
        self.hidden_word = ''
        self.letters = []
        self.starting_letter = ''

    def prepare_word(self):
        i = random.randint(0, len(self.wordbank) - 1)
        self.word = self.wordbank[i]
        for letter in self.word:
            if letter not in self.letters:
                self.letters.append(letter)
        j = random.randint(0, len(self.letters) - 1)
        self.starting_letter = self.letters[j]
        letters_to_hide = []
        for k, letter in enumerate(self.word):
            if letter not in (self.starting_letter, ' '):
                letter = '_'
            letters_to_hide.append(letter)
        self.hidden_word = ''.join(letters_to_hide)
    
    def uncover_letter(self, word, hidden_word, guess):
        for i, letter in enumerate(word):
            if guess == letter:
                hidden_word = hidden_word[:i] + letter + hidden_word[i + 1:]
        return hidden_word
    
    def verify_letter(self, guess, word, hidden_word, letters):
        guess = guess.casefold()
        if guess not in self.alphabet:
            print('\nThat is not a letter.')
            return hidden_word

        if guess in self.guessed_letters:
            s = ', '.join(self.guessed_letters)
            print('\nThis letter has already been guessed.')
            print(f'Here are your guesses so far: {s}')
        elif guess not in letters:
            self.current_try += 1
            print(f'{gallow_prints[self.current_try]}')
        else:
            hidden_word = self.uncover_letter(word, hidden_word, guess)

        self.guessed_letters.add(guess)
        return hidden_word
    
    def is_game_over(self, hidden_word, word):
        has_won = (hidden_word == word)
        has_lost = (self.current_try == self.max_tries)
        if not has_won and not has_lost:
            return False
        if has_won:
            print(f'\n>>> {word} <<<')
            print('CONGRATULATIONS! You have won!')
        elif has_lost:
            print('\nGAME OVER! You ran out of tries!')
            print(f'The word was: >>> {word} <<<')
        return True

    def reset_game(self):
        self.guessed_letters = set()
        self.current_try = 0
        self.hidden_word = ''
        self.starting_letter = ''
        self.letters = []

    def play_again(self):
        choice = input('\nDo you want to play again? (y/n): ').casefold()
        if choice == 'y':
            self.prepare_game()
        quit()

    def prepare_game(self):
        self.reset_game()
        self.prepare_word()
        print(title_screen)
        self.guessed_letters.add(self.starting_letter)
        self.game_loop(self.word, self.hidden_word, self.letters, self.starting_letter)

    def game_loop(self, word, hidden_word, letters, starting_letter):
        if self.is_game_over(hidden_word, word):
            self.play_again()
        print(f'\n>>> {hidden_word} <<<')
        guess = input('Guess a letter: ')
        hidden_word = self.verify_letter(guess, word, hidden_word, letters)
        self.game_loop(word, hidden_word, letters, starting_letter)


hangman = HangmanGame()

def __main__():
    hangman.prepare_game()

if __name__ == '__main__':
    __main__()
