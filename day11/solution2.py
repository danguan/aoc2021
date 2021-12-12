#! /usr/bin/python3.8
import csv
from typing import List
from collections import deque


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.directions = (
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1),
        )

    def _process_step(self, board: List[List[int]]) -> bool:
        """Returns whether the entire board has flashed, and update board.

        Args:
            board: Board state of octopi and their current energy levels.

        Returns:
            True if all octopi on the board have flashed, or False otherwise.
        """
        flashes_in_step = 0
        flashed_coords = deque()

        # Create initial state of incremented-step board
        for r in range(len(board)):
            for c in range(len(board[0])):
                board[r][c] += 1
                if board[r][c] == 10:
                    flashed_coords.append((r, c))

        while flashed_coords:
            r, c = flashed_coords.popleft()

            for r_inc, c_inc in self.directions:
                new_r = r + r_inc
                new_c = c + c_inc

                if len(board) > new_r >= 0 and len(board[0]) > new_c >= 0:
                    board[new_r][new_c] += 1
                    if board[new_r][new_c] == 10:
                        flashed_coords.append((new_r, new_c))

            flashes_in_step += 1

        if flashes_in_step == len(board) * len(board[0]):
            return True

        # Clean up flashed octopi
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] >= 10:
                    board[r][c] = 0

        return False

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            step = 0
            all_flashed = False
            board = []

            for row in csv_reader:
                curr_row = []
                for ch in row[0]:
                    curr_row.append(int(ch))
                board.append(curr_row)

            while not all_flashed:
                all_flashed = self._process_step(board)
                step += 1

            print(step)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
