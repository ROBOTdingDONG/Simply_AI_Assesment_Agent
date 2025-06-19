import sys

def count_words(filepath):
    try:
        with open(filepath, 'r') as file:
            text = file.read()
            words = text.split()
            return len(words)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python word_counter.py <filename>")
    else:
        filepath = sys.argv[1]
        word_count = count_words(filepath)
        if word_count is not None:
            print(f"The file '{filepath}' contains {word_count} words.")
