#!/usr/bin/env python3
"""Test assignment 3 Trie class."""

import unittest

import Assignment_3

class TrieNode:
    def __init__(self,char):
        self.children = [None] * 26
        self.leaf_nodes = [] #list of leaf children
        self.is_end = False
        self.char = char
        self.count = 0

class Trie:
    def __init__(self,string_list):
        self.root = TrieNode(" ")
        self.string_list = string_list
        self.wildcard = []

        for word in string_list:
            self.insert(word)

    def insert(self, word):
        current_node = self.root

        if len(word) == 0:
            return

        for char in word:
            index = ord(char) - ord('a')
            if current_node.children[index] is None:
                current_node.children[index] = TrieNode(char)
                current_node.leaf_nodes.append(index)
                current_node.leaf_nodes = sorted(current_node.leaf_nodes)
            current_node = current_node.children[index]

        current_node.is_end = True
        current_node.count += 1


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
        current_node = self.root

        if len(query_str) == 0:
            return len(self.string_list)

        #get to the end of the prefix
        for char in query_str:
            index = ord(char) - ord('a')

            if current_node.children[index] is not None or current_node.is_end:
                current_node = current_node.children[index]
            else:
                return 0

        if current_node is not None:
            if current_node.count > 0:
                #get number of children + number of how many repeats of that string
                return len(current_node.leaf_nodes) + current_node.count
            else:
                return len(current_node.leaf_nodes)
        return 0

    def wildcard_prefix_freq(self, query_str):
        if len(query_str) == 0:
            return []

        output_list = []
        current_node = self.root

        # get prefix and suffix
        question_mark = query_str.index("?")
        prefix_query = query_str[0:question_mark]
        suffix_query = query_str[question_mark + 1: len(query_str)]

        # prefix -> iterate until you find ?
        for char in prefix_query:
            index = ord(char) - ord('a')
            if current_node.children[index] is not None or current_node.is_end:
                current_node = current_node.children[index]
            else:
                output_list.append(prefix_query + current_node.char + suffix_query)
        # we have the child array of current node which is array of integers

        child_array = current_node.leaf_nodes

        if suffix_query != "":

            if current_node.char == " ":
                return []

            # for the index of each child
            for index in child_array:

                suffix_found = True
                letter = chr(index + 97)
                current = current_node.children[index]

                if current is None:
                    return []

                for suffix in suffix_query:
                    index = ord(suffix) - ord('a')

                    if current.children[index] is None:
                        suffix_found = False
                        break

                if suffix_found:
                    self.wildcard_prefix_aux(current.children[index], prefix_query + letter + suffix_query, query_str,
                                             output_list)

        # suffix does not exist -> ? is at the end
        else:
            if query_str == "?":
                self.wildcard_prefix_aux(current_node, prefix_query, query_str, output_list)

            else:
                for index in child_array:

                    suffix_found = True
                    letter = chr(index + 97)
                    current = current_node.children[index]

                    if current is None:
                        return []

                    for suffix in prefix_query:
                        index = ord(suffix) - ord('a')

                        if current.children[index] is None:
                            suffix_found = False
                            break

                    if suffix_found:
                        self.wildcard_prefix_aux(current.children[index], prefix_query, query_str, output_list)

        return self.wildcard

    def wildcard_prefix_aux(self, current_node, current_string, query, strings=[]):
        if current_node.is_end:
            if len(current_string) >= len(query):
                for i in range(current_node.count):
                    self.wildcard.append(current_string)
        for index in current_node.leaf_nodes:
            self.wildcard_prefix_aux(current_node.children[index], current_string + chr(index + 97), strings)


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

    # def test_string_freq_example(self):
    #     """Test `string_freq` on spec example."""
    #     self.assertEqual(self.trie.string_freq("aa"), 3)
    #
    # def test_string_freq_absent(self):
    #     """Test `string_freq` with non-matching strings."""
    #     for absentee in ["c", "abc", "abbac", "aacb"]:
    #         with self.subTest(absentee=absentee):
    #             self.assertEqual(self.trie.string_freq(absentee), 0)
    #
    # def test_prefix_freq_example(self):
    #     """Test `prefix_freq` on spec example."""
    #     self.assertEqual(self.trie.prefix_freq("aa"), 8)
    #
    # def test_prefix_freq_empty(self):
    #     """Test `prefix_freq` on empty prefix."""
    #     self.assertEqual(self.trie.prefix_freq(""), len(self.text))
    #
    # def test_prefix_freq_absent(self):
    #     """Test `prefix_freq` with non-matching queries."""
    #     for absentee in ["aaaa", "c", "ac", "aabc", "aabac"]:
    #         with self.subTest(absentee=absentee):
    #             self.assertEqual(self.trie.prefix_freq(absentee), 0)

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

