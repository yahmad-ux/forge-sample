"""Word counts for plain text.

Helpers:
- words: the lowercased words in text.
- word_count: the number of words.
- line_count: the number of lines.
- char_count: the number of characters, not counting newlines.
- top_words: the most common words and their counts.
- word_frequencies: every word and its count, most common first.
- sentence_count: the number of sentences ended by ".", "!" or "?".
- average_word_length: the average length of the words, to 2 places.
- file_word_count: the number of words in a UTF-8 text file.
- redact_personal_data: text with email addresses and phone numbers replaced.
"""

import re
from collections import Counter

_WORD = re.compile(r"[A-Za-z0-9']+")
_SENTENCE_END = re.compile(r"[.!?]+")
# The lookbehind keeps a long run without "@" from being rescanned at every offset.
_EMAIL = re.compile(
    r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"
)
_INTERNATIONAL_PHONE = re.compile(r"(?<![\w+])\+\d+(?:[\s.-]?\(\d+\)|[\s.-]\d+)*")
_DIGITS = re.compile(r"\d+")
_MIN_INTERNATIONAL_DIGITS = 7
_MAX_INTERNATIONAL_DIGITS = 15
_US_PHONE = re.compile(
    r"(?<![\w(])(?:\+?1[\s.-]?)?(?:\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}(?!\d)"
)


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


def word_frequencies(text: str) -> list[tuple[str, int]]:
    """Return every word in text with its count, most common first.

    Words are lowercased and stripped of punctuation by words(). Words with
    the same count keep the order in which they first appear.
    """
    return Counter(words(text)).most_common()


def sentence_count(text: str) -> int:
    """Return the number of sentences in text.

    A sentence ends with ".", "!" or "?". A run of these marks, such as "?!"
    or "...", counts once. Empty or whitespace-only text has 0 sentences.
    """
    return len(_SENTENCE_END.findall(text))


def average_word_length(text: str) -> float:
    """Return the average length of the words in text, rounded to 2 places.

    Words come from words(), so apostrophes count as letters and other
    punctuation does not. Text with no words has an average of 0.0.
    """
    found = words(text)
    if not found:
        return 0.0
    return round(sum(len(word) for word in found) / len(found), 2)


def file_word_count(path: str) -> int:
    """Return the number of words in the UTF-8 text file at path.

    Raises FileNotFoundError if path does not exist and IsADirectoryError if
    path is a directory.
    """
    with open(path, encoding="utf-8") as file:
        return word_count(file.read())


def _redact_international(match: re.Match[str]) -> str:
    """Redact the leading digit groups of a match, up to 15 digits.

    Groups past the 15-digit limit, such as a year after the number, stay.
    """
    text = match.group()
    total = 0
    end = 0
    for group in _DIGITS.finditer(text):
        if total + len(group.group()) > _MAX_INTERNATIONAL_DIGITS:
            break
        total += len(group.group())
        end = group.end()
    if total < _MIN_INTERNATIONAL_DIGITS:
        return text
    if text.startswith(")", end):
        end += 1
    return "[phone]" + text[end:]


def redact_personal_data(text: str) -> str:
    """Return text with email addresses and phone numbers replaced.

    Email addresses become "[email]" and phone numbers become "[phone]". Phone
    numbers are US numbers with an optional +1 or 1 prefix (dashes, dots,
    spaces or parentheses, or 10 digits in a row), and international numbers
    that start with "+" and have 7 to 15 digits. All other text is unchanged.
    """
    text = _EMAIL.sub("[email]", text)
    text = _INTERNATIONAL_PHONE.sub(_redact_international, text)
    return _US_PHONE.sub("[phone]", text)
