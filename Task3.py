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
    max_number = (max(num_list))
    copy_of_num_list = num_list[:]
    new_temp_list = num_list[:]
    len_max_number = len(max_number)

    while (len_max_number != 0):
        new_temp_list = list_conversion(new_temp_list,position)
        new_temp_list = radix_sort(new_temp_list,10)

        #map numbers
        for i in range(len(new_temp_list)):
            b = new_temp_list.index(new_temp_list[i],i)
            new_temp_list[i] = copy_of_num_list[b]

        position += 1
        len_max_number -= 1

    print(new_temp_list)
    return new_temp_list

def list_conversion(list_to_convert,position):

    temp_list = []
    for number in list_to_convert:
        if number[position] != 0:
            element = ord((number[len(number) - position - 1]))
            temp_list.append(element)
        else:
            temp_list.append(0)
    return temp_list

a = ['aaa','cab','abc','cab','xyze']

print(find_rotations(a, 1))