#! /usr/bin/python3.8
import csv
from typing import List, Tuple


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def _parseValidRow(self, bingo_row: str) -> List[int]:
        """Parses valid input bingo row string into its respective ints.

        Args:
            Valid input bingo row string.

        Returns:
            List of ints represented by input bingo_row string.
        """
        return [int(num) for num in bingo_row.split(" ") if num != ""]

    def _checkWon(self, board: List[List[int]], r: int, c: int) -> bool:
        """Identifies whether current board wins if board[r][c] is picked.

        Args:
            board: Valid running state of a bingo board (can contain neg vals).
            r: Row of number selected on board.
            c: Col of number selected on board.

        Returns:
            True if a row or col has been marked (all negative) or False
            otherwise.
        """
        won = True
        for idx in range(len(board[r])):
            if board[r][idx] >= 0:
                won = False

        if won:
            return True

        won = True

        for idx in range(len(board)):
            if board[idx][c] >= 0:
                won = False

        return won

    def _markBoard(self, board: List[List[int]], num: int) -> Tuple[int, int]:
        """Marks input board if num is found by setting value to -1.

        Args:
            board: Valid running state of a bingo board (can contain neg vals).
            num: Number to mark on bingo board. May not be present.

        Returns:
            Coordinate of marked number if found, else (-1, -1).
        """
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] == num:
                    board[r][c] = -1
                    return (r, c)
        return (-1, -1)

    def _getScore(self, board: List[List[int]]) -> int:
        """Returns sum of un-marked numbers of board.

        Args:
            board: Valid running state of a bigno board (can contain neg vals).

        Returns:
            Sum of non-marked numbers on given board.
        """
        total = 0
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] >= 0:
                    total += board[r][c]

        return total

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            bingo_nums = [int(num) for num in next(csv_reader)]
            bingo_boards = []
            curr_board = []

            for row in csv_reader:
                if not row:
                    continue
                curr_board.append(self._parseValidRow(row[0]))

                if len(curr_board) == 5:
                    bingo_boards.append(curr_board)
                    curr_board = []

            for num in bingo_nums:
                for board in bingo_boards:
                    r, c = self._markBoard(board, num)

                    if r >= 0 and self._checkWon(board, r, c):
                        print(self._getScore(board) * num)
                        return


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
