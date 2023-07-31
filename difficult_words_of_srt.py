import nltk
from nltk.stem import WordNetLemmatizer
#write (pip install nltk ) in terminal for installing the module
def convert_to_past_tense(verb):
    lemmatizer = WordNetLemmatizer()
    past_tense_verb = lemmatizer.lemmatize(verb, 'v')
    return past_tense_verb

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
        for word in clean_words:
            if word.lower() in lc_words:
                pass
            elif len(word) == 1:
                pass
            else:
                # Check if the verb is in base form (convert it to base form)
                if convert_to_past_tense(word.lower()) not in lc_words:
                    unsimilar.append(word.lower())

        return unsimilar

    except FileNotFoundError:
        print("File not found. Please check the file paths.")
    except IOError:
        print("Error reading the file. Please ensure the files are accessible.")

# Get the file paths from user input (You can replace these paths with your file paths)
srt_file_l = input('please enter srt file  path: ')
lc_file_l =  input('please enter Longman Communication 3000 file  path: ')

# Call the function and retrieve the results
unsimilar_words = find_unsimilar_words(srt_file_l, lc_file_l)

# Write the unsimilar words to the 'new_txt_file.txt' file
with open('new_txt_file.txt', 'w') as new_file:
    for word in sorted(set(unsimilar_words)):  # Use set to remove duplicates
        new_file.write(word + '\n')

