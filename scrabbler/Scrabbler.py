# This is a Scrabble Helper script that will generate words for you. It uses the Official
# Scrabble Dictionary as reference. It will take inputs of your rack position (i.e. the
# letters (tiles) that you have on the rack, including blank tiles if any) and your preferred
# word length range. It will then output all words matching the criteria along with their
# point scores to a text file. It also accounts for any double or triple word or letter scores.
# It requires scrabble.dict file (the reference Dictionary) in the same directory to work.
#
# IMPORTANT: It needs the pandas package to execute. Please ensure that it is installed.
#
# Install pandas package with:
# python3 -m pip install --upgrade pip
# python3 -m pip install --upgrade pandas
#
# This script is written by AMEYA KAMAT and is licensed under GNU GPL v3.
#
# You can freely download, use, modify and/or distribute this code.

from itertools import permutations, combinations
import pandas as pd


def main():
    # Initialize / Create the variables and datasets that we would be using later.
    num_words, total_words, word_value, bingo = 0, 0, 0, 0
    repeat_check, word_list, word_len_list, point_list, ltr1_list, ltr2_list = [], [], [], [], [], []
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'P', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    points = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1,
              "F": 4, "G": 2, "H": 4, "I": 1, "J": 8,
              "K": 5, "L": 1, "M": 3, "N": 1, "O": 1,
              "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1,
              "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10}
    special_squares_list = ("DWS", "DLS", "TWS", "TLS")
    special_squares = dict()
    df_words = pd.DataFrame()

    # Create a file where the final solution (matching words) will be output to
    word_file = open('words.txt', "w")

    # Start the program with a welcome message.
    print("WELCOME TO THE SCRABBLE HELPER BY AMEYA KAMAT\n")

    # Transfer the list of items in the text file to a tuple
    with open('scrabble.dict') as file:
        scrab_dict = file.read().splitlines()
        scrab_dict = tuple(scrab_dict)
    print("We use the Official Colin's Scrabble Dictionary that contains", len(scrab_dict), "words.\n")

    # Get inputs about word length
    while True:
        print("How long do you want the word to be? ")
        min_word_length = input("Input Minimum length: ")
        max_word_length = input("Input Maximum length: ")

        if min_word_length.isdigit() and max_word_length.isdigit():
            min_word_length = int(min_word_length)
            max_word_length = int(max_word_length)
            break
        else:
            print("Both values should be numbers. Please try again.\n")

    # Find all words matching the specified word length(s).
    for item in scrab_dict:
        if min_word_length <= len(item) <= max_word_length:
            total_words += 1
            word_list.append(item)
    print("We found a total of", total_words, "words! \n")

    # Get the tiles on the rack and validate input
    while True:
        rack1 = input("What tiles do you have on your rack? (excluding blanks): ")
        rack1 = rack1.upper()

        # Validating for alphabet and rack length
        if rack1.isalpha() and 0 < len(rack1) <= 7:
            break
        else:
            print("Please enter the tiles without spaces and numbers."
                  "Also you can have a maximum of 7 tiles on your rack. Try again.")

    # Get the number of blank tiles and validate input
    while True:
        blanks = input("How many blank tiles do you have? ")
        if blanks.isdigit() and 0 <= int(blanks) <= 2:
            blanks = int(blanks)
            break
        else:
            print("\nThere are a maximum of 2 blank tiles in Scrabble.")
            print("Please enter a number from 0 to 2. Try again.")

    print("\nPlease wait while we find the words for you...")

    # Break up user input of a string (for letters in the rack) into individual letters
    rack = [char for char in rack1]

    # Find solution if there are no blanks in the rack.
    if blanks == 0:
        for number in range(min_word_length, max_word_length + 1):  # For Loop iterating for word length
            for current_set in combinations(rack, number):  # Combinations Function
                # Code for the Basic Anagram Finder
                for current in permutations(current_set):
                    current_word = ''.join(current).upper()
                    # Check for legality of the generated word and avoid duplicates
                    if current_word in word_list and current_word not in repeat_check:
                        # Compute point score for the matching word
                        for let in range(0, len(current_word)):
                            key = current_word[let]
                            letter_value = points[key]
                            word_value += letter_value
                        # Write the word and its point score to the file we created earlier
                        word_with_value = (current_word + " [" + str(word_value) + "]")
                        word_file.write(word_with_value)
                        word_file.write("\n")

                        repeat_check.append(current_word)   # Add the matched word to a list to avoid duplication
                        word_len_list.append(len(current_word))  # Add the current word length to a list
                        point_list.append(word_value)       # Add point score of words to a list

                        num_words += 1  # Increment matched word count
                        word_value = 0  # Reset the point score back to zero for the next word

        # Create a Data Frame of the generated words and their point scores
        ltr1_list = [None] * len(point_list)
        ltr2_list = [None] * len(point_list)
        df_words = pd.DataFrame(list(zip(repeat_check, word_len_list, point_list, ltr1_list, ltr2_list)))
        df_words.columns = ['Words', 'Length', 'Points', 'Blank 1', 'Blank 2']
        # df_words = df_words.set_index("Words", drop = False)

    # Find solution if there is 1 blank in the rack.
    elif blanks == 1:
        for num in range(0, 26):    # Iterate 26 times to cycle through the alphabet for substituting the blank tile
            rack.append(alphabet[num])  # Add an alphabet to the rack
            added_ltr1 = alphabet[num].upper()  # Save the added letter to a variable
            added_val1 = points[added_ltr1]     # Save the point score of the added letter to a variable
            for number in range(min_word_length, max_word_length + 1):  # For Loop to iterate for word length
                for current_set in combinations(rack, number):  # Combinations Function
                    # Code for the Basic Anagram Finder
                    for current in permutations(current_set):
                        current_word = ''.join(current).upper()
                        # Check for legality of the generated word and avoid duplicates
                        if current_word in word_list and current_word not in repeat_check:
                            # Compute point score for the matching word
                            for let in range(0, len(current_word)):
                                key = current_word[let]
                                letter_value = points[key]
                                word_value += letter_value
                            # Reduce the point score of the letter added to substitute the blank tile
                            if current_word.count(added_ltr1) > rack1.count(added_ltr1):
                                word_value -= added_val1
                            else:
                                pass
                            # Formatting the final output that will detail the word, score and substitutions, if any
                            word_with_value = (current_word + " [" + str(word_value) + "]")
                            if added_ltr1 not in rack1:
                                word_with_value += ("  Blank converted to: " + added_ltr1)
                            else:
                                pass
                            # Write the final output the file we created earlier
                            word_file.write(word_with_value)
                            word_file.write("\n")

                            repeat_check.append(current_word)   # Add the matched word to a list to avoid duplication
                            word_len_list.append(len(current_word))  # Add the current word length to a list
                            point_list.append(word_value)       # Add point score of words to a list
                            ltr1_list.append(added_ltr1)        # Add 1st blank substitution to a list
                            num_words += 1  # Increment the matched word count
                            word_value = 0  # Reset the point score to zero for the next word
            rack.remove(alphabet[num])      # Remove the added alphabet / Restore the original rack

        # Create a Data Frame of the generated words and their point scores
        ltr2_list = [None] * len(point_list)
        df_words = pd.DataFrame(list(zip(repeat_check, word_len_list, point_list, ltr1_list, ltr2_list)))
        df_words.columns = ['Words', 'Length', 'Points', 'Blank 1', 'Blank 2']

    # Find solution if there are 2 blanks in the rack.
    elif blanks == 2:
        for num in range(0, 26):    # Iterate 26 times to cycle through the alphabet to substitute first blank tile
            rack.append(alphabet[num])  # Add a letter to the rack
            added_ltr1 = alphabet[num].upper()  # Save the first added letter to a variable
            added_val1 = points[added_ltr1]     # Save the point score of the first added letter to a variable
            for num1 in range(0, 26):  # Iterate 26 times to cycle through the alphabet to substitute second blank tile
                rack.append(alphabet[num1])     # Add a letter to the rack
                added_ltr2 = alphabet[num1].upper()     # Save the second added letter to a variable
                added_val2 = points[added_ltr2]         # Save the point score of the second added letter to a variable
                for number in range(min_word_length, max_word_length + 1):  # For Loop to iterate for word length
                    for current_set in combinations(rack, number):  # Combinations Function
                        # Code for the Basic Anagram Finder
                        for current in permutations(current_set):
                            current_word = ''.join(current).upper()
                            # Check for legality of the generated word and avoid duplicates
                            if current_word in word_list and current_word not in repeat_check:
                                # Compute point score for the matching word
                                for let in range(0, len(current_word)):
                                    key = current_word[let]
                                    letter_value = points[key]
                                    word_value += letter_value
                                # Reduce the point score of the first letter added to substitute the blank tile
                                if current_word.count(added_ltr1) > rack1.count(added_ltr1):
                                    word_value -= added_val1
                                else:
                                    pass
                                # Reduce the point score of the second letter added to substitute the blank tile
                                if current_word.count(added_ltr2) > rack1.count(added_ltr2):
                                    word_value -= added_val2
                                else:
                                    pass
                                # Formatting the final output that will detail the word, score and substitutions, if any
                                word_with_value = (current_word + " [" + str(word_value) + "]")
                                if current_word.count(added_ltr1) > rack1.count(added_ltr1):
                                    word_with_value += ("  Blank converted to: " + added_ltr1)
                                else:
                                    pass
                                if current_word.count(added_ltr2) > rack1.count(added_ltr2):
                                    word_with_value += ("  Blank converted to: " + added_ltr2)
                                else:
                                    pass
                                # Write the final output the file we created earlier
                                word_file.write(word_with_value)
                                word_file.write("\n")

                                repeat_check.append(current_word)   # Add matched word to a list to avoid duplication
                                word_len_list.append(len(current_word))  # Add the current word length to a list
                                point_list.append(word_value)  # Add point score of words to a list
                                ltr1_list.append(added_ltr1)  # Add 1st blank substitution to a list
                                ltr2_list.append(added_ltr2)  # Add 2nd blank substitution to a list
                                num_words += 1  # Increment the matched word count
                                word_value = 0  # Reset point score to zero for the next word
                rack.remove(alphabet[num1])     # Remove the second added alphabet
            rack.remove(alphabet[num])  # Remove the first added alphabet / Restore the original rack

        # Create a Data Frame of the generated words and their point scores
        df_words = pd.DataFrame(list(zip(repeat_check, word_len_list, point_list, ltr1_list, ltr2_list)))
        df_words.columns = ['Words', 'Length', 'Points', 'Blank 1', 'Blank 2']

    print("\nHERE ARE THE RESULTS...")
    print("---------------------------------")

    # Calculate number of words based on word length
    for words in range(min_word_length, max_word_length + 1):
        count = len([item for item in repeat_check if len(item) == words])
        print(words, "letter words found:", count)

    # The final results / solution of matched words
    print("---------------------------------")
    print("Total matching words found:", num_words)
    print("=================================")

    # Count and Print number of bingo found if any
    bingo = len([item for item in repeat_check if len(item) == 7])
    if bingo > 0:
        print("Hey Congratulations! We found", bingo, "bingo for you!!")
    else:
        pass

    print("\nThe list of matching words has been exported to words.txt file.\n")

    # Ask if the user wishes to find the best plays.
    choice = input("\nEnter H to search for the highest scoring play. Any other key to quit: ")
    if choice.upper() != "H":
        quit()
    else:
        pass

    # Ask the user to pick a word length and validate the input
    while True:
        print("\nPick a word length between", min_word_length, "and", max_word_length,
              "letters to get the highest scoring play.")
        word_len = input("What word length do you wish to use? ")
        if word_len.isdigit() and min_word_length <= int(word_len) <= max_word_length:
            word_len = int(word_len)
            break
        else:
            print("\nYour input is not correct. Please try again.")

    # Check for special squares
    print("\nAre there any special squares in the", word_len, "lettered word?")
    choice = input("Enter Y for Yes or any other key for No: ").upper()

    # Get the positions of all the special squares for the proposed position of the word on the board.
    if choice == "Y":
        print("Use the following keys to denote for every letter. Press ENTER for None.")
        print("DWS: Double Word Score\nDLS: Double Letter Score\nTWS: Triple Word Score\nTLS: Triple Letter Score")
        for item in range(1, word_len + 1):
            while True:
                let = input("Letter " + str(item) + " : ").upper()
                if let in special_squares_list or let == "":
                    special_squares[item] = let
                    break
                else:
                    print("\nWrong key for special squares entered. Please try again.")
    else:
        pass

    # Add a column for High scores for each word after special squares scoring.
    df_words['Best Play'] = 0

    # Trim the dataframe so that it contains words of the specified length only.
    df_words = df_words.loc[df_words['Length'] == word_len]

    # Iterate through all the words
    for word in range(len(df_words)):
        pick_word = df_words.iat[word, 0]
        # Iterate through the letters of the word
        for let in range(len(pick_word)):
            key = pick_word[let]

            # If blanks are used, set the letter value to Zero
            if key == df_words.iat[word, 3]:
                letter_value = 0
            elif key == df_words.iat[word, 4]:
                letter_value = 0
            else:   # Else, set the letter value to the points for that letter
                letter_value = points[key]

            letd = let + 1

            # Account for Double and Triple Letter Scores
            if len(special_squares) != 0:
                if special_squares[letd] == "DLS":
                    letter_value = letter_value * 2
                elif special_squares[letd] == "TLS":
                    letter_value = letter_value * 3
                else:
                    pass
            else:
                pass

            # Calculate the points value for the word
            word_value += letter_value

        # Account for Double and Triple Word Score
        if "DWS" in special_squares.values():
            word_value = word_value * 2
        else:
            pass
        if "TWS" in special_squares.values():
            word_value = word_value * 3
        else:
            pass

        # Update the data frame for the high score for the word after accounting for special squares & bingo
        if len(pick_word) == 7:
            df_words.loc[df_words['Words'] == pick_word, 'Best Play'] = word_value + 50
        else:
            df_words.loc[df_words['Words'] == pick_word, 'Best Play'] = word_value
        word_value = 0      # Reset word value to 0 to calculate for the next word

    # Sort the words by highest scoring plays
    df_words.sort_values(by=['Best Play'], inplace=True, ascending=False)

    print("\nHere are the Top 5 highest scoring plays for you")
    select_df_words = df_words[['Words', 'Best Play']]
    print(select_df_words.head())

    print("\nThank you for using Ameya Kamat's Scrabbler.")


if __name__ == '__main__':
    main()
