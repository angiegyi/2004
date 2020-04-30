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

