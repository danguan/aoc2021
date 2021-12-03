#! /usr/bin/python3.8
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            horiz = 0
            depth = 0
            aim = 0

            for row in csv_reader:
                direction, size = row[0].split(" ")
                size = int(size)

                if direction == "forward":
                    horiz += size
                    depth += aim * size
                elif direction == "down":
                    aim += size
                else:
                    aim -= size
        print(horiz * depth)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
