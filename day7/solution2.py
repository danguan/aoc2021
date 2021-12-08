#! /usr/bin/python3.8
from collections import defaultdict, deque
import csv
import sys


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def _distance(self, num1: int, num2: int) -> int:
        """Computes fuel needed to reach num2 from num1.

        Follows triangle number formula.

        Args:
            num1: A valid horizontal distance (positive integer).
            num2: A valid horizontal distance (positive integer).

        Returns: Fuel needed to reach num2 from num1.
        """
        diff = abs(num2 - num1)

        return (diff * (diff + 1)) // 2

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            input_row = next(csv_reader)

            positions = []

            for num_str in input_row:
                positions.append(int(num_str))
            positions.sort()

            min_guess = (-1, sys.maxsize)
            left_queue = []
            right_deque = deque(positions)

            for guess in range(max(positions)):
                while right_deque and guess > right_deque[0]:
                    left_queue.append(right_deque.popleft())

                left_dist = sum([self._distance(num, guess) for num in left_queue])
                right_dist = sum([self._distance(num, guess) for num in right_deque])

                if left_dist + right_dist < min_guess[1]:
                    min_guess = (guess, left_dist + right_dist)
                else:
                    print(min_guess)
                    return


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
