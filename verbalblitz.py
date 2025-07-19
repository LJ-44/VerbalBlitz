import os
import time
import random
import threading
import emoji

# game like Word Bomb on Roblox

'''
# BRAIN DUMP: 

# Two text files
# 1: list of english words from a dictionary
# 2: list of strings, 2 characters, ex: "ar", "el", "pr", etc

# Random Number Generator:
# pick random string from file 2 
# user types word, if selected string from file 2 is in user's word, pass to next if, if word in file 1, accept word. 

# Timer:
# count down from 10 after string is picked

# Text: 
# prompt: "Quick, type an english word containing {string}!" 
# lose: "Game Over! You ran out of time!"
# typo, wrong word, etc: "That word doesn't exist!" (timer continues)

# Difficulties?:
# Start menu, 3 options, easy medium hard
# easy: accepts all inputs if its a real word
# medium: input > 3 letters
# hard: input > 5 letters

# Start Menu: 
# "Welcome to Verbal Blitz!" 
#
# Choose an Option: 
#
# 1. Pick Game Mode:
#   1. Normal (Word Bomb)
#   2. Blitz (type as many words as you can containing the string)
# 2. Exit

# High Score:
# highest streak of words accepted in a row
# different high scores need to be stored for different difficulties, game modes, etc
# for now just write them to a text file
# after figuring that out, try to figure out .json files to store them
'''

#TODO: add more phrases to phrases.txt 

CORRECT = 0

# words = open("C:\\Users\\lucas\\Documents\\pythonProjects\\VerbalBlitz\\words.txt", "r")
def start_menu():
    print("Welcome to Verbal Blitz!\n")
    print("Pick a Game Mode:")
    print("1. Normal")
    print("2. Blitz")
    print("Exit? (q)\n")

# load words in english dictionary
def load_words():
    with open("C:\\Users\\lucas\\Documents\\pythonProjects\\VerbalBlitz\\words.txt") as word_file:
        valid_words = set(word_file.read().split())
    return valid_words

# load 2-letter phrases
def load_phrases():
    with open("C:\\Users\\lucas\\Documents\\pythonProjects\\VerbalBlitz\\phrases.txt") as phrase_file:
        valid_phrases = set(phrase_file.read().split())
    return valid_phrases

# game modes
def pick_game_mode():

    choice = input()

    if choice == '1':
        game_mode = 'normal'
    elif choice == '2':
        game_mode = 'blitz'
    elif choice == 'q':
        print("Goodbye!")
        os._exit(1)

    return game_mode

def timeout():
    print(f"\nUh oh! You ran out of time! {emoji.emojize(":frowning_face:")}")
    print(f"Score: {CORRECT}")
    os._exit(1)

# game modes
def run_game_mode(mode='normal', words=None, phrases=None):
    # keepGoing = True
    global CORRECT
    if mode == 'normal':
        print(f'\n{emoji.emojize("Normal Mode Selected :check_mark_button:")}')
        time.sleep(1)
        print("Type words containing the 2-letter phrase given to you.")
        time.sleep(1)
        print("There is a 10 second time limit for each word!")
        time.sleep(1)
        print("Good luck!\n")
        time.sleep(1)

        random_phrase = random.choice(list(phrases))
        normal_timer = threading.Timer(10.0, timeout)
        normal_timer.start()

        while True:
            
            normal_input = input(f"{emoji.emojize(":hourglass_not_done:")} Quick, type an english word containing \"{random_phrase}\" within 10 seconds! {emoji.emojize(":hourglass_not_done:")}\n\n").lower()

            if not normal_timer.is_alive():
                break

            if ((random_phrase in normal_input) and (normal_input in words)):

                normal_timer.cancel()

                print(f"\nGood Job! {emoji.emojize(':face_with_tongue:')}")
                CORRECT += 1

                random_phrase = random.choice(list(phrases))
                normal_timer = threading.Timer(10.0, timeout)
                normal_timer.start()

            else: 
                print(f"Oops! Try again. Time is still ticking! {emoji.emojize(":hourglass_not_done:")}")
            
    if mode == 'blitz':
        print(f"\n{emoji.emojize("Blitz Mode Selected :check_mark_button:")}")
        time.sleep(1)
        print("Type as many words as you can containing the 2-letter phrase given to you.")
        time.sleep(1)
        print("There is a 30 second time limit!")
        time.sleep(1)
        print("Good luck!\n")
        time.sleep(1)

        random_phrase = random.choice(list(phrases))
        blitz_timer = threading.Timer(30.0, timeout)
        blitz_timer.start()

        print(f"{emoji.emojize(":hourglass_not_done:")} Type as many words as you can containing \"{random_phrase}\" within 30 seconds! {emoji.emojize(":hourglass_not_done:")}\n\n")

        words_typed = set()

        while True:

            blitz_input = input()

            if not blitz_timer.is_alive():
                break
            if ((blitz_input in words) and (blitz_input in words_typed)):
                print(f"You already typed that word!")
                continue
            if ((random_phrase in blitz_input) and (blitz_input in words) and (blitz_input not in words_typed)):
                words_typed.add(blitz_input)
                CORRECT += 1
                pass
            else:
                print(f"That word doesn't exist! Try again.{emoji.emojize(":hourglass_not_done:")}")

def main(): 
    # write setup functions in order of game flow
    start_menu()
    english_words = load_words()
    set_phrases = load_phrases()
    game_mode = pick_game_mode()
    run_game_mode(mode=game_mode, words=english_words, phrases=set_phrases)
    #end_game()

if __name__ == "__main__":
    main()
