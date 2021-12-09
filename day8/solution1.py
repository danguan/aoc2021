#! /usr/bin/python3.8
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            count = 0

            for row in csv_reader:
                _, right = row[0].split(" | ")

                for sequence in right.split(" "):
                    if len(sequence) in [2, 3, 4, 7]:
                        count += 1

            print(count)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
