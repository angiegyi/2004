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

#print(time_radxix_sort())
