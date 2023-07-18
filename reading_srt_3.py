def find_similar_words(srt_file, lc_file):
    try:
        # Open and read the SRT file
        with open(srt_file, 'r') as srt_file:
            srt_content = srt_file.read()

        # Split the content into words
        words = srt_content.split()

        # Create a list to store words without numbers
        clean_words = [word for word in words if  word is not int]

        # Open and read the Longman Communication 3000 file
        with open(lc_file, 'r') as lc_file:
            lc_content = lc_file.read()

        # Find different words between the SRT file and Longman Communication 3000 file
        similar_words = [lc_word for lc_word in lc_content.split() if lc_word.lower() not in clean_words]

        # Remove duplicates by converting the list to a set
        synonyms = set(similar_words)

        return synonyms
    except FileNotFoundError:
        print("File not found. Please check the file paths.")
    except IOError:
        print("Error reading the file. Please ensure the files are accessible.")

try:
    # Get the file paths from user input
    srt_file = input("Enter the path to the SRT file: ")
    lc_file = input("Enter the path to the Longman Communication 3000 file: ")
# ...

    similar_words = find_similar_words(srt_file, lc_file)
    sorted_words = sorted(similar_words)  # Sort the words alphabetically

    for word in sorted_words:
        print(word)

except Exception as e:
    print("An error occurred:", str(e))
