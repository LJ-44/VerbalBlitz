import os
import time
import random
import threading
import emoji
from collections import defaultdict

# game like Word Bomb on Roblox

CORRECT = 0

def start_menu():
    print("Welcome to Verbal Blitz!\n")
    print("Pick a Game Mode:")
    print("1. Normal")
    print("2. Blitz")
    print("Exit? (q)\n")

# load words in english dictionary
def load_words():
    with open("words.txt") as word_file:
        valid_words = set(word_file.read().split())
    return valid_words

# game modes
def pick_game_mode():
    
    valid_choice = False
    while not valid_choice:
    
        choice = input()
        
        if choice == '1':
            game_mode = 'normal'
            valid_choice = True
        elif choice == '2':
            game_mode = 'blitz'
            valid_choice = True
        elif choice == 'q':
            print("Goodbye!")
            os._exit(1)
        else:
            print("That's not a valid choice. Try again")
            continue

    return game_mode

def select_difficulty():
    
    with open("words.txt") as word_file:
        words = [line.strip().lower() for line in word_file if len(line.strip()) > 2]

    pair_freq = defaultdict(int)

    for word in words:
        for i in range(len(word) - 1):
            pair = word[i:i+2]
            pair_freq[pair] += 1
        
    easy = [pair for pair, count in pair_freq.items() if count > 15000]
    medium = [pair for pair, count in pair_freq.items() if 1000 < count <= 15000]
    hard = [pair for pair, count in pair_freq.items() if 100 < count <= 9000]
    insane = [pair for pair, count in pair_freq.items() if count <= 5000]
    
    print("Select Difficulty\n")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    print("4. Insane")
    
    valid_difficulty = False
    
    while not valid_difficulty:
        difficulty = input()
        
        with open("phrases.txt", "w") as phrases_file:
            if difficulty == '1':
                valid_difficulty = True
                for phrase in easy:
                    phrases_file.write(phrase + "\n")
            elif difficulty == '2':
                valid_difficulty = True
                for phrase in medium:
                    phrases_file.write(phrase + "\n")
            elif difficulty == '3':
                valid_difficulty = True
                for phrase in hard:
                    phrases_file.write(phrase + "\n")
            elif difficulty == '4':
                valid_difficulty = True
                for phrase in insane:
                    phrases_file.write(phrase + "\n")
            else:
                print("That's not a valid choice. Try again.")
                continue
    with open("phrases.txt", 'r') as phrases_file:
        phrases = set(phrases_file.read().split())
    return phrases
    
# running out of time
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
    game_mode = pick_game_mode()
    difficulty = select_difficulty()
    run_game_mode(mode=game_mode, words=english_words, phrases=difficulty)
    #end_game()

if __name__ == "__main__":
    main()
