#! /usr/bin/python3.8
import csv
from typing import Set, Tuple


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def _handle_fold(
        self, dots: Set[Tuple[int, int]], xy: str, pos: int
    ) -> Set[Tuple[int, int]]:
        """Returns set of dots as if folded to the left or up based on xy/pos.

        Args:
            dots: Set of dots, which comprise of (col, row) pairs.
            xy: Either "x" or "y", determining whether fold should be vertical
                or horizontal.
            pos: Position of fold line.

        Returns:
            New set of dots, post-fold (omitting duplicates by nature of set).
        """
        new_dots = set()

        for col, row in dots:
            if xy == "y" and row > pos:
                new_dots.add((col, pos - (row - pos)))
            elif xy == "x" and col > pos:
                new_dots.add((pos - (col - pos), row))
            else:
                new_dots.add((col, row))

        return new_dots

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            dots: Set[Tuple[int, int]] = set()  # List of (col, row) pairs
            folds = []

            for row in csv_reader:
                if not row:
                    continue
                elif len(row) == 2:
                    dots.add((int(row[0]), int(row[1])))
                elif "=" in row[0]:
                    xy, pos = row[0].split("=")
                    xy = xy[-1]

                    folds.append([xy, int(pos)])

            for xy, pos in folds[:1]:
                dots = self._handle_fold(dots, xy, pos)

            print(len(dots))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
