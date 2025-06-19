import unittest
import os
import sys

# Add src directory to sys.path to allow importing word_counter
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from word_counter import count_words

class TestWordCounter(unittest.TestCase):

    def setUp(self):
        # Create a dummy test file
        self.test_file_path = "test_file.txt"
        with open(self.test_file_path, "w") as f:
            f.write("This is a test file.\n")
            f.write("It has multiple lines and words.\n")
            f.write("  Leading and trailing spaces for this line.  \n")

        self.empty_file_path = "empty_file.txt"
        with open(self.empty_file_path, "w") as f:
            pass # Create an empty file

    def tearDown(self):
        # Remove the dummy test file
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
        if os.path.exists(self.empty_file_path):
            os.remove(self.empty_file_path)

    def test_count_words_normal_file(self):
        # Expected: "This", "is", "a", "test", "file.", "It", "has", "multiple", "lines", "and", "words.", "Leading", "and", "trailing", "spaces", "for", "this", "line."
        self.assertEqual(count_words(self.test_file_path), 18)

    def test_count_words_empty_file(self):
        self.assertEqual(count_words(self.empty_file_path), 0)

    def test_count_words_nonexistent_file(self):
        # Expecting None or some error indication, and a print to stderr
        # For now, we'll check if it returns None as per current word_counter.py implementation
        self.assertIsNone(count_words("nonexistent_file.txt"))

    def test_count_words_with_punctuation(self):
        # Create a file with punctuation
        punctuation_file_path = "punctuation_test.txt"
        with open(punctuation_file_path, "w") as f:
            f.write("Hello, world! This is a test.")
        # Expected: "Hello,", "world!", "This", "is", "a", "test." (6 words by current split logic)
        self.assertEqual(count_words(punctuation_file_path), 6)
        os.remove(punctuation_file_path)

if __name__ == "__main__":
    unittest.main()
