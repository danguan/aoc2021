#! /usr/bin/python3.8
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self, bin_size: int):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            bit_counts = [0 for _ in range(bin_size)]

            for row in csv_reader:
                for idx, bit_ch in enumerate(row[0]):
                    if bit_ch == "1":
                        bit_counts[idx] += 1
                    else:
                        bit_counts[idx] -= 1
            gamma = 0
            epsilon = 0

            for count in bit_counts:
                gamma <<= 1
                epsilon <<= 1
                if count > 0:
                    gamma += 1
                else:
                    epsilon += 1

            print(gamma * epsilon)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve(12)
