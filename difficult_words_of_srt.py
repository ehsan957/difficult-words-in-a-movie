# Import necessary libraries
import requests
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
import csv
import time

# Create a class called WordMeaningFetcher
class WordMeaningFetcher:
    # Initialize the class
    def __init__(self):
        # Create an instance of the WordNetLemmatizer
        self.lemmatizer = WordNetLemmatizer()
        # Set the default path for the Longman Communication 3000 file
        self.lc_file_path = "Longman Communication 3000.txt"

    # Define a method to convert a verb to its past tense
    def convert_to_past_tense(self, verb):
        # Use the WordNetLemmatizer to lemmatize the verb
        past_tense_verb = self.lemmatizer.lemmatize(verb, 'v')
        return past_tense_verb

    # Define a method to fetch the meaning of a word from the Longman dictionary website
    def get_word_meaning_from_longman(self, word, again=0):
        try:
            # Construct the URL for the Longman dictionary website
            url = f'https://www.ldoceonline.com/dictionary/{word}'
            # Set the user agent for the HTTP request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            # Send an HTTP GET request to the website
            response = requests.get(url, headers=headers)

            # Check if the HTTP response status code is 200 (OK)
            if response.status_code == 200:
                # Parse the HTML content of the website using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                # Find the HTML element containing the word's meaning
                meaning_element = soup.find('span', {'class': 'DEF'})
                # Find other relevant information such as word register, hyphenation, etc.
                not_polite = soup.find('span', {'class': 'REGISTERLAB'})
                upperWord = soup.find('span', {'class': 'HYPHENATION'})
                activ = soup.find('span', {'class': 'REFHWD'})
                freq = soup.find('span', {'class': 'FREQ'})

                # Check for conditions indicating that the word may not be suitable
                # for the Longman dictionary (e.g., frequency, politeness)
                if freq or (upperWord and upperWord.get_text().strip() != upperWord.get_text().lower().strip()) \
                        or (not_polite and (not_polite.get_text().strip() == "not polite" or not_polite.get_text().strip() == "taboo")):
                    return None

                # If the word is a verb form, attempt to find its base form
                if activ:
                    # If it's the second attempt, return None to avoid infinite recursion
                    if again == 1:
                        return None
                    # Recursively call the method with the base form of the verb
                    return self.get_word_meaning_from_longman(activ.get_text().lower().replace(" ", "-"), 1)

                # If the meaning element is found, extract and return the meaning
                if meaning_element:
                    meaning = meaning_element.get_text()
                    return meaning.strip()
                else:
                    return None
            else:
                # Print an error message if the HTTP request fails
                print(f"Failed to fetch data from Longman website. HTTP status code: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that may occur during the HTTP request
            print("Error fetching data from Longman website:", str(e))
            return None

    # Define a method to fetch words from the Longman dictionary website
    def fetch_longman_words(self):
        try:
            # Define the URL for the Longman dictionary website
            url = 'https://www.ldoceonline.com/dictionary/'
            # Set the user agent for the HTTP request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            # Send an HTTP GET request to the website
            response = requests.get(url, headers=headers)
            # Raise an exception if the HTTP request fails
            response.raise_for_status()

            # Parse the HTML content of the website using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Create a set to store Longman dictionary words
            lc_words = set()

            # Extract words from the website and add them to the set
            for entry in soup.select('.Entry'):
                word = entry.select_one('.Head .HYPHENATION')
                if word:
                    lc_words.add(word.get_text().strip().lower())

            return lc_words

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that may occur during the HTTP request
            print("Error fetching data from Longman website:", str(e))
            return set()

    # Define a method to find words in an SRT file that are not present in the Longman Communication 3000 list
    def find_unsimilar_words(self, srt_file_path, lc_file_path=None):
        # Use the default path if lc_file_path is not provided
        if lc_file_path is None:
            lc_file_path = self.lc_file_path
        try:
            # Open and read the content of the SRT file
            with open(srt_file_path, 'r') as srt_file:
                srt_content = srt_file.read()

            # Split the SRT content into words
            words = srt_content.split()
            # Filter out non-alphabetic words
            clean_words = [word for word in words if word.isalpha()]

            # Open and read the content of the Longman Communication 3000 file
            with open(lc_file_path, 'r') as lc_file:
                lc_content = lc_file.read()

            # Split the LC content into words
            lc_words = lc_content.split()
            # Initialize lists to store dissimilar and difficult words
            unsimilar = []
            difficult_words = []

            # Iterate through the clean words from the SRT file
            for word in clean_words:
                # Check if the lowercase word is present in the LC words
                if word.lower() in lc_words:
                    pass
                # Skip single-character words
                elif len(word) == 1:
                    pass
                else:
                    # Check if the past tense form of the word is not in the LC words
                    if self.convert_to_past_tense(word.lower()) not in lc_words:
                        unsimilar.append(word.lower())

            # Iterate through the unsimilar words
            for word in unsimilar:
                # Check if the word is in the LC words
                if word not in lc_words:
                    pass
                else:
                    difficult_words.append(word)

            # Return lists of difficult and unsimilar words
            return difficult_words, unsimilar

        except FileNotFoundError:
            # Handle the case where the file is not found
            print("File not found. Please check the file paths.")
        except IOError:
            # Handle IO errors while reading files
            print("Error reading the file. Please ensure the files are accessible.")

    # Define a method to fetch and store the meanings of difficult words
    def fetch_and_store_meanings(self, srt_file_path, csv_file_path=None):
        # Find difficult and unsimilar words in the SRT file
        unsimilar, difficult_words = self.find_unsimilar_words(srt_file_path)
        # Initialize a list to store key words
        key_words = []

        # Iterate through sorted unique difficult words
        for word in sorted(set(difficult_words)):
            # Convert the word to its past tense form
            verb = self.convert_to_past_tense(word)
            if verb:
                key_words.append(verb)

        # Create a dictionary to store unsimilar words with their meanings
        unsimilar_words_with_meaning_dict = {}

        # Iterate through key words and fetch their meanings
        for word in key_words:
            meaning = self.get_word_meaning_from_longman(word)
            if meaning:
                unsimilar_words_with_meaning_dict[word] = meaning

        # Use a default CSV file path if not provided
        if csv_file_path is None:
            csv_file_path = "unsimilar_words_meanings.csv"

        # Write the meanings to a CSV file
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Word', 'Meaning'])

            for word, meaning in unsimilar_words_with_meaning_dict.items():
                csv_writer.writerow([word, meaning])

# Entry point for the script
if __name__ == "__main__":
    # Create an instance of the WordMeaningFetcher class
    meaning_fetcher = WordMeaningFetcher()
    # Prompt the user for the SRT file path
    srt_file_path = input("Please input SRT file path: ")
    # Prompt the user for the CSV file path
    csv_file_path = input("Please input CSV file path: ")
    # Fetch and store the meanings of difficult words
    meaning_fetcher.fetch_and_store_meanings(srt_file_path, csv_file_path)
