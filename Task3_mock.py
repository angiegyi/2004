from Task_1 import counting_sort, radix_sort

def lets_pad(input_list):
    """
    O(m*n + n)
    adds 0's
    :param input_list:
    :return:
    """
    max = len(input_list[0])

    for x in range(1, len(input_list)):
        if (len(input_list[x]) > max):
            max = len(input_list[x])

    for i in range(len(input_list)):
        for j in range(len(input_list[i]), max):
            input_list[i] = input_list[i] + "0"

    return input_list

def rotate_string(string_enter,p):
    """
    -> needs to accomodate for right rotations(-p)
    rotates string by p positions
    O(m) = O(2m)
    :param string_enter:
    :param p:
    :return:
    """
    temp = ""
    if p >= 0:
        for i in range(p, len(string_enter)):
            temp += string_enter[i]
        for i in range(p):
            temp += string_enter[i]
    elif p < 0:
        for i in range(len(string_enter) + p, len(string_enter)):
            temp += string_enter[i]
        for i in range(len(string_enter) + p):
            temp += string_enter[i]

def find_rotations(string_list,p):

    temp = []

    #rotate all the strings first O(m)
    for i in range(len(string_list)):
        rotated_string = rotate_string(string_list[i],p)
        temp.append(rotated_string)

    #padding
    temp = lets_pad(temp)
    output = list_conversion_to_num(temp)
    out = merge(string_list,output)

    return out

def merge(non_rotated_list, rotated_list):
    """
    using the merge algorithm, this function determines if the rotated string is in the input list
    Complexity: O(n) where n = a + b, the summed lengths of sublists a and b
    :param non_rotated_list: string type list containing non rotated original input list of strings
    :param rotated_list: string type list containing rotated original input list of strings
    :return:
    """

    #how do you get the original unrotated string

    new_list = []
    pointer1 = 0
    pointer2 = 0

    for i in range(len(non_rotated_list)+len(rotated_list)):

        if (i == (len(non_rotated_list)-1)) or (i == (len(rotated_list)-1)):
            return new_list
        else:
            if non_rotated_list[pointer1] == rotated_list[pointer2]:
                new_list.append(non_rotated_list[pointer1])
                pointer1 += 1
                pointer2 += 1
            elif non_rotated_list[pointer1] > rotated_list[pointer2]:
                pointer2 += 1
            else:
                pointer1 += 1

def list_conversion_to_num(num_list):

    position = 0
    len_max_number = len(max(num_list))

    new_temp_list = num_list[:]
    temp_string_list = num_list[:]

    while (len_max_number != 0):

        #this holds the number conversions
        new_temp_list = list_conversion(temp_string_list,position)
        temp = new_temp_list[:]
        copy_of_num_list = radix_sort(temp,10)


        #map numbers
        for i in range(len(new_temp_list)):
            b = temp.index(copy_of_num_list[i],i)
            temp_string_list[i] = temp_string_list[b]
        position += 1
        len_max_number -= 1

    return new_temp_list

def list_conversion(list_to_convert,position):

    temp_list = []

    for number in list_to_convert:
        if number[len(number)-position-1] != '0':
            element = ord((number[len(number) - position - 1]))
            temp_list.append(element)
        else:
            temp_list.append(0)
    return temp_list


def list_num_conversion(string_list):
    position = 0
    len_max_number = len(max(string_list))

    input_copy = string_list[:]

    while (len_max_number != 0):

        to_num = list_conversion(input_copy,position)
        sorted_to_num = radix_sort(to_num,10)

        for i in range(len(input_copy)):
            input_copy[i] = input_copy[to_num.index(sorted_to_num[i],i)]

        position += 1
        len_max_number -= 1

    return input_copy

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

    position = 0
    len_max_number = len(max(num_list))

    input_copy = num_list[:]

    while (len_max_number != 0):

        to_num = list_conversion(input_copy, position)
        sorted_to_num = radix_sort(to_num, 10)

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

a = ['aaa0','cab0','abc0','cab0','xyze']

print(list_num_conversion(['aaa0', 'abc0', 'bca0', 'abc0', 'yzex']))