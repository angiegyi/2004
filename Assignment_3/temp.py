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

        print(current_node.count)

        if current_node is not None:
            if current_node.is_end:
                #get number of children + number of how many repeats of that string
                return len(current_node.leaf_nodes) + current_node.count + 1
            else:
                return len(current_node.leaf_nodes)
        return 0

    def wildcard_prefix_freq(self, query_str):
        if len(query_str) == 0:
            return []

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
                return []

        # we have the child array of current node which is array of integers
        child_array = current_node.leaf_nodes

        #node that doesnt exist
        if current_node.char == " ":
            if query_str[0] != "?":
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
                current = current.children[index]

            if suffix_found:
                self.wildcard_prefix_aux(current, prefix_query + letter + suffix_query, query_str)

        return self.wildcard

    def wildcard_prefix_aux(self, current_node, current_string, query):
        if current_node.is_end:
            if len(current_string) >= len(query):
                for i in range(current_node.count):
                    self.wildcard.append(current_string)
        for index in current_node.leaf_nodes:
            self.wildcard_prefix_aux(current_node.children[index], current_string + chr(index + 97),query)


words = ['aa', 'aab', 'bcd', 'aa', 'baa', 'bcd', 'aab', 'aa', 'bhde']

trie = Trie(words)
print(trie.prefix_freq('aa'))