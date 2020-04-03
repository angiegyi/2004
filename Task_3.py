from Task_1 import radix_sort, counting_sort

#this is the final task 3 copy

def lets_pad(input_list):
    """
    Pads strings which arent of equal length to the longest string in the inoput list
    Complexity: O(m*n) where n is the length of the input list and m is the length of the longest string in the list
    adds 0's
    :param input_list:
    :return: a list of strings which are of equal length
    """
    max = len(input_list[0])

    for x in range(1, len(input_list)):
        if (len(input_list[x]) > max):
            max = len(input_list[x])

    for i in range(len(input_list)):
        for j in range(len(input_list[i]), max):
            input_list[i] = "0" + input_list[i]

    return input_list


#
def rotate_string(string_enter, p):
    """
    rotates the string using a rotation size p
    :param string_enter: non empty input string
    :param p: rotation size p
    :return: string rotated to size p
    """
    temp = ""
    while abs(p) > len(string_enter):
        if p > 0:
            p -= len(string_enter)
        else:
            p += len(string_enter)
    if p >= 0:
        for i in range(p, len(string_enter)):
            temp += string_enter[i]
        for i in range(p):
            temp += string_enter[i]
    elif p < 0:
        for i in range(len(string_enter) + p, len(string_enter)):
            temp += string_enter[i]
        for i in range(len(string_enter)+p):
            temp += string_enter[i]
    return temp


def conversion_intstring(input_string):
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


def conversion_back(input_string):
    """
    Converts the number representation back to character representation
    Complexity: O(m) where m is the length of the input string
    :param input_string: A valid non empty integer
    :return: integer representation of input string
    """
    output = ""
    for i in range(0, len(input_string) - 1, 2):
        temp = input_string[i] + input_string[i + 1]
        a = chr(int(temp) + 70)
        output += str(a)
    return output


def find_rotations(string_list, p):
    """
    given a non empty list of strings and a rotation size p, find_rotations finds all the strings in the list
    whos p-rotations also appear in the list, outputted in the form of a string list.
    Complexity O(nm) = O(n + n + m*n + n + n + mn + mn + n + m*n): where n is the length of the input list and m is the most ammount of letters in a word
    :param string_list: a non empty list of strings
    :param p: the number of left/right rotations
    :return: a list of strings containing strings whos rotated string is also in string_list
    """

    assert len(string_list) != 0, 'cannot have an empty list'

    temp = []
    copy_of_string_list = string_list[:]

    #rotate all the strings first list
    for i in range(len(string_list)):
        rotated_string = rotate_string(string_list[i], p)
        temp.append(rotated_string)

    #apply padding
    temp = lets_pad(temp)
    copy_of_string_list = lets_pad(copy_of_string_list)

    #convert letters to numbers
    for i in range(len(temp)):
        temp[i] = conversion_intstring(temp[i])
        copy_of_string_list[i] = conversion_intstring(copy_of_string_list[i])

    #sort both lists
    output = radix_sort(temp, 100)
    copy_of_string_list = radix_sort(copy_of_string_list, 100)

    #get the duplicates
    output = merge(copy_of_string_list, output)
    print(output)

    #convert back to numbers
    for i in range(len(output)):
        output[i] = rotate_string(str(conversion_back(str(output[i]))),-p)

    return output


def merge(non_rotated_list, rotated_list):
    """
    using the merge algorithm, this function determines if the rotated string is in the input list
    Complexity: O(n) where n is the size of the input list
    :param non_rotated_list: string type list containing non rotated original input list of strings
    :param rotated_list: string type list containing rotated original input list of strings
    :return: a String list containing the duplicated rotated strings
    """

    new_list = []
    pointer1 = 0
    pointer2 = 0

    for i in range(len(non_rotated_list) + len(rotated_list)):
        if (pointer1 == (len(non_rotated_list))) or (pointer2 == (len(rotated_list))):
            return new_list
        else:
            if non_rotated_list[pointer1] == rotated_list[pointer2]:
                new_list.append((rotated_list[pointer2]))
                pointer1 += 1
                pointer2 += 1

            elif non_rotated_list[pointer1] > rotated_list[pointer2]:
                pointer2 += 1
            else:
                pointer1 += 1

print(find_rotations((['abcdefgh', 'ghabcdef', 'qwerty', 'qwerty', 'ertyqw']),-2))