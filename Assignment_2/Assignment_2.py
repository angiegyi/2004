def longest_oscillation(L):
    """
    finds the longest oscillation in a given list of integers
    time complexity: O(N) where n is the list of the input list
    space complexity: O(N) where n is the list of the input list
    :param L: list of integers
    :return: int of longest oscillation, list of longest length oscillation indexes
    """
    memo = len(L) * [1]

    if len(L) == 0:
        return 0, []

    if len(L) == 1:
        return (1,[0])

    #initial check
    needs_max = determine_flag(L[0],L[1])

    i = 0
    j = i + 1

    while j < len(L):
        prev_j = j

        # iterate through: looking for the next biggest element
        if needs_max is True:
            if L[i] < L[j]: #if previous < next
                while j < len(L)-1 and L[j+1] > L[j]: #is finding the max element
                    memo[j] = max(memo[i] + 1, (memo[j])) #while it hasnt found the peak, the best we can do is the previous one
                    j += 1
                if j == len(L)-1:  #to stop it from going n^2
                    memo[j] = max(memo[i] + 1, (memo[j]))
                    break
                else:
                    memo[j] = max(memo[i]+1, (memo[j]))
                    j = prev_j
                    needs_max = False
            elif L[i] == L[j]: #edge case: if the next elements are equal
                memo[j] = memo[i]

        # looking for the next smallest element
        elif needs_max is False:
            if L[i] > L[j]: #if previous > next
                while j < len(L) - 1 and L[j + 1] < L[j]: #iterates through to find
                    memo[j] = max(memo[i] + 1, (memo[j]))
                    j += 1
                if j == len(L)-1: #to stop it from going n^2
                    memo[j] = max(memo[i] + 1, (memo[j]))
                    break
                else:
                    memo[j] = max(memo[i]+1, (memo[j]))
                    needs_max = True
                    j = prev_j
            elif L[i] == L[j]: #edge case: if the next elements are equal
                memo[j] = memo[i]

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
    takes in two integers, compares them and determines if the next digit must be greater or less than the current digit using a boolean
    Time Complexity: O(1) constant time comparison
    Space Complexity: O(1)
    :param a: integer a
    :param b: integer b
    :return: boolean indicating whether next integer must be > or < then current
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
    Time Complexity: O(n) where n is the length of the memo array
    Space Complexity: O(n) where n is the length of the memo array
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
        return [0]

    return output_index

# ------------- Task 2 -----------------------------

def longest_walk(M):
    """
    taking in a 2D matrix of integers, the longest increasing walk in the matrix will be returned
    Complexity: O(MN) where M is the width of the matrix and N is the height
    Space Complexity: O(MN))
    :param M: 2D matrix of numbers
    :return: a tuple containing an integer representing the longest increasing walk and its corresponding path
    """

    if len(M) == 0:
        return 0, []

    #make table
    memo = [[None for _ in range(len(M[0]))] for _ in range(len(M))]
    max_path = 0

    #O(mn)
    max_occurrance_list = find_max(M)

    for option in max_occurrance_list:
        if option != None:
            memo[option[0]][option[1]] = 1

    # O(mn)
    for i in range(len(M)):
        for j in range(len(M[0])):
            path_length = calculate_walk(M,i,j,memo)
            max_path = max(path_length, max_path)

    #to get the path
    path_taken = reverse_find_neighbour(memo,max_path)
    return max_path,path_taken

def valid_neighbour(matrix, current_position):
    """
    given a current position, valid neighbour will return a list of positions which you can move to
    Time Complexity: O(1) will run for a constant 9 loops for each direction
    Space Complexity: O(1) -> O(9) max worst case for the length of directions
    :param matrix: 2D matrix of numbers
    :param current_position: tuple (i,j) representing current position
    :return: list of possible valid moves in tuples (i,j)
    """
    direction = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]

    original_row = current_position[0]
    original_column = current_position[1]

    valid_neighbour = []

    #iterates through the 9 directions to see which positions are viable
    for i in range(len(direction)):
        row_dir = direction[i][0]
        col_dir = direction[i][1]

        if (0 <= original_row + row_dir < len(matrix)) and (0 <= original_column + col_dir < len(matrix[0])):
            if matrix[original_row][original_column] < matrix[row_dir+original_row][col_dir+original_column]:
                if (original_row+row_dir,original_column+col_dir) != current_position:
                    valid_neighbour.append((original_row+row_dir,original_column+col_dir))

    return valid_neighbour


def reverse_find_neighbour(memo,target):
    """
    given the final memo table, this function works backwards to find the path taken
    Time Complexity: O(mn) * O(1) will run for a constant 9 loops for each position in the matrix
    Space Complexity: O(mn) max worst case occurs when the path uses every position in the table
    :param matrix: O(1)
    :param target: length of max path in the memo table
    :return: returns a list of integer tuples which hold the path taken
    """
    direction = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]

    for i in range(len(memo)):
        for j in range(len(memo[0])):
            if memo[i][j] == target:
                current = (i,j)
                break

    original_row = current[0]
    original_column = current[1]

    valid_neighbour = []
    valid_neighbour.append((original_row,original_column))

    for _ in range(len(memo)+len(memo[0])):
        for i in range(len(direction)):
            row_dir = direction[i][0]
            col_dir = direction[i][1]

            together_row = original_row + row_dir
            together_col = original_column + col_dir

            if (0 <= together_row < len(memo)) and (0 <= together_col < len(memo[0])):
                if memo[together_row][together_col] == (memo[original_row][original_column]-1):
                    valid_neighbour.append((together_row,together_col))
                    original_row = together_row
                    original_column = together_col
                    break

    return valid_neighbour

def find_max(matrix):
    """
    finds occurrences of the maximum element in the list
    Time Complexity: O(mn)
    Space Complexity: O(mn) worst case
    :param matrix: M x N matrix
    :return: returns a list of tuples containing occurances of the maximum element in the list
    """
    max_val = -1
    max_list = []

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):  # O(n), where n is the columns
            if matrix[i][j] > max_val:
                max_val = matrix[i][j]

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):  # O(n), where n is the columns
            if matrix[i][j] == max_val:
                max_list.append((i, j))

    return max_list

def calculate_walk(matrix, i ,j,memo):
    """
    recursive function to find the max length path at starting index i,j
    Time Complexity: O(1) if result is in memo otherwise O(mn) if path hasnt been calculated yet
    Space Complexity: where O() no extra space is created
    :param matrix: 2D matrix of numbers
    :param i: starting row (integer)
    :param j: starting column (integer)
    :param memo: 2D matrix of numbers storing longest path
    :return: return integer representation of longest path at matrix[i][j]
    """

    #if a number already has been stored, O(1) lookup
    if memo[i][j] != None:
        return memo[i][j]

    valid = valid_neighbour(matrix,(i,j))

    #this keeps track of the maximum path length
    max_length = 0

    if len(valid) == 0:
        memo[i][j] = 1
        return memo[i][j]

    for move in valid:
        path_length = 1 + calculate_walk(matrix,move[0],move[1],memo)
        max_length = max(max_length,path_length)
    memo[i][j] = max_length
    return max_length

