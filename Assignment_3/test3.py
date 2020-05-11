#!/usr/bin/env python3
"""Test assignment 3 Trie class."""

import unittest

import Assignment_3

class TrieNode:
    def __init__(self,char):
        self.children = [None] * 27
        self.leaf_count = [] #list of leaf children
        self.is_end = False
        self.char = char
        self.count = 0

class Trie:
    def __init__(self,string_list):
        self.root = TrieNode(" ")
        self.string_list = string_list

        for word in string_list:
            self.insert(word)

    def insert(self,word):
        current_node = self.root

        if len(word) == 0:
            return

        for char in word:
            index = ord(char) - ord('a')
            if current_node.children[index] is None:
                new_node = TrieNode(char)
                current_node.children[index] = new_node
            current_node.leaf_count += [current_node.children[index]]
            current_node = current_node.children[index]

        current_node.is_end = True
        current_node.count += 1
        current_node.leaf_count += [TrieNode(word[len(word)-1])]



    def search(self,word):
        if len(word) == 0:
            return True

        current_node = self.root
        for char in word:
            index = ord(char) - ord('a')
            if current_node.children[index] is None:
                return False
            else:
                current_node = current_node.children[index]
        return current_node.is_end


    def string_freq(self,query_str):

        if len(query_str) == 0:
            return 0

        current_node = self.root

        for char in query_str:
            index = ord(char) - ord('a')
            if current_node.children[index] is not None:
                current_node = current_node.children[index]
            else:
                return 0
        return current_node.count

    def prefix_freq(self,query_str):
        count = 0
        current_node = self.root

        if len(query_str) == 0:
            return len(self.string_list)

        #get to the end of the prefix
        for char in query_str:
            index = ord(char) - ord('a')
            if current_node.children[index] is not None or current_node.is_end:
                current_node = current_node.children[index]
        temp_node = current_node

        if temp_node != None:
            count += len(temp_node.leaf_count)
        return count




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

    # def test_wildcard_prefix_freq_example(self):
    #     """Test `wildcard_prefix_freq` with spec example."""
    #     self.assertEqual(
    #         self.trie.wildcard_prefix_freq("aa?"),
    #         ["aaa", "aaab", "aaab", "aab", "aaba"]
    #     )
    #
    # def test_wildcard_prefix_freq_minimal(self):
    #     """Test `wildcard_prefix_freq` on a single wildcard."""
    #     self.assertEqual(self.trie.wildcard_prefix_freq("?"), sorted(self.text))
    #
    # def test_wildcard_prefix_freq_too_long(self):
    #     """Test `wildcard_prefix_freq` with too-long queries."""
    #     self.assertEqual(self.trie.wildcard_prefix_freq("aaab?"), [])
    #     self.assertEqual(self.trie.wildcard_prefix_freq("?aaab"), [])
    #
    # def test_wildcard_prefix_absent(self):
    #     """Test `wildcard_prefix_freq` with non-matching queries."""
    #     for absentee in ["?c", "c?", "a?c", "bb?a", "ac?", "a?ac"]:
    #         with self.subTest(absentee=absentee):
    #             self.assertEqual(self.trie.wildcard_prefix_freq(absentee), [])
    #
    # def test_wildcard_prefix_match(self):
    #     """Test `wildcard_prefix_freq` with valid queries."""
    #     self.assertEqual(
    #         self.trie.wildcard_prefix_freq("a?a"),
    #         sorted(["aaa", "aaab", "aaab", "abaa"])
    #     )


if __name__ == "__main__":
    unittest.main()
