def valid_neighbour(matrix, current_position):
    """
    given a current position, valid neighbour will return a list of positions which you can move to
    :param matrix:
    :param current_position:
    :return:
    """
    direction = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]

    original_row = current_position[1]
    original_column = current_position[0]

    valid_neighbour= []

    for i in range(len(direction)):
        row_dir = direction[i][0]
        col_dir = direction[i][1]
        if (0 <= original_row + row_dir < len(matrix)) and (0 <= original_column+ col_dir < len(matrix[0])):
            #if the original position < desired position
            if matrix[original_row][original_column] < matrix[row_dir+original_row][col_dir+original_column]:
                valid_neighbour.append((original_row+row_dir,original_column+col_dir))


    return valid_neighbour


def longest_walk(M):

    if len(M) == 0:
        return 0

    memo = [[0 for _ in range(len(M[0]))] for _ in range(len(M))]

    for i in range(len(M)):
        for j in range(len(M[0])):
            if memo[i][j] == 0:
                memo[i][j] = calculate_walk(M,i,j)
            else:
                memo[i][j] += 1
    return memo[-1][-1]



def calculate_walk(matrix, i ,j):

    valid = valid_neighbour(matrix,(i,j))
    max_length = 0

    for move in valid:
        path_length = 1 + calculate_walk(matrix,move[0],move[1])
        max_length = max(max_length,path_length)
    return max_length

print(longest_walk([[4,6],[7,2]]))