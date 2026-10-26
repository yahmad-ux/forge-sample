import unittest

from forge_sample.textstats import line_count, top_words, word_count, words


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


if __name__ == "__main__":
    unittest.main()
