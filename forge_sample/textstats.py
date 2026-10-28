"""Word counts for plain text.

Helpers:
- words: the lowercased words in text.
- word_count: the number of words.
- line_count: the number of lines.
- char_count: the number of characters, not counting newlines.
- top_words: the most common words and their counts.
- sentence_count: the number of sentences ended by ".", "!" or "?".
"""

import re
from collections import Counter

_WORD = re.compile(r"[A-Za-z0-9']+")
_SENTENCE_END = re.compile(r"[.!?]+")


def words(text: str) -> list[str]:
    """Return the words in text, lowercased, in order."""
    return [word.lower() for word in _WORD.findall(text)]


def word_count(text: str) -> int:
    """Return the number of words in text."""
    return len(words(text))


def line_count(text: str) -> int:
    """Return the number of lines in text.

    Empty text has 0 lines. A trailing newline does not add a line.
    """
    return len(text.splitlines())


def char_count(text: str) -> int:
    """Return the number of characters in text, not counting newlines.

    Line feed and carriage return both count as newlines, so a Windows line
    ending adds 0.
    """
    return len(text.replace("\r", "").replace("\n", ""))


def top_words(text: str, n: int) -> list[tuple[str, int]]:
    """Return the n most common words and their counts, most common first.

    Words with the same count keep the order in which they first appear.
    """
    if n < 0:
        raise ValueError("n must be zero or more")
    return Counter(words(text)).most_common(n)


def sentence_count(text: str) -> int:
    """Return the number of sentences in text.

    A sentence ends with ".", "!" or "?". A run of these marks, such as "?!"
    or "...", counts once. Empty or whitespace-only text has 0 sentences.
    """
    return len(_SENTENCE_END.findall(text))
