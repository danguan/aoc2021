#! /usr/bin/python3.8
import csv
from collections import Counter


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.pair_insertions = {}

    def _process_insertions(self, template: str) -> str:
        """Processes insertions on current template and returns new template.

        Args:
            template: String of characters.

        Returns:
            New form of template inserting in characters simultaneously for
            all characters in given template using `self.pair_insertions`.
        """
        new_template = template[0]

        for c_idx in range(len(template) - 1):
            pair = template[c_idx : c_idx + 2]
            if pair in self.pair_insertions:
                new_template += self.pair_insertions[pair]
            new_template += pair[1]

        return new_template

    def _get_common_diff(self, template: str) -> int:
        """Finds <most common char count> - <least common char count>.

        Args:
            template: String of characters.

        Returns:
            Difference between count of most common character and count of
            least common character.
        """
        counts = Counter(template).most_common()

        return counts[0][1] - counts[-1][1]

    def solve(self, steps: int):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            template = ""

            for row in csv_reader:
                if not row:
                    continue
                elif "->" in row[0]:
                    pair, insertion = row[0].split(" -> ")
                    self.pair_insertions[pair] = insertion
                else:
                    template = row[0]

            for _ in range(steps):
                template = self._process_insertions(template)

            print(self._get_common_diff(template))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve(10)
