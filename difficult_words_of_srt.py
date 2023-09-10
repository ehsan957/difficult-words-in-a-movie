import requests
from bs4 import BeautifulSoup
import nltk
from nltk.stem import WordNetLemmatizer
import csv 
import time
# Define a function to convert a verb to its past tense form
def convert_to_past_tense(verb):
    lemmatizer = WordNetLemmatizer()
    past_tense_verb = lemmatizer.lemmatize(verb, 'v')
    return past_tense_verb

# Define a function to get the meaning of a word from the Longman dictionary website
def get_word_meaning_from_longman(word):
    try:
        # Define the URL for the Longman page
        url = f'https://www.ldoceonline.com/dictionary/{word}'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the element that contains the meaning
            meaning_element = soup.find('span', {'class': 'DEF'})
            not_polite = soup.find('span', {'class': 'REGISTERLAB'})
            if not_polite:
                if not_polite.get_text().strip()=="not polite" or not_polite.get_text().strip()=="taboo":
                    return None
            if meaning_element:
                # Get the text content of the meaning element
                meaning = meaning_element.get_text()
                return meaning.strip()
            else:
                return None
        else:
            print(f"Failed to fetch data from Longman website. HTTP status code: {response.status_code}")
            return None
        
    except requests.exceptions.RequestException as e:
        print("Error fetching data from Longman website:", str(e))
        return None
# Add a delay of 3 second to avoid overloading the website with requests

time.sleep(3)

# Define the maximum number of retry attempts and the delay between retries
max_retries = 2  # Adjust this value for more retries if needed
retry_delay = 5  # Number of seconds to wait before retrying

# Define a function to fetch words from the Longman Communication 3000 list
def fetch_longman_words():
    try:
        # Use the URL link to Longman Communication 3000
        url = 'https://www.ldoceonline.com/dictionary/{word}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception if the response is not successful

        soup = BeautifulSoup(response.text, 'html.parser')

        lc_words = set()

        for entry in soup.select('.Entry'):
            word = entry.select_one('.Head .HYPHENATION')
            if word:
                lc_words.add(word.get_text().strip().lower())

        return lc_words

    except requests.exceptions.RequestException as e:
        print("Error fetching data from Longman website:", str(e))
        return set()
# Define a function to find words in a given SRT file that are not in the Longman Communication 3000 list
def find_unsimilar_words(srt_file_l, lc_file_l):
    try:
        # Open and read the SRT file
        with open(srt_file_l, 'r') as srt_file:
            srt_content = srt_file.read()

        # Split the content of the SRT file into words
        words = srt_content.split()

        # Create a list to store words without special characters (alphabetic words)
        clean_words = [word for word in words if word.isalpha()]

        # Open and read the Longman Communication 3000 file
        with open(lc_file_l, 'r') as lc_file:
            lc_content = lc_file.read()

        # Split the content of the Longman Communication 3000 file into words
        lc_words = lc_content.split()

        # Initialize lists to store unsimilar and difficult words
        unsimilar = []
        difficult_words = []

        # Loop through clean words from the SRT file
        for word in clean_words:
            if word.lower() in lc_words:
                pass
            elif len(word) == 1:
                pass
            else:
                # Check if the verb is in base form (convert it to base form)
                if convert_to_past_tense(word.lower()) not in lc_words:
                    unsimilar.append(word.lower())
        
        # Filter out words that are not in the Longman list
        for word in unsimilar:
            if word not in lc_words:
                pass
            else:
                difficult_words.append(word)

        return difficult_words, unsimilar

    except FileNotFoundError:
        print("File not found. Please check the file paths.")
    except IOError:
        print("Error reading the file. Please ensure the files are accessible.")

# Fetch Longman Communication 3000 words
#lc_words = fetch_longman_words()

# Define the file paths for the SRT file and the Longman Communication 3000 file
srt_file_l = input("please enter srt file path...")
lc_file_l = input("please enter Longman Communication 3000 file path...")

# Call the function to find unsimilar words and retrieve the results
unsimilar, difficult_words = find_unsimilar_words(srt_file_l, lc_file_l)
# Create a dictionary to store word meanings
key_word = []
for word in sorted(set(difficult_words)):
    verb = convert_to_past_tense(word)
    if verb:
        key_word.append(verb)
unsimilar_words_with_meaning_dict = {}
# Fetch meanings for unsimilar words and store them in the dictionary
for word in key_word:
    meaning = get_word_meaning_from_longman(word)
    if meaning:
        unsimilar_words_with_meaning_dict[word] = meaning
# Print the unsimilar words with their meanings
csv_file_path = 'unsimilar_words_meaning.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Word', 'Meaning'])  # Write header row
    for word, meaning in unsimilar_words_with_meaning_dict.items():
        csv_writer.writerow([word +'\n', meaning +"\n"])

