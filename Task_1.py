import timeit
import random
import csv
import math

#this one has no base conversions
def counting_sort(num_list,pos,base):
    """
    final copy
    input a list of strings, sort by each index
    :param num_list:
    :param pos:
    :param base:
    :return:
    """

    #if digit is greater than base > raise assertion

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

def radix_sort(num_list,base=10):

    max_number = max(num_list)
    new_temp_list = num_list[:]

    position = 0
    while (max_number != 0):
        new_temp_list = counting_sort(new_temp_list,position,base)
        position += 1
        max_number = max_number//base

    return new_temp_list


    # base runs the best when length of base matches input

def time_radxix_sort():
    """
    :return:
    """
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
