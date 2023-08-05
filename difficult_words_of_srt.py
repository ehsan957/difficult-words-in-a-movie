import requests
from bs4 import BeautifulSoup
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

def convert_to_past_tense(verb):
    lemmatizer = WordNetLemmatizer()
    past_tense_verb = lemmatizer.lemmatize(verb, 'v')
    return past_tense_verb

def fetch_longman_words():
    try:
        # Use the URL link to Longman site
        url = 'https://www.ldoceonline.com'#/dictionary/english'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find words in the Longman site
        lc_words = set()
        for entry in soup.select('.Entry'):
            word = entry.select_one('.Head .HYPHENATION')
            if word:
                lc_words.add(word.get_text().strip().lower())

        return lc_words

    except requests.exceptions.RequestException as e:
        print("Error fetching data from Longman website:", str(e))
        return set()

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
        difficult_words = []
        for word in unsimilar:
            if word not in lc_words:
                pass
            else:
                difficult_words.append(word)

        return difficult_words,unsimilar

    except FileNotFoundError:
        print("File not found. Please check the file paths.")
    except IOError:
        print("Error reading the file. Please ensure the files are accessible.")

# Fetch Longman Communication 3000 words
lc_words = fetch_longman_words()

# Get the file paths from user input
srt_file_l = input('please enter srt file  path: ')
lc_file_l =  input('please enter Longman Communication 3000 file  path: ')

# Call the function and retrieve the results
difficult_words,unsimilar = find_unsimilar_words(srt_file_l, lc_file_l)

# Write the unsimilar words to the 'new_txt_file.txt' file
with open('new_txt_filen.txt', 'w') as new_file:
    for word in sorted(set(difficult_words)):  # Use set to remove duplicates
        new_file.write(word + '\n')

