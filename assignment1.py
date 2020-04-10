import timeit
import random

def counting_sort(num_list,pos,base):
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
        element = int(number//base ** pos) % base
        temp_list.append(element)
        count[element] += 1

    for i in range(1,len(position)):
        position[i] = position[i-1] + count[i-1]

    for i in range(len(num_list)):
        index = temp_list[i]
        output[position[index]] = num_list[i]
        position[index] += 1

    return output

def radix_sort(num_list,base):
    """
    radix sort is a sorting algorithm which takes in a list of integers and sorts numbers on their representation in base b using counting sort and returns a sorted integer list.
    Complexity: O((N+b)M) where N is the number of integers in num_list, b is the base and M
    is the length of the largest number in the list represented in base b.
    :param num_list: non empty list of integers
    :param base: integer for the numbers to be sorted in the base
    :return: a sorted list of integers
    """

    assert len(num_list) != 0, 'cannot have an empty list'

    max_number = max(num_list)
    new_temp_list = num_list[:]

    position = 0
    while (max_number != 0):
        new_temp_list = counting_sort(new_temp_list,position,base)
        position += 1
        max_number = max_number//base

    return new_temp_list

def time_radxix_sort():

    test_data = [random.randint(1, (2 ** 64) - 1) for _ in range(100000)]
    output_array = []

    base_list = [2,8,64,512,4096,32768,100000]

    for base in base_list:
        start = timeit.default_timer()
        radix_sort(test_data,base)
        stop = (timeit.default_timer() - start)
        output_array.append((base,stop))

    return output_array

from Task_1 import radix_sort, counting_sort

def pad_function(input_list):
    """
    Pads strings which arent of equal length to the longest string in the inoput list
    Complexity: O(m*n) where n is the length of the input list and m is the length of the longest string in the list
    adds 0's
    :param input_list:
    :return: a list of strings which are of equal length
    """
    max_len = len(input_list[0])

    for x in range(1, len(input_list)):
        if (len(input_list[x]) > max_len):
            max_len = len(input_list[x])

    for i in range(len(input_list)):
        for j in range(len(input_list[i]), max_len):
            input_list[i] = "0" + input_list[i]

    return input_list


def rotate_string(input_string, p):
    """
    rotates the string using a rotation size p
    Complexity: O(m) where m is the size of the input list
    :param input_string: non empty input string
    :param p: rotation size p
    :return: string rotated to size p
    """
    output = ""
    p = p % len(input_string)

    if p < 0:
        for i in range(len(input_string) + p, len(input_string)):
            output += input_string[i]
        for i in range(len(input_string) + p):
            output += input_string[i]
    elif p >= 0:
        for i in range(p, len(input_string)):
            output += input_string[i]
        for i in range(p):
            output += input_string[i]
    return output


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


def conversion_back(input_number):
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


def find_rotations(string_list, p):
    """
    given a non empty list of strings and a rotation size p, find_rotations finds all the strings in the list
    whos p-rotations also appear in the list, outputted in the form of a string list.
    Complexity O(nm) = O(5n + 4mn): where n is the length of the input list and m is the most ammount of letters in a word
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
    temp = pad_function(temp)
    copy_of_string_list = pad_function(copy_of_string_list)

    #convert letters to numbers
    for i in range(len(temp)):
        temp[i] = conversion_intstring(temp[i])
        copy_of_string_list[i] = conversion_intstring(copy_of_string_list[i])

    #sort both lists
    output = radix_sort(temp, 100)
    copy_of_string_list = radix_sort(copy_of_string_list, 100)

    #get the duplicates
    output = merge(copy_of_string_list, output)

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

