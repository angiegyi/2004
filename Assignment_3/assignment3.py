class TrieNode:
    def __init__(self,char):
        self.children = [None] * 26
        self.leaf_nodes = [] #list of leaf children
        self.is_end = False
        self.char = char
        self.end_count = 0
        self.node_count = 0

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
            current_node.node_count += 1
            current_node = current_node.children[index]

        current_node.node_count += 1
        current_node.is_end = True
        current_node.end_count += 1

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
        return current_node.end_count

    def prefix_freq(self,query_str):
        current_node = self.root

        if len(query_str) == 0:
            return len(self.string_list)

        #get to the end of the prefix
        for char in query_str:
            index = ord(char) - ord('a')

            if current_node.children[index] is not None:
                current_node = current_node.children[index]
            else:
                return 0


        return current_node.node_count


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
            if current_node.children[index] is not None:
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

        print(self.wildcard)
        return self.radix_sort(self.wildcard,26)

    def wildcard_prefix_aux(self, current_node, current_string, query):
        if current_node.is_end:
            if len(current_string) >= len(query):
                for i in range(current_node.end_count):
                    self.wildcard.append(current_string)
        for index in current_node.leaf_nodes:
            self.wildcard_prefix_aux(current_node.children[index], current_string + chr(index + 97),query)

    def counting_sort(self, num_list, pos, base):
        """
        counting sort is a sorting alogrithm which takes in a list of integers and sorts them based on a key (in this case the place position).
        Complexity: O(N * U) where N is the length of the input list and U is the length of the largest digit to be sorted
        :param num_list: non empty list of integers
        :param pos: integer position to determine place value
        :param base: integer for the numbers to be sorted in the base
        :return: a sorted list of integers according to pos
        """

        count = [0] * (base)
        position = [0] * base
        output = [0] * len(num_list)

        temp_list = []

        for number in (num_list):
            element = int(number // base ** pos) % base
            temp_list.append(element)
            count[element] += 1

        for i in range(1, len(position)):
            position[i] = position[i - 1] + count[i - 1]

        for i in range(len(num_list)):
            index = temp_list[i]
            output[position[index]] = num_list[i]
            position[index] += 1

        return output

    def radix_sort(self, num_list, base):
        """
        radix sort is a sorting algorithm which takes in a list of integers and sorts numbers on their representation in base b using counting sort and returns a sorted integer list.
        Complexity: O((N+b)M) where N is the number of integers in num_list, b is the base and M
        is the length of the largest number in the list represented in base b.
        :param num_list: non empty list of integers
        :param base: integer for the numbers to be sorted in the base
        :return: a sorted list of integers
        """

        assert len(num_list) != 0, 'cannot have an empty list'

        for i in range(len(num_list)):
            num_list[i] = self.conversion_intstring(num_list[i])

        max_number = max(num_list)
        new_temp_list = num_list[:]

        position = 0
        while (max_number != 0):
            new_temp_list = self.counting_sort(new_temp_list, position, base)
            position += 1
            max_number = max_number // base

        print(new_temp_list)

        for i in range(len(new_temp_list)):
            new_temp_list[i] = self.conversion_back(str(new_temp_list[i]))

        return new_temp_list

    def conversion_intstring(self,input_string):
        """
        Converts a character to its corresponding number representation
        Complexity: O(m) where m is the length of the input string
        :param input_string: A valid non empty integer
        :return: string representation of input integer
        """
        return_list = ""
        for i in (input_string):
            if i == str(0):
                return_list += "0"
            else:
                return_list += (str(ord(i) - 70))
        return int(return_list)

    def conversion_back(self,input_number):
        """
        Converts the number representation back to character representation
        Complexity: O(m) where m is the length of the input string
        :param input_number: A valid non empty integer
        :return: string representation of input integer
        """
        output = ""
        for i in range(0, len(input_number) - 1, 2):
            temp = input_number[i] + input_number[i + 1]
            a = chr(int(temp) + 70)
            output += str(a)
        return output




words = ['aht', 'qy', 'fqkkg', 'v']

trie = Trie(words)
print(trie.wildcard_prefix_freq('?'))