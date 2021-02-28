"""
Dropbox

Bottles of Soda / Combination Sum / Coin Change

This problem is given in the context of soda bottles or coins of different values.

This problem is usually for college interns.

Given a collection of soda bottles of different sizes, find all unique combinations of bottles that 
result in a given amount of soda.
"""

class CombinationSum:

    def __init__(self, bottles, target):
        self.bottles = bottles
        self.target = target
        self.result = []
        self.bottles.sort()
        self.num_bottles = len(bottles)

    def backtrack(self, remainder, combo, start_idx):
        if remainder == 0: #You've found a combination!
            self.results.append(combo[:]) #Add a deep copy of the combo to the results
            return
        elif remainder < 0:
            return
        for bottle_idx in range(start_idx, self.num_bottles):
            bottle_size = self.bottles[bottle_idx]
            if bottle_size > remainder:
                break #this bottle is too big, and all the rest of the bottles are also too big
            combo.append(bottle_size)
            self.backtrack(remainder - bottle_size, combo, bottle_idx)
            combo.pop()

    def process(self):
        self.backtrack(self.target, [], 0)
        return self.result