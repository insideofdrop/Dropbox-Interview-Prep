"""
Game of Life:

The Game of Life is a cellular automaton devised by Conway in 1970.

The board is made up of an m x n grid of cells, where each cell has an initial state: 
alive = 1
dead = 0

Each cell interacts with its eight neighbors (horizontal, vertical, diagonal) using the following rules:

Any live cell with fewer than 2 live neighbors dies as if caused by under-population.
Any live cell with 2 or 3 live neighbors lives on to the next generation.
Any live cell with more than 3 live neighbors dies, as if by over-population.
Any dead cell with exactly 3 live neighbors becomes a live cell, as if by reproduction.

Determine the next state of the game.

Follow up:
1. How to save space?
- If using Java, use byte[][].
- Don't make an extra board. Just rewrite the current one.
- All you need is a set of the cells that are alive
2. What if this can't fit into an array?
- Read the rows as streams from a disk, read 3 rows at a time
3. What if we just give you generating functions G(row, col, time) for the cell states?
- Just do the math with the generating functions.

"""
class GameOfLife:
    
    def __init__(self, board):
        self.board = board
        self.R = len(board) #Corner case: null board or the board is [] or [[]]
        self.C = len(board[0])

        #2 = currently dead, will be alive
        #3 = currently alive, will be dead
        self.neighbors = ((1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1))

    def convertValues(self):
        for rowIdx, row in enumerate(self.board):
            for colIdx, value in enumerate(row):
                if value == 2:
                    self.board[rowIdx][colIdx] = 1
                elif value == 3:
                    self.board[rowIdx][colIdx] = 0

    def runIteration(self):
        for rowIdx, row in enumerate(self.board):
            for colIdx, value in enumerate(row):
                numLivingNeighbors = 0
                for dy, dx in self.neighbors:
                    if (0 <= rowIdx + dy < self.R) and (0 <= colIdx + dx < self.C) and self.board[rowIdx + dy][colIdx + dx] in (1, 3):
                        numLivingNeighbors += 1
                if value == 1 and (numLivingNeighbors > 3 or numLivingNeighbors < 2):
                    self.board[rowIdx][colIdx] = 3
                elif value == 0 and (numLivingNeighbors == 3):
                    self.board[rowIdx][colIdx] = 2
        print(self.board)

if __name__ == "__main__":
    game = GameOfLife(board)
    game.runIteration()
    game.convertValues()
    print(game.board)


"""
Infinite:
def gameOfLifeInfinite(self, live):
    ctr = collections.Counter((I, J)
                              for i, j in live
                              for I in range(i-1, i+2)
                              for J in range(j-1, j+2)
                              if I != i or J != j)
    return {ij for ij in ctr if ctr[ij] == 3 or ctr[ij] == 2 and ij in live}

def gameOfLife(self, board):
    live = {(i, j) for i, row in enumerate(board) for j, live in enumerate(row) if live}
    live = self.gameOfLifeInfinite(live)
    for i, row in enumerate(board):
        for j in range(len(row)):
            row[j] = int((i, j) in live)
"""
