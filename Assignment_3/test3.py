#!/usr/bin/env python3
"""Test assignment 3 Trie class."""

import unittest

from Assignment_3 import Task_1


class TestTrie(unittest.TestCase):
    """Test the `Trie` class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = [
            "aa",
            "aab",
            "aaab",
            "abaa",
            "aa",
            "abba",
            "aaba",
            "aaa",
            "aa",
            "aaab",
            "abbb",
            "baaa",
            "baa",
            "bba",
            "bbab"
        ]
        self.trie = Trie(self.text)

    def test_string_freq_example(self):
        """Test `string_freq` on spec example."""
        self.assertEqual(self.trie.string_freq("aa"), 3)

    def test_string_freq_absent(self):
        """Test `string_freq` with non-matching strings."""
        for absentee in ["c", "abc", "abbac", "aacb"]:
            with self.subTest(absentee=absentee):
                self.assertEqual(self.trie.string_freq(absentee), 0)

    def test_prefix_freq_example(self):
        """Test `prefix_freq` on spec example."""
        self.assertEqual(self.trie.prefix_freq("aa"), 8)

    def test_prefix_freq_empty(self):
        """Test `prefix_freq` on empty prefix."""
        self.assertEqual(self.trie.prefix_freq(""), len(self.text))

    def test_prefix_freq_absent(self):
        """Test `prefix_freq` with non-matching queries."""
        for absentee in ["aaaa", "c", "ac", "aabc", "aabac"]:
            with self.subTest(absentee=absentee):
                self.assertEqual(self.trie.prefix_freq(absentee), 0)

    def test_wildcard_prefix_freq_example(self):
        """Test `wildcard_prefix_freq` with spec example."""
        self.assertEqual(
            self.trie.wildcard_prefix_freq("aa?"),
            ["aaa", "aaab", "aaab", "aab", "aaba"]
        )

    def test_wildcard_prefix_freq_minimal(self):
        """Test `wildcard_prefix_freq` on a single wildcard."""
        self.assertEqual(self.trie.wildcard_prefix_freq("?"), sorted(self.text))

    def test_wildcard_prefix_freq_too_long(self):
        """Test `wildcard_prefix_freq` with too-long queries."""
        self.assertEqual(self.trie.wildcard_prefix_freq("aaab?"), [])
        self.assertEqual(self.trie.wildcard_prefix_freq("?aaab"), [])

    def test_wildcard_prefix_absent(self):
        """Test `wildcard_prefix_freq` with non-matching queries."""
        for absentee in ["?c", "c?", "a?c", "bb?a", "ac?", "a?ac"]:
            with self.subTest(absentee=absentee):
                self.assertEqual(self.trie.wildcard_prefix_freq(absentee), [])

    def test_wildcard_prefix_match(self):
        """Test `wildcard_prefix_freq` with valid queries."""
        self.assertEqual(
            self.trie.wildcard_prefix_freq("a?a"),
            sorted(["aaa", "aaab", "aaab", "abaa"])
        )


if __name__ == "__main__":
    unittest.main()
