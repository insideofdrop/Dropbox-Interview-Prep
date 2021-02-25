"""
Grid Illumination: 

This problem is usually given in phone screens.

This problem is basically like checking whether a square on a chessboard is within
the attack range of a queen.

Suppose you have lights on a grid. The light illuminates all the squares up and down, left and right,
and all the diagonal squares. Given a list of locations for lights and a list of squares to check
for illumination, return an array indicating whether each square to check is illuminated.
"""

"""
Every square on the same top-left to bottom-right diagonal as a light has the same value for (row - col). 
This is because each square on that diagonal can be expressed as (r + k, c + k), where (r, c) is a square
on the diagonal and k is some integer. Then (r + k) - (c + k) = r - c + k - k = r - c, which is always the same.

Every square on the same top-right to bottom-left diagonal has the same value for (row + col) because
those squares can be expressed as (r + k, c - k), so (r + k) + (c - k) = r + c + k - k = r + c is constant.

Every square on the same row has the same row num, every square on the same col has the same col num...
"""

def illuminated(grid_size, lights, squares_to_check):
    output = [False] * len(squares_to_check)
    top_left_bottom_right_diagonal = set()
    top_right_bottom_left_diagonal = set()
    rows = set()
    cols = set()
    for lit_row, lit_col in lights:
        top_left_bottom_right_diagonal.add(lit_row - lit_col)
        top_right_bottom_left_diagonal.add(lit_row + lit_col)
        rows.add(lit_row)
        cols.add(lit_col)
    for idx in range(len(squares_to_check)):
        row, col = squares_to_check[idx]
        if not (0 <= row < grid_size) or not (0 <= col < grid_size):
            raise OffTheGridException(f"Row: {row}, Col: {col} is off the grid") 
            #error since it's not on the board
        if ((row in rows) or 
            (col in cols) or 
            ((row - col) in top_left_bottom_right_diagonal) or
            ((row + col) in top_right_bottom_left_diagonal)):
            output[idx] = False
        else:
            output[idx] = True
    return output
