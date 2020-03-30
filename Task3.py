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
            input_list[i] = "0" + input_list[i]

    return input_list

def rotate_string(string_enter,p):
    """
    rotates string by p positions
    O(m) = O(2m)
    :param string_enter:
    :param p:
    :return:
    """

    temp = ""

    for i in range(p,len(string_enter)):
        temp += string_enter[i]

    for i in range(p):
        temp += string_enter[i]

    return temp

def conversion_intstring(input_string):
    return_list = ""
    for i in (input_string):
        if i == str(0):
            return_list += "0"
        else:
            return_list += ((str(ord(i))))
    return int(return_list)


def conversion_back(input_string):
    output = ""
    for i in range(0,len(input_string)-1,2):
        temp = input_string[i] + input_string[i+1]
        a = chr(int(temp))
        output += str(a)
    return output

print(conversion_back('979797'))

def find_rotations(string_list,p):

    temp = []

    #rotate all the strings first O(m)
    for i in range(len(string_list)):
        rotated_string = rotate_string(string_list[i],p)
        temp.append(rotated_string)

    #apply padding (O(m))
    temp = lets_pad(temp)

    #O(nm) -> convert letters to numbers
    for i in range(len(temp)):
        temp[i] = conversion_intstring(temp[i])

    output = radix_sort(temp,10)

    for i in range(len(output)):
        output[i] = str(conversion_back(str(output[i])))

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


def counting_sort(num_list,pos,base):
    """
    final copy
    input a list of strings, sort by each index
    :param num_list:
    :param pos:
    :param base:
    :return:
    """

    #sort right to left
    digits = []

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

#print(merge([1,2,3,4],[1,2,7,8]))

a = ['aaa','cab','abc','cab']

print(find_rotations(a, 1))