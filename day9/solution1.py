#! /usr/bin/python3.8
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.directions = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            risk_level = 0
            caves = []

            for row in csv_reader:
                curr_row = [int(num) for num in row[0]]
                caves.append(curr_row)

            for r in range(len(caves)):
                for c in range(len(caves[r])):
                    low_point = True
                    height = caves[r][c]

                    for d in self.directions:
                        new_r = r + d[0]
                        new_c = c + d[1]

                        if (
                            len(caves) > new_r >= 0
                            and len(caves[r]) > new_c >= 0
                        ):
                            if caves[new_r][new_c] <= height:
                                low_point = False
                                break
                    if low_point:
                        risk_level += height + 1
            print(risk_level)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
