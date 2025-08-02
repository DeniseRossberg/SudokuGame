import random
import numpy as np


class Sudoku:

    @staticmethod
    def _is_solved(sudoku):
        for i in range(9):
            if sudoku[i].sum() < 45:
                return False
        return True

    @staticmethod
    def _next_free(sudoku):
        for i in range(9):
            for j in range(9):
                if sudoku[i][j] == 0:
                    return i, j
        return -1, -1

    @staticmethod
    def _is_valid(sudoku, row, col, num):
        if num in sudoku[row]:
            return False
        if num in sudoku[:, col]:
            return False

        r = row - (row % 3)
        c = col - (col % 3)
        if num in sudoku[r:r + 3, c:c + 3]:
            return False
        return True

    @staticmethod
    def _generate_solution(sudoku):
        if Sudoku._is_solved(sudoku):
            return True
        row, col = Sudoku._next_free(sudoku)
        nums = list(range(1, 10))
        random.shuffle(nums)

        for num in nums:
            if Sudoku._is_valid(sudoku, row, col, num):
                sudoku[row][col] = num
                solved = Sudoku._generate_solution(sudoku)
                if solved:
                    return True
                sudoku[row][col] = 0
        return False

    @staticmethod
    def _count_solutions(sudoku, count=0):
        if count > 1:
            return count

        row, col = Sudoku._next_free(sudoku)
        if row == -1:
            return count + 1

        for num in range(1, 10):
            if Sudoku._is_valid(sudoku, row, col, num):
                sudoku[row][col] = num
                count = Sudoku._count_solutions(sudoku, count)
                sudoku[row][col] = 0

        return count

    @staticmethod
    def _generate_puzzle(sudoku, holes):
        puzzle = np.copy(sudoku)
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)

        removed = 0
        for row, col in positions:
            if removed >= holes:
                break

            backup = puzzle[row][col]
            puzzle[row][col] = 0

            temp = np.copy(puzzle)
            if Sudoku._count_solutions(temp) == 1:
                removed += 1
            else:
                puzzle[row][col] = backup

        return puzzle

    @staticmethod
    def get_sudoku(difficulty):
        solution = np.zeros(shape=(9, 9), dtype=int)
        Sudoku._generate_solution(solution)

        if difficulty == "easy":
            puzzle = Sudoku._generate_puzzle(solution, 30)
        elif difficulty == "medium":
            puzzle = Sudoku._generate_puzzle(solution, 40)
        else:
            puzzle = Sudoku._generate_puzzle(solution, 50)

        return puzzle, solution