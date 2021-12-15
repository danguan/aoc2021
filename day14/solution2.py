#! /usr/bin/python3.8
import csv
from collections import Counter, defaultdict
from typing import DefaultDict


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.pair_insertions = {}

    def _process_insertions(
        self, template_counts: DefaultDict[str, int]
    ) -> DefaultDict[str, int]:
        """Processes insertions on template_counts and return new counts.

        Args:
            template_counts: Count of pairs of characters in current template
                iteration.

        Returns:
            Counts of all 2-letter pairs in template_counts after making
            appropriate pair insertions for all pairs in template_counts.
        """
        new_template_counts = defaultdict(int)

        for pair_str in template_counts:
            occurrence = template_counts[pair_str]

            if pair_str not in self.pair_insertions:
                new_template_counts[pair_str] += occurrence
            else:
                insertion_char = self.pair_insertions[pair_str]
                new_template_counts[pair_str[0] + insertion_char] += occurrence
                new_template_counts[insertion_char + pair_str[1]] += occurrence

        return new_template_counts

    def _get_common_diff(
        self, template_counts: DefaultDict[str, int], original_template: str
    ) -> int:
        """Finds <most common char count> - <least common char count>.

        Note that each pair in template counts will double-count any chars
        besides the first and last chars.

        Example:
            original_template = "ABCDE"
            template_counts = {
                "AB": 1,
                "BC": 1,
                "CD": 1,
                "DE": 1,
            }
            assert _get_common_diff(template_counts, original_template) == 0

        In above example, B, C, and D will have frequencies of 2 if counting
        all letters in all pairs, while A and E will only have frequencies of
        1. To fix this, we add 1 to the frequencies of the first and last
        chars in original_template, and then divide all frequencies by 2.

        Args:
            template_counts: Count of pairs of characters in current template
                iteration.
            original_template: Template provided in original puzzle input.

        Returns:
            Difference between count of most common character and count of
            least common character.
        """
        char_counts = defaultdict(int)

        for pair in template_counts:
            occurrence = template_counts[pair]
            char_counts[pair[0]] += occurrence
            char_counts[pair[1]] += occurrence

        char_counts[original_template[0]] += 1
        char_counts[original_template[-1]] += 1

        counts = Counter(char_counts).most_common()

        return counts[0][1] // 2 - counts[-1][1] // 2

    def solve(self, steps: int):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            template = ""
            template_counts = defaultdict(int)

            for row in csv_reader:
                if not row:
                    continue
                elif "->" in row[0]:
                    pair, insertion = row[0].split(" -> ")
                    self.pair_insertions[pair] = insertion
                else:
                    template = row[0]

            for c_idx in range(len(template) - 1):
                pair = template[c_idx : c_idx + 2]
                template_counts[pair] += 1

            for _ in range(steps):
                template_counts = self._process_insertions(template_counts)

            print(self._get_common_diff(template_counts, template))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve(40)
