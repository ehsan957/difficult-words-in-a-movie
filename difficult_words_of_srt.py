import requests
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
import csv
import time

class WordMeaningFetcher:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.lc_file_path = "Longman Communication 3000.txt"

    def convert_to_past_tense(self, verb):
        past_tense_verb = self.lemmatizer.lemmatize(verb, 'v')
        return past_tense_verb

    def get_word_meaning_from_longman(self, word, again=0):
        try:
            url = f'https://www.ldoceonline.com/dictionary/{word}'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                meaning_element = soup.find('span', {'class': 'DEF'})
                not_polite = soup.find('span', {'class': 'REGISTERLAB'})
                upperWord = soup.find('span', {'class': 'HYPHENATION'})
                activ = soup.find('span', {'class': 'REFHWD'})
                freq = soup.find('span', {'class': 'FREQ'})

                if freq or (upperWord and upperWord.get_text().strip() != upperWord.get_text().lower().strip()) \
                        or (not_polite and (not_polite.get_text().strip() == "not polite" or not_polite.get_text().strip() == "taboo")):
                    return None

                if activ:
                    if again == 1:
                        return None
                    return self.get_word_meaning_from_longman(activ.get_text().lower().replace(" ", "-"), 1)

                if meaning_element:
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

    def fetch_longman_words(self):
        try:
            url = 'https://www.ldoceonline.com/dictionary/'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()

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

    def find_unsimilar_words(self, srt_file_path, lc_file_path=None):
        if lc_file_path is None:
            lc_file_path = self.lc_file_path  # Use the default path
        try:
            with open(srt_file_path, 'r') as srt_file:
                srt_content = srt_file.read()

            words = srt_content.split()
            clean_words = [word for word in words if word.isalpha()]

            with open(lc_file_path, 'r') as lc_file:
                lc_content = lc_file.read()

            lc_words = lc_content.split()
            unsimilar = []
            difficult_words = []

            for word in clean_words:
                if word.lower() in lc_words:
                    pass
                elif len(word) == 1:
                    pass
                else:
                    if self.convert_to_past_tense(word.lower()) not in lc_words:
                        unsimilar.append(word.lower())

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

    def fetch_and_store_meanings(self, srt_file_path, csv_file_path=None):
        unsimilar, difficult_words = self.find_unsimilar_words(srt_file_path)
        key_words = []

        for word in sorted(set(difficult_words)):
            verb = self.convert_to_past_tense(word)
            if verb:
                key_words.append(verb)

        unsimilar_words_with_meaning_dict = {}

        for word in key_words:
            meaning = self.get_word_meaning_from_longman(word)
            if meaning:
                unsimilar_words_with_meaning_dict[word] = meaning

        if csv_file_path is None:
            csv_file_path = "unsimilar_words_meanings.csv"

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Word', 'Meaning'])

            for word, meaning in unsimilar_words_with_meaning_dict.items():
                csv_writer.writerow([word, meaning])

if __name__ == "__main__":
    meaning_fetcher = WordMeaningFetcher()
    srt_file_path = input("Please input SRT file path: ")
    # Prompt the user for the CSV file path
    csv_file_path = input("Please input CSV file path: ")
    meaning_fetcher.fetch_and_store_meanings(srt_file_path, csv_file_path)