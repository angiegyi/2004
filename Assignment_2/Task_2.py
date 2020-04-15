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
        if (original_row + row_dir >= 0 and original_row + row_dir < len(matrix)) and (original_column+ col_dir >= 0 and original_column + col_dir < len(matrix[0])):
            if matrix[original_row][original_column] < matrix[row_dir+original_row][col_dir+original_column]:
                valid_neighbour.append((original_row+row_dir,original_column+col_dir))

    return valid_neighbour


a = [
    [3,4,6,7],
    [5,8,3,1]

    ]

# 0 = row (y) 1 = col (x)
print(len(a[0])/len(a))
print(valid_neighbour(a,(0,0)))