#! /usr/bin/python3.8
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.score_table = {")": 3, "]": 57, "}": 1197, ">": 25137}
        self.closings = {"(": ")", "[": "]", "{": "}", "<": ">"}

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            score = 0

            for row in csv_reader:
                st = []

                for ch in row[0]:
                    if ch in self.closings:
                        st.append(ch)
                    elif st and self.closings[st[-1]] == ch:
                        st.pop()
                    else:
                        score += self.score_table[ch]
                        break
            print(score)

if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
