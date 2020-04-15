def longest_oscillation_greedy(L):
    """
    only gives consecutive oscillations
    """
    memo = len(L) * [1]

    if len(L) == 0:
        return [0]

    if len(L) == 1:
        return [1]


    #initial check
    needs_max = determine_flag(L[0],L[1])

    i = 0
    j = i + 1

    while j < len(L):
        prev_j = j

        # iterate through: looking for the next biggest element
        if needs_max is True:
            if L[i] < L[j]: #if previous < next
                while j < len(L)-1 and L[j+1] > L[j]: #is finding the max elemen
                    memo[j] = memo[i] #while it hasnt found the peak, the best we can do is the previous one
                    j += 1
                if j == len(L)-1:  #to stop it from going n^2
                    memo[j] = max(memo[i] + 1, (memo[j]))
                    break
                else:
                    memo[j] = max(memo[i]+1, (memo[j]))
                    j = prev_j
                    needs_max = False

        # looking for the next smallest element
        elif needs_max is False:
            if L[i] > L[j]: #if previous > next
                while j < len(L) - 1 and L[j + 1] < L[j]: #iterates through to find
                    memo[j] = memo[i]
                    j += 1
                if j == len(L)-1: #to stop it from going n^2
                    memo[j] = max(memo[i] + 1, (memo[j]))
                    break
                else:
                    memo[j] = max(memo[i]+1, (memo[j]))
                    needs_max = True
                    j = prev_j

        #if two items are equal
        else:
            if j > len(L)-2:
                j += 1
                i += 1
            else:
                memo[j] = memo[i]
                needs_max = determine_flag(L[i],L[j+1])

        j += 1
        i += 1

    return (memo[-1],get_numbers(memo))

def determine_flag(a,b):
    """
    takes in two intergers, compares them and determines if the next digit must be greater or less than the current digit using a boolean
    :param a: integer a
    :param b: integer b
    :return: boolean
    """
    if a < b:
        flag = True

    elif a > b:
        flag = False
    else:
        flag = None

    return flag

def get_numbers(memo):
    """
    takes in an input list of max subsequences at the ith inedex gets the indexes which make up the longest oscillation
    :param memo: the memo array
    :return: an array of integers at where the oscillations occur
    """

    output_index = []

    for i in range(len(memo)):
        current = memo[i]
        if (i != len(memo)-1):
            if memo[i + 1] <= current:
                continue
        output_index.append(i)

    #if all the numbers are the same
    if len(output_index) == 1:
        return [1]

    return output_index

print(longest_oscillation_greedy([0]))
