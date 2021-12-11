#! /usr/bin/python3.8
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.score_table = {")": 1, "]": 2, "}": 3, ">": 4}
        self.closings = {"(": ")", "[": "]", "{": "}", "<": ">"}

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            scores = []

            for row in csv_reader:
                score = 0
                st = []
                corrupted = False

                for ch in row[0]:
                    if ch in self.closings:
                        st.append(ch)
                    elif st and self.closings[st[-1]] == ch:
                        st.pop()
                    else:
                        corrupted = True
                        break
                if corrupted:
                    continue

                while st:
                    closing = self.closings[st.pop()]
                    score *= 5
                    score += self.score_table[closing]
                scores.append(score)
            scores.sort()
            print(scores[len(scores) // 2])

if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
