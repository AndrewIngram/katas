import random


class Cell(object):
    def generate_choices(self):
        choices = range(1,10)
        random.shuffle(choices)
        self.choices = choices

    def next_value(self):
        return self.choices.pop()

    def __init__(self):
        self.generate_choices()
        self.value = None


class Puzzle(object):

    def __init__(self):
        self.grid = []
        for i in range(81):
            self.grid.append(Cell())

    def fetch_row(self, index):
        row = index / 9
        return self.grid[9*row:9*row+9]

    def fetch_column(self, index):
        column = index % 9
        return self.grid[column::9]

    def fetch_square(self, index):
        square_row = (index / 9) / 3
        square_column = (index % 9) / 3

        tl = (square_row * 27) + (square_column * 3)

        result = []

        result.extend(self.grid[tl:tl+3])
        result.extend(self.grid[tl+9:tl+12])
        result.extend(self.grid[tl+18:tl+21])

        return result

    def is_valid(self, index):
        
        row = [x.value for x in self.fetch_row(index)]
        column = [x.value for x in self.fetch_column(index)]
        square = [x.value for x in self.fetch_square(index)]

        cell = self.grid[index]
        val = cell.value

        if not val:
            val = cell.next_value()

        if val in row:
            return False

        if val in column:
            return False

        if val in square:
            return False

        cell.value = val
        return True

    def display_puzzle(self):
        line = '+-------+-------+-------+'

        print line

        for i in range(0,9):
            parts = ['|']
            subgrid = self.grid[9*i:(9*i)+3]
            parts.extend([str(x.value) for x in subgrid])
            parts.append('|')
            subgrid = self.grid[9*i+3:(9*i)+6]
            parts.extend([str(x.value) for x in subgrid])
            parts.append('|')
            subgrid = self.grid[9*i+6:(9*i)+9]
            parts.extend([str(x.value) for x in subgrid])
            parts.append('|')
            print ' '.join(parts)

            if i in (2,5):
                print line
        print line


    def build(self):
        index = 0

        while index < 81:
            valid = False
            while self.grid[index].choices:
                #import pdb; pdb.set_trace()
                if self.is_valid(index):
                    valid = True
                    index += 1
                    break
            # If it's not valid, we're going to backtrack
            if not valid:
                for i in range(index,0,-1):
                    if len(self.grid[i].choices):
                        index = i
                        self.grid[i].value = None
                        break
                    else:
                        self.grid[i].generate_choices()
                        self.grid[i].value = None


        self.display_puzzle()

if __name__ == "__main__":
    puzzle = Puzzle()
    puzzle.build()
