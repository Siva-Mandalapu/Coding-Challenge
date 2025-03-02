import os
import re
import sys
from collections import Counter

def find_files(directory, extension=".txt"):
## generator function scans a directory recursively for files with a specific extension 
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(root, file)

def count_word_occurrences(directory, extension=".txt", min_occurrences=2):
## Reads all matching files, counts word occurrences, and filters words appearing more than min_occurrences times.
    word_counter = Counter()
    word_pattern = re.compile(r'\b\w+\b')  # Matches words

    for file_path in find_files(directory, extension):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                words = word_pattern.findall(file.read().lower())  # Normalize to lowercase
                word_counter.update(words)
        except Exception as e:
            print(f"Error reading {file_path}: {e}", file=sys.stderr)

    # Filter words exceeding the minimum occurrence threshold
    frequent_words = {word: count for word, count in word_counter.items() if count > min_occurrences}

    # Sort by frequency in descending order
    return sorted(frequent_words.items(), key=lambda item: item[1], reverse=True)

def main():
# The main function takes user input and runs the word count process.
    directory = input("Enter your directory path to scan: ").strip()

    if not os.path.isdir(directory):
        print("Error: Invalid directory path.", file=sys.stderr)
        sys.exit(1)

    results = count_word_occurrences(directory)

    if results:
        print("\nWord Frequency Count:")
        for word, count in results:
            print(f"{word} {count}")
    else:
        print("No words met the occurrence threshold.")

if __name__ == "__main__":
    main()
