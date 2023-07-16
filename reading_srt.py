#I use a try and except block to handle any potential errors that may occur when opening and reading the files
# first, deffine a function
def find_similar_words(srt_file, lc_file):
    try:
        # Open and read the SRT file
        with open(srt_file, 'r') as srt_file:
            srt_content = srt_file.read()

        # Split the content into words
        words = srt_content.split()

        # Create a list to store words without special characters
        clean_words = []
        for word in words:
            if word.isalpha():
                clean_words.append(word)

        # Open and read the Longman Communication 3000 file
        with open(lc_file, 'r') as lc_file:
            lc_content = lc_file.read()

        # Find similar words between the SRT file and Longman Communication 3000 file
        similar_words = []
        lc_words = lc_content.split()
        for clean_word in clean_words:
            for lc_word in lc_words:
                if clean_word != lc_word.lower():
                    similar_words.append(lc_word)

        # Remove duplicates by converting the list to a set
        synonyms = set(similar_words)

        return synonyms
    except FileNotFoundError:
        print("File not found. Please check the file paths.")
    except IOError:
        print("Error reading the file. Please ensure the files are accessible.")

# Get the file paths from user input
try:
    srt_file = input("Enter the path to the SRT file: ")
    lc_file = input("Enter the path to the Longman Communication 3000 file: ")

    similar_words = find_similar_words(srt_file, lc_file)
    print(similar_words)
except Exception as e:
    print("An error occurred:", str(e))
