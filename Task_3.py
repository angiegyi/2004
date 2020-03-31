from Task_1 import radix_sort, counting_sort

#this is the final task 3 copy

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


def rotate_string(string_enter, p):
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
    :param input_string: A valid non empty integer
    :return: String conversion
    """
    output = ""
    for i in range(0, len(input_string) - 1, 2):
        temp = input_string[i] + input_string[i + 1]
        a = chr(int(temp) + 70)
        output += str(a)
    return output


def find_rotations(string_list, p):

    assert len(string_list) != 0, 'cannot have an empty list'

    temp = []

    # rotate all the strings first O(m)
    for i in range(len(string_list)):
        rotated_string = rotate_string(string_list[i], p)
        temp.append(rotated_string)

    # apply padding (O(m))
    temp = lets_pad(temp)

    # O(nm) -> convert letters to numbers
    for i in range(len(temp)):
        temp[i] = conversion_intstring(temp[i])
    output = radix_sort(temp, 100)

    #convert back to numbers
    for i in range(len(output)):
        output[i] = str(conversion_back(str(output[i])))

    #convert input list

    copy_of_string_list = string_list[:]
    copy_of_string_list = lets_pad(copy_of_string_list)

    for i in range(len(copy_of_string_list)):
        copy_of_string_list[i] = conversion_intstring(copy_of_string_list[i])
    copy_of_string_list = radix_sort(copy_of_string_list, 100)

    for i in range(len(copy_of_string_list)):
        copy_of_string_list[i] = str(conversion_back(str(copy_of_string_list[i])))

    rename = merge(copy_of_string_list, output, -p)

    return rename


def merge(non_rotated_list, rotated_list, p):
    """
    using the merge algorithm, this function determines if the rotated string is in the input list
    Complexity: O(n) = O(n)*O(m), the summed lengths of sublists a and b
    :param non_rotated_list: string type list containing non rotated original input list of strings
    :param rotated_list: string type list containing rotated original input list of strings
    :return: a String list containing the duplicated rotated strings
    """

    new_list = []
    pointer1 = 0
    pointer2 = 0

    for i in range(len(non_rotated_list) + len(rotated_list)):

        if (i == (len(non_rotated_list) - 1)) or (i == (len(rotated_list) - 1)):
            return new_list
        else:
            if non_rotated_list[pointer1] == rotated_list[pointer2]:
                new_list.append(rotate_string(rotated_list[pointer2], p))
                pointer1 += 1
                pointer2 += 1

            elif non_rotated_list[pointer1] > rotated_list[pointer2]:
                pointer2 += 1
            else:
                pointer1 += 1

print(find_rotations(['qwertyui', 'wertyuiq', 'rtyuiqwe', 'asdfgh', 'dfghas'], 2))