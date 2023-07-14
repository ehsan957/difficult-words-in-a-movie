# Open and read the SRT file
with open('C:\\Users\\DELL\\Desktop\\How.I.Met.Your.Mother.S01E01.srt', 'r') as srt_file:
    srt_content = srt_file.read()

# Split the content into words
words = srt_content.split()

# Create a list to store words without special characters
clean_words = []
for word in words:
    if word.isalpha():
        clean_words.append(word)

# Open and read the Longman Communication 3000 file
with open('C:\\Users\\DELL\\Desktop\\Longman Communication 3000.txt', 'r') as lc_file:
    lc_content = lc_file.read()

# Find differnt words between the SRT file and Longman Communication 3000 file
different_words = []
lc_words = lc_content.split()
for clean_word in clean_words:
    for lc_word in lc_words:
        if clean_word != lc_word.lower():
            different_words.append(lc_word)

# Remove duplicates by converting the list to a set
synonyms = set(different_words)

# Print the set of different words
print(synonyms)
