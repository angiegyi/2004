def longest_walk(M):
    """
    taking in a 2D matrix of numbers, the longest increasing walk in the matrix will be outputted
    Complexity: O(MN) where M is the width of the matrix and N is the height
    :param M: 2D matrix of numbers
    :return: integer representing the longest increasing walk
    """

    if len(M) == 0:
        return 0

    memo = [[0 for _ in range(len(M[0]))] for _ in range(len(M))]
    max_path = 0

    for i in range(len(M)):
        for j in range(len(M[0])):
            path_length = calculate_walk(M,i,j,memo)
            memo[i][j] = path_length
            max_path = max(path_length, max_path)

    return max_path

def valid_neighbour(matrix, current_position):
    """
    given a current position, valid neighbour will return a list of positions which you can move to
    Complexity: O(1) will run for a constant 9 loops for each direction
    :param matrix:
    :param current_position:
    :return:
    """
    direction = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]

    original_row = current_position[0]
    original_column = current_position[1]

    valid_neighbour = []

    for i in range(len(direction)):
        row_dir = direction[i][0]
        col_dir = direction[i][1]

        if (0 <= original_row + row_dir < len(matrix)) and (0 <= original_column + col_dir < len(matrix[0])):
            #if the original position < desired position
            if matrix[original_row][original_column] < matrix[row_dir+original_row][col_dir+original_column]:
                if (original_row+row_dir,original_column+col_dir) != current_position:
                    valid_neighbour.append((original_row+row_dir,original_column+col_dir))
    return valid_neighbour

def calculate_walk(matrix, i ,j,memo):
    """
    recursive function to find the max length path at starting index i,j
    Complexity: O(1) straight lookup if result is in memo otherwise O(mn) if path hasnt been calculate yet
    :param matrix: 2D matrix of numbers
    :param i: starting row (integer)
    :param j: starting column (integer)
    :param memo: 2D matrix of numbers storing longest path
    :return: return longest path at matrix[i][j]
    """

    #if a number already has been stored, O(1) lookup
    if memo[i][j] > 0:
        return memo[i][j]

    valid = valid_neighbour(matrix,(i,j))
    max_length = 0

    if len(valid) == 0:
        return 1

    for move in valid:
        path_length = 1 + calculate_walk(matrix,move[0],move[1],memo)
        max_length = max(max_length,path_length)
    return max_length

print(longest_walk([[1,2,3],[1,2,1]]))