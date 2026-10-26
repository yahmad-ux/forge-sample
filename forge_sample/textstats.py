"""Word counts for plain text."""

import re
from collections import Counter

_WORD = re.compile(r"[A-Za-z0-9']+")


def words(text: str) -> list[str]:
    """Return the words in text, lowercased, in order."""
    return [word.lower() for word in _WORD.findall(text)]


def word_count(text: str) -> int:
    """Return the number of words in text."""
    return len(words(text))


def top_words(text: str, n: int) -> list[tuple[str, int]]:
    """Return the n most common words and their counts, most common first.

    Words with the same count keep the order in which they first appear.
    """
    if n < 0:
        raise ValueError("n must be zero or more")
    return Counter(words(text)).most_common(n)
