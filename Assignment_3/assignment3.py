class TrieNode:
    def __init__(self, char):
        self.children = [None] * 26
        self.leaf_nodes = []
        self.is_end = False
        self.char = char
        self.end_count = 0
        self.node_count = 0


class Trie:
    def __init__(self, string_list):
        """
        builds the trie by inserts word from input string_list
        :param string_list: list of strings to be inserted into Trie
        Complexity O(T): where T is the total numbers of characters in string list
        """
        self.root = TrieNode(" ")
        self.string_list = string_list
        self.wildcard = []

        for word in string_list:
            self.insert(word)

    def insert(self, word):
        """
        inserts a word into the Trie
        :param word: string word to be inserted
        Complexity O(T): where T is the total numbers of characters in string list
        """
        current_node = self.root

        if len(word) == 0:
            return

        for char in word:
            index = ord(char) - ord('a')

            if current_node.children[index] is None:
                current_node.children[index] = TrieNode(char)
                current_node.leaf_nodes.append(index)
            current_node.node_count += 1
            current_node = current_node.children[index]

        current_node.node_count += 1
        current_node.is_end = True
        current_node.end_count += 1

    def string_freq(self, query_str):
        """
        Given a query string, string_freq calculates the number of times that word has occurred
        :param query_str: string to be queried
        Complexity O(q) where q is the length of query_str
        :return: integer representing the number of query_str occurrences
        """

        if len(query_str) == 0:
            return 0

        current_node = self.root
        for char in query_str:
            index = ord(char) - ord('a')
            if current_node.children[index] is not None:
                current_node = current_node.children[index]
            else:
                return 0
        return current_node.end_count

    def prefix_freq(self, query_str):
        """
        Given a query string, prefix_freq calculates the number of words with prefix query_str
        :param query_str: string to be queried
        Complexity O(q) where q is the length of query_str
        :return: integer representing the number of words with query_str as a prefix
        """
        current_node = self.root

        if len(query_str) == 0:
            return len(self.string_list)

        # get to the end of the prefix
        for char in query_str:
            index = ord(char) - ord('a')
            if current_node.children[index] is not None:
                current_node = current_node.children[index]
            else:
                return 0

        return current_node.node_count

    def wildcard_prefix_freq(self, query_str):
        """
        given a query_str, wildcard_prefix_freq outputs the number of strings in the trie with the prefix query_str
        accounting for the ? wildcard
        :param query_str: string to be queried
        Complexity O(q + S) where q is the length of query_str and  where S is the total number of characters in all
        strings of text with prefix query_str
        :return: a list of strings with prefix query_str
        """
        if len(query_str) == 0:
            return []

        current_node = self.root

        # get prefix and suffix
        prefix_query = ""
        suffix_query = ""

        #O(q)
        for i in range(len(query_str)):
            if query_str[i] == "?":
                prefix_query = query_str[0:i]
                suffix_query = query_str[i + 1: len(query_str)]

        #O(q)
        # prefix -> iterate until you find ?
        for char in prefix_query:
            index = ord(char) - ord('a')
            if current_node.children[index] is not None:
                current_node = current_node.children[index]
            else:
                return []

        # we have the child array of current node which is array of integers
        child_array = current_node.leaf_nodes

        # node that doesnt exist
        if current_node.char == " ":
            if query_str[0] != "?":
                return []

        #O(q)
        #sort child array
        if len(child_array) != 0:
            child_array = self.counting_sort(child_array)

        #O(1)
        for index in child_array:
            suffix_found = True
            letter = chr(index + 97)
            current = current_node.children[index]

            if current is None:
                return []

            #check suffix lies in tree
            for suffix in suffix_query:
                index = ord(suffix) - ord('a')
                if current.children[index] is None:
                    suffix_found = False
                    break
                current = current.children[index]

            #O(S)
            #retrieve rest of word recursively
            if suffix_found:
                self.wildcard_prefix_aux(current, prefix_query + letter + suffix_query, query_str)

        return self.wildcard

    def wildcard_prefix_aux(self, current_node, current_string, query):
        """
        DFS to search for the rest of a current string
        :param current_node: current_node we are up to in traversal
        :param current_string: concatenated string
        :param query: query string from wildcard_prefix
        Complexity O(S) where S is the total number of characters in all strings of text with prefix query_str
        """
        if current_node.is_end:
            if len(current_string) >= len(query):
                for i in range(current_node.end_count):
                    self.wildcard.append(current_string)
        if len(current_node.leaf_nodes) != 0:
            current_node.leaf_nodes = self.counting_sort(current_node.leaf_nodes)
        for index in current_node.leaf_nodes:
            self.wildcard_prefix_aux(current_node.children[index], current_string + chr(index + 97), query)

    def counting_sort(self, num_list):
        """
        counting sort is a sorting alogrithm which takes in a list of integers and sorts them based on a key (in this case the place position).
        Complexity: O(N * U) where N is the length of the input list and U is the length of the largest digit to be sorted
        :param num_list: non empty list of integers
        :return: a sorted list of integers according to pos
        """

        count = [0] * 27
        position = [0] * 27
        output = [0] * len(num_list)

        for i in range(len(num_list)):
            current = num_list[i]
            count[current] += 1

        position[0] = 1

        for i in range(1, len(position)):
            position[i] = position[i - 1] + count[i - 1]

        for i in range(len(num_list)):
            index = num_list[i]
            output[position[index] - 1] = num_list[i]
            position[index] += 1

        return output


