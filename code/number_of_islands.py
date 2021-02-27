"""
Dropbox

Number of Islands


Given a 2d grid map of 1s (land) and 0s (water), count the number of islands.
An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.
You may assume all four edges of the grid are all surrounded by water.

i.e. count the number of connected components in a grid.
Ask if you can modify the grid. If you can, then you can use a flood fill.
If not, then you'll need to use O(Rows * Cols) space to store a grid or set to store the visited spots.
"""

class NumberOfIslands:

    def __init__(self, grid):
        self.grid = grid
        self.R = 0
        self.C = 0
        self.num_islands = 0
        self.directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    
    def process_grid(self):
        if not self.grid or not self.grid[0]: #You got null, [], or [[]]
            return self.num_islands
        self.R = len(self.grid)
        self.C = len(grid[0])
        for row in range(self.R):
            for col in range(self.C):
                if self.grid[row][col] == 1: #If you find land, flood that island so that
                    #you don't double count the same island
                    self.flood(row, col)
                    self.num_islands += 1
        return self.num_islands

    def flood(self, row, col):
        if not (0 <= row < self.R) or not (0 <= col < self.C) or self.grid[row][col] != 1:
            return
        self.grid[row][col] = 0 #flood with water so that you don't revisit the square
        for dr, dc in self.directions:
            self.flood(row + dr, col + dc)

if __name__ == "__main__":
    board = [
        [0, 1, 1, 0, 0, 0],
        [1, 0, 1, 1, 0, 0],
        [1, 0, 1, 0, 1, 0]
    ]
    processor = NumberOfIslands(board)
    assert processor.process_grid() == 3


"""
FOLLOW UP:
What if there is too much data to store in memory:
Answer: Read it in row by row in the form of streams. Use a union find.
Also observe that you only need information about the previous row for the union find if reading row-by-row.
"""