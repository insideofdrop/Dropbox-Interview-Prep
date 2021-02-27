"""
Dropbox

Sharpness Values

Things to consider:
- Ask questions to clarify and let interviewer know you understand the problem before coding
- Explain the concept how it is DP = min(max(..,..,..), self)
- Space optimization, tell the interviewer the observation it just depends on prev column result.


Sometimes, the interviewer will say "all values greater than X" or "the area is flooding with water".
This just means that you have an additional constraint that value > x.

You might also be asked 
"""

def sharpness_value(matrix):
    if not matrix or not matrix[0]:
        return -1
    R = len(matrix)
    C = len(matrix[0])

    sharpness_column = [-1] * R #column to hold the previous sharpness values
    for row in range(R):
        sharpness_column[row] = matrix[row][0]
    
    for col in range(1, C):
        for row in range(R):
            prev_sharpness = sharpness_column[row]
            if row > 0: #You can look back at the previous row
                prev_sharpness = max(prev_sharpness, sharpness_column[row - 1])
            if row < R - 1: #You can look ahead to the next row
                prev_sharpness = max(prev_sharpness, sharpness_column[row + 1])
            sharpness_column[row] = max(prev_sharpness, matrix[row][col])
    return min(sharpness_column)

"""
If the matrix is very large:
Can process the matrix in horizontal strips, minding the boundary of the strip depends on the previous and next strips.

Or you can read it column by column each time (many disk seek() because of the way array is stored). Helps to have it stored in random access files

Or transpose the file: same if read row, output col, many disk seek() when write; 
if read col, output row, many disk seek() when read
we can according to the memory size, each time read a square matrix, and do the transpose of it. 
Then do the processing row by row.
"""
