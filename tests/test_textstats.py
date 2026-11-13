import os
import tempfile
import unittest

from forge_sample.textstats import (
    average_word_length,
    char_count,
    file_word_count,
    line_count,
    sentence_count,
    top_words,
    word_count,
    word_frequencies,
    words,
)


class WordsTest(unittest.TestCase):
    def test_splits_and_lowercases(self) -> None:
        self.assertEqual(words("Hello, World! hello"), ["hello", "world", "hello"])

    def test_keeps_apostrophes(self) -> None:
        self.assertEqual(words("It's done"), ["it's", "done"])

    def test_empty_text(self) -> None:
        self.assertEqual(words(""), [])


class WordCountTest(unittest.TestCase):
    def test_counts_words(self) -> None:
        self.assertEqual(word_count("one two  three"), 3)

    def test_punctuation_only(self) -> None:
        self.assertEqual(word_count("... !"), 0)


class LineCountTest(unittest.TestCase):
    def test_empty_text(self) -> None:
        self.assertEqual(line_count(""), 0)

    def test_single_line_without_newline(self) -> None:
        self.assertEqual(line_count("one"), 1)

    def test_multiple_lines(self) -> None:
        self.assertEqual(line_count("one\ntwo\nthree"), 3)

    def test_trailing_newline_adds_no_line(self) -> None:
        self.assertEqual(line_count("one\ntwo\n"), 2)

    def test_blank_lines_are_counted(self) -> None:
        self.assertEqual(line_count("one\n\ntwo"), 3)


class CharCountTest(unittest.TestCase):
    def test_empty_text(self) -> None:
        self.assertEqual(char_count(""), 0)

    def test_counts_spaces_and_punctuation(self) -> None:
        self.assertEqual(char_count("a b, c"), 6)

    def test_newlines_are_not_counted(self) -> None:
        self.assertEqual(char_count("one\ntwo\n"), 6)

    def test_windows_newlines_are_not_counted(self) -> None:
        self.assertEqual(char_count("one\r\ntwo"), 6)

    def test_only_newlines(self) -> None:
        self.assertEqual(char_count("\n\n"), 0)


class TopWordsTest(unittest.TestCase):
    def test_most_common_first(self) -> None:
        self.assertEqual(top_words("b a b c b a", 2), [("b", 3), ("a", 2)])

    def test_ties_keep_first_seen_order(self) -> None:
        self.assertEqual(top_words("x y z", 2), [("x", 1), ("y", 1)])

    def test_zero_returns_empty(self) -> None:
        self.assertEqual(top_words("a b", 0), [])

    def test_negative_n_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            top_words("a", -1)


class WordFrequenciesTest(unittest.TestCase):
    def test_mixed_case_is_counted_together(self) -> None:
        self.assertEqual(word_frequencies("Fig fig FIG"), [("fig", 3)])

    def test_punctuation_is_stripped(self) -> None:
        self.assertEqual(
            word_frequencies("plum, plum! (kiwi)"), [("plum", 2), ("kiwi", 1)]
        )

    def test_ties_keep_first_seen_order(self) -> None:
        self.assertEqual(
            word_frequencies("pear apple lime"),
            [("pear", 1), ("apple", 1), ("lime", 1)],
        )

    def test_empty_text(self) -> None:
        self.assertEqual(word_frequencies(""), [])

    def test_repeated_words_sorted_by_count(self) -> None:
        self.assertEqual(
            word_frequencies("b a b c b a"), [("b", 3), ("a", 2), ("c", 1)]
        )


class AverageWordLengthTest(unittest.TestCase):
    def test_averages_word_lengths(self) -> None:
        self.assertEqual(average_word_length("plum pear fig"), 3.67)

    def test_exact_average(self) -> None:
        self.assertEqual(average_word_length("ab abcd"), 3.0)

    def test_punctuation_is_not_counted(self) -> None:
        self.assertEqual(average_word_length("fig, kiwi! (plum)"), 3.67)

    def test_apostrophes_count_as_letters(self) -> None:
        self.assertEqual(average_word_length("it's ok"), 3.0)

    def test_empty_text(self) -> None:
        self.assertEqual(average_word_length(""), 0.0)

    def test_punctuation_only_text(self) -> None:
        self.assertEqual(average_word_length("... !"), 0.0)


class FileWordCountTest(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)

    def write(self, name: str, text: str) -> str:
        path = os.path.join(self.dir.name, name)
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)
        return path

    def test_counts_words_in_file(self) -> None:
        path = self.write("a.txt", "plum pear\nfig, kiwi!\n")
        self.assertEqual(file_word_count(path), 4)

    def test_reads_utf8_text(self) -> None:
        path = self.write("u.txt", "café plum")
        self.assertEqual(file_word_count(path), 2)

    def test_empty_file(self) -> None:
        self.assertEqual(file_word_count(self.write("e.txt", "")), 0)

    def test_missing_file_raises(self) -> None:
        missing = os.path.join(self.dir.name, "missing.txt")
        with self.assertRaises(FileNotFoundError):
            file_word_count(missing)

    def test_directory_raises(self) -> None:
        with self.assertRaises(IsADirectoryError):
            file_word_count(self.dir.name)


if __name__ == "__main__":
    unittest.main()


class SentenceCountTest(unittest.TestCase):
    def test_counts_each_terminator(self) -> None:
        self.assertEqual(sentence_count("One. Two! Three?"), 3)

    def test_run_of_terminators_counts_once(self) -> None:
        self.assertEqual(sentence_count("Really?! Yes... ok."), 3)

    def test_empty_text(self) -> None:
        self.assertEqual(sentence_count(""), 0)

    def test_whitespace_only_text(self) -> None:
        self.assertEqual(sentence_count(" \n\t "), 0)

    def test_text_without_terminator(self) -> None:
        self.assertEqual(sentence_count("no ending here"), 0)
