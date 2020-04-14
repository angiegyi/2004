def longest_oscillation_greedy(L):
    """
    only gives consecutive oscillations
    """
    memo = len(L) * [1]
    output = []

    if len(L) == 0:
        return [0]

    #initial check
    flag = determine_flag(L[0],L[1])

    i = 0
    j = i + 1

    while j < len(L):
        prev_j = j

        # iterate through: looking for the next biggest element
        if flag is True:
            if L[i] < L[j]: #if previous < next
                while j < len(L)-1 and L[j+1] > L[j]: #is finding the peak
                    memo[j] = memo[i] #while it hasnt found the peak, the best we can do is the previous one
                    j += 1
                memo[j] = max(memo[i]+1, (memo[j]))
                j = prev_j
                flag = False

        # looking for the next smallest element
        elif flag is False:
            if L[i] > L[j]: #if previous > next
                while j < len(L) - 1 and L[j + 1] < L[j]: #
                    memo[j] = memo[i]
                    j += 1
                memo[j] = max(memo[i]+1, (memo[j]))
                flag = True
                j = prev_j

        #if two items are equal
        else:
            if j > len(L)-2:
                j += 1
                i += 1

            else:
                memo[j] = memo[i]
                flag = determine_flag(L[i],L[j+1])

        j += 1
        i += 1

    return (memo[-1],get_numbers(memo))

def determine_flag(a,b):
    if a < b:
        flag = True

    elif a > b:
        flag = False
    else:
        flag = None

    return flag

def get_numbers(memo):

    output_index = []

    i = 0
    while i < len(memo):
        j = i
        if j < len(memo)-1:
            while memo[j] == memo[j + 1]:
                j += 1
        output_index.append(j-1) #may be affecting it
        i = j
        i += 1
    return output_index

print(get_numbers([1,1,2,3,3,4,4,5,6,7]))

def longest_oscillation(L):
    """
    only gives consecutive oscillations
    """
    memo = len(L) * [1]

    #initial check

    if L[0] < L[1]:
        flag = True

    if L[0] > L[1]:
        flag = False

    i = 0
    j = i + 1

    while j < len(L):

        if flag is True:
            if L[i] < L[j]:
                memo[j] = max(memo[i]+1, (memo[j]))
                flag = False
        else:
            if L[i] > L[j]:
                memo[j] = max(memo[i]+1, (memo[j]))
                flag = True

        j += 1
        i += 1

    return memo

#print(longest_oscillation_greedy([3,3,2]))
