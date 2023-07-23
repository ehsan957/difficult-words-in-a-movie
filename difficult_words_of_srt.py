def find_unsimilar_words(srt_file_l, lc_file_l):
    try:
        # Open and read the SRT file
        with open(srt_file_l, 'r') as srt_file:
            srt_content = srt_file.read()

        # Split the content into words
        words = srt_content.split()

        # Create a list to store words without special characters
        clean_words = [word for word in words if word.isalpha()]

        # Open and read the Longman Communication 3000 file
        with open(lc_file_l, 'r') as lc_file:
            lc_content = lc_file.read()

        # Split the content into words
        lc_words = lc_content.split()

        # Find the unsimilar words (not present in the Longman Communication 3000 file)
        unsimilar = []
        difficult_word = []
        for word in clean_words:
            if word.lower() in lc_words:
                pass
            else:
                unsimilar.append(word.lower())

        # Check for words that end with 'ed' or 'ing'and exist in LC 3000 file or have a length of 1 character
        for word in unsimilar:
            if  len(word) == 1:
                pass
            elif word in lc_words or word.endswith('ing') or word.endswith('ed'):
                    pass
            else:
                difficult_word.append(word)

        return unsimilar, difficult_word
    except FileNotFoundError:
        print("File not found. Please check the file paths.")
    except IOError:
        print("Error reading the file. Please ensure the files are accessible.")


# Get the file paths from user input (You can replace these paths with your file paths)
srt_file_l = input('please enter srt file path: ')
lc_file_l = input('please enter longman communication 3000 file path: ')
# for testing code we use these links(https://github.com/jnoodle/English-Vocabulary-Word-List/blob/master/Longman%20Communication%203000.txt)

# Call the function and retrieve the results
unsimilar_words, difficult_words = find_unsimilar_words(srt_file_l, lc_file_l)

# Write the unsimilar words to the 'new_txt_file.txt' file
with open('new_txt_file.txt', 'w') as new_file:
    for word in sorted(set(difficult_words)):  # Use set to remove duplicates
        new_file.write(word + '\n')


