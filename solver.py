import sys
from math import floor


class Cell:

    def __init__(self, puzzle, row_index, column_index):
        self.puzzle = puzzle
        self.row = self.puzzle.rows[row_index]
        self.puzzle.rows[row_index].cells.append(self)
        self.column = self.puzzle.columns[column_index]
        self.puzzle.columns[column_index].cells.append(self)
        self.value = 0
        self.solved = False

        self.row_index = row_index
        self.column_index = column_index

        self.tile_index = len(self.puzzle.tiles[floor(column_index / 3) + floor(row_index / 3) * 3].cells)
        self.tile = self.puzzle.tiles[floor(column_index / 3) + floor(row_index / 3) * 3]
        self.puzzle.tiles[floor(column_index / 3) + floor(row_index / 3) * 3].cells.append(self)

        if self.puzzle.configuration[row_index][column_index] == 0:
            self.possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        else:
            self.possible_values = [self.puzzle.configuration[row_index][column_index]]
            self.value = self.possible_values[0]
            self.set_solved()

    def set_solved(self):
        print(self.row.contains, self.column.contains, self.tile.contains)
        print(self.row_index, self.column_index, ": ", self.value)
        self.solved = True
        self.tile.contains.append(self.value)
        self.row.contains.append(self.value)
        self.column.contains.append(self.value)
        self.possible_values = [self.value]

    def update_possible_values(self):
        possibilities = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        eliminated_vals = set(self.row.contains + self.column.contains + self.tile.contains)
        possible_values = list(possibilities.difference(eliminated_vals))

        if len(possible_values) < len(self.possible_values):
            self.possible_values = possible_values

        return self.possible_values

    def check_only_solution(self):
        if not self.solved:
            self.update_possible_values()

            if len(self.possible_values) == 1:

                self.value = self.possible_values[0]

                self.set_solved()

                self.puzzle.rule_updates[0] += 1

            elif len(self.possible_values) == 0:
                print("Failed Puzzle:")
                print(self.puzzle.print_puzzle())
                raise Exception("Cell ({x}, {y}) has no solution in Rule 1. Puzzle is likely unsolvable.".format(x = self.row_index, y = self.column_index))

    def check_only_possibility(self):
        if not self.solved:
            self.update_possible_values()

            row_possibilities = []
            column_possibilities = []
            tile_possibilities = []
            for i in range(9):
                if i != self.column_index:
                    row_possibilities += self.row.cells[i].possible_values
                if i != self.row_index:
                    column_possibilities += self.column.cells[i].possible_values
                if i != self.tile_index:
                    tile_possibilities += self.tile.cells[i].possible_values

            if (self.row_index == 2 and self.column_index == 0):
                print("3,7:")
                print(row_possibilities, column_possibilities, tile_possibilities)
                print(self.row.contains, self.column.contains, self.tile.contains)

            row_possibilities = list(set(self.possible_values).difference(set(row_possibilities)))
            column_possibilities = list(set(self.possible_values).difference(set(column_possibilities)))
            tile_possibilities = list(set(self.possible_values).difference(set(tile_possibilities)))

            if (self.row_index == 2 and self.column_index == 0):
                print("3,7:")
                print(row_possibilities, column_possibilities, tile_possibilities)
                print(self.row.contains, self.column.contains, self.tile.contains)

            if len(row_possibilities) > 1 or len(column_possibilities) > 1 or len(tile_possibilities) > 1:
                self.puzzle.print_puzzle()
                print(row_possibilities, column_possibilities, tile_possibilities)
                print(self.row.contains)
                print(self.possible_values)
                print(self.solved)
                raise Exception(
                    "Cell ({x}, {y}) has no solution in Rule 2. Puzzle is likely unsolvable.".format(x=self.row_index,
                                                                                                     y=self.column_index))
            elif len(row_possibilities) == 1:
                self.value = row_possibilities[0]
                self.set_solved()
                self.puzzle.rule_updates[1] += 1

            elif len(column_possibilities) == 1:
                self.value = column_possibilities[0]
                self.set_solved()
                self.puzzle.rule_updates[1] += 1

            elif len(tile_possibilities) == 1:
                self.value = tile_possibilities[0]
                self.set_solved()
                self.puzzle.rule_updates[1] += 1

    def check_for_pairs(self):
        if not self.solved:
            self.update_possible_values()
            matches = [[], [], []]

            for i in range(9):
                if i != self.column_index and self.row.cells[i] not in matches[0] and self.row.cells[i].update_possible_values() == self.possible_values:
                    matches[0].append(self.row.cells[i])
                if i != self.row_index and self.column.cells[i] not in matches[1] and self.column.cells[i].update_possible_values() == self.possible_values:
                    matches[1].append(self.column.cells[i])
                if i != self.tile_index and self.tile.cells[i] not in matches[2] and self.tile.cells[i].update_possible_values() == self.possible_values:
                    matches[2].append(self.tile.cells[i])

            if len(matches[0]) >= len(self.possible_values) - 1:
                for i in range(9):
                    if self.row.cells[i] is not self and self.row.cells[i] not in matches[0]:
                        p_values = self.row.cells[i].possible_values
                        self.row.cells[i].possible_values = list(set(self.row.cells[i].possible_values).difference(self.possible_values))
                        if self.row.cells[i].possible_values != p_values:
                            self.puzzle.rule_updates[2] += 1

            if len(matches[1]) >= len(self.possible_values) - 1:
                for i in range(9):
                    if self.column.cells[i] is not self and self.column.cells[i] not in matches[1]:
                        p_values = self.column.cells[i].possible_values
                        self.column.cells[i].possible_values = list(set(self.column.cells[i].possible_values).difference(self.possible_values))
                        if self.column.cells[i].possible_values != p_values:
                            self.puzzle.rule_updates[2] += 1

            if len(matches[2]) >= len(self.possible_values) - 1:
                for i in range(9):
                    if self.tile.cells[i] is not self and self.tile.cells[i] not in matches[2]:
                        p_values = self.tile.cells[i].possible_values
                        self.tile.cells[i].possible_values = list(set(self.tile.cells[i].possible_values).difference(self.possible_values))
                        if self.tile.cells[i].possible_values != p_values:
                            self.puzzle.rule_updates[2] += 1

    def check_exclusion(self):
        if not self.solved:
            self.update_possible_values()

            removed_values = []

            for i in range(len(self.possible_values)):

                for j in range(9):

                    if self.column.cells[j] not in self.tile.cells and self.possible_values[i] in self.column.cells[j].possible_values:
                        remove = True
                        for t in self.column.cells[j].tile.cells:
                            if t not in self.column.cells and self.possible_values[i] in t.possible_values:
                                remove = False

                        if remove:
                            removed_values.append(self.possible_values[i])

                    if self.row.cells[j] not in self.tile.cells and self.possible_values[i] in self.row.cells[j].possible_values:
                        remove = True
                        for t in self.row.cells[j].tile.cells:
                            if t not in self.row.cells and self.possible_values[i] in t.possible_values:
                                remove = False

                        if remove:
                            removed_values.append(self.possible_values[i])

            for r in removed_values:
                if r in self.possible_values:
                    self.possible_values.remove(r)
                    self.puzzle.rule_updates[3] += 1



class Puzzle_Segment:

    def __init__(self):
        self.cells = []
        self.contains = []

    def print_segment(self):
        for c in self.cells:
            print(c.value)


class Puzzle:

    def __init__(self, configuration):
        self.configuration = configuration
        self.rows = []
        self.columns = []
        self.tiles = []
        self.cells = []

        self.rule_updates = [0,0,0,0]

        for i in range(9):
            self.rows.append(Puzzle_Segment())
            self.columns.append(Puzzle_Segment())
            self.tiles.append(Puzzle_Segment())

        for i in range(9):
            for j in range(9):
                self.cells.append(Cell(self, i, j))


    def rule_1(self):
        print("Rule 1:")
        for c in self.cells:
            c.check_only_solution()

    def rule_2(self):
        print("Rule 2:")
        for c in self.cells:
            c.check_only_possibility()

    def rule_3(self):
        print("Rule 3:")
        for c in self.cells:
            c.check_for_pairs()

    def rule_4(self):
        print("Rule 4:")
        for c in self.cells:
            c.check_exclusion()

    def print_puzzle(self):
        grid = []
        for c in self.cells:
            grid.append(c.value)

        for i in range(0, 81, 9):
            print(grid[i:i + 3], grid[i + 3:i + 6], grid[i + 6:i + 9])


class Solver:

    def __init__(self, configuration):
        self.initial_configuration = configuration
        self.puzzle = Puzzle(configuration)

    # def rule_1(self):
    #     last_rule_1 = self.puzzle.rule_1_updates
    #
    #     while True:
    #         self.puzzle.rule_1()
    #
    #         if last_rule_1 == self.puzzle.rule_1_updates:
    #             break
    #
    #         else:
    #             last_rule_1 = self.puzzle.rule_1_updates
    #
    #
    #     print(self.puzzle.rule_1_updates)

    def solve(self):
        last_update = sum(self.puzzle.rule_updates)

        while True:
            print(last_update)
            self.puzzle.rule_1()

            if last_update == sum(self.puzzle.rule_updates):
                self.puzzle.rule_2()
                if last_update == sum(self.puzzle.rule_updates):
                    self.puzzle.rule_3()
                    if last_update == sum(self.puzzle.rule_updates):
                        self.puzzle.rule_4()
                        if last_update == sum(self.puzzle.rule_updates):
                            print(sum(self.puzzle.rule_updates))
                            break

            last_update = sum(self.puzzle.rule_updates)


        print(self.puzzle.rule_updates)





if __name__ == "__main__":
    arguments = sys.argv

    input_file = arguments[1]
    if len(arguments) == 3:
        output_file = arguments[2]

    with open(input_file) as file:
        raw_text = file.read()

    raw_config = []
    for character in raw_text:
        if character not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            raw_config.append(0)
        else:
            raw_config.append(int(character))

    grid = raw_config
    for i in range(0, 81, 9):
        print(grid[i:i + 3], grid[i + 3:i + 6], grid[i + 6:i + 9])

    raw_config = [raw_config[:9], raw_config[9:18], raw_config[18:27], raw_config[27:36], raw_config[36:45], raw_config[45:54], raw_config[54:63], raw_config[63:72], raw_config[72:]]

    solver = Solver(raw_config)

    solver.solve()


    grid = []
    for c in solver.puzzle.cells:
        grid.append(c.value)

    for i in range(0, 81, 9):
        print(grid[i:i+3], grid[i+3:i+6], grid[i+6:i+9])
