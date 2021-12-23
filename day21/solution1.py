#! /usr/bin/python3.8
import csv
from typing import List


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def _advance(self, player_pos: int, steps: int) -> int:
        """Return new position of player after advancing `steps` spaces.

        Args:
            player_pos: Location of player from 1 to 10.
            steps: Number of steps to advance player position.

        Returns:
            Player position from 1 to 10 after advancing `steps` spaces.
        """
        return ((player_pos - 1 + steps) % 10) + 1

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            positions = []
            scores = [0, 0]
            turn = 0
            curr_dice_value = 0

            for row in csv_reader:
                positions.append(int(row[0][-1]))

            while max(scores) < 1000:
                player = turn % 2
                steps = 0
                for _ in range(3):
                    curr_dice_value += 1
                    steps += curr_dice_value

                new_pos = self._advance(positions[player], steps)
                positions[player] = new_pos
                scores[player] += new_pos
                turn += 1

            print(turn * 3 * min(scores))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
