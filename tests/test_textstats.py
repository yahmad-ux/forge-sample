import unittest

from forge_sample.textstats import top_words, word_count, words


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
