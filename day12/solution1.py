#! /usr/bin/python3.8
import csv
from collections import defaultdict
from typing import DefaultDict, List, Set


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def _get_path_count(
        self, adj: DefaultDict[str, List], small_caves: Set[str], cave: str
    ) -> int:
        """Counts # of paths from given `cave` to end using `small_caves`.

        Only counts paths that successfully reach `end` cave.

        Args:
            adj: Adjacency list of caves.
            small_caves: Remaining set of small_caves available to use.
            cave: Current cave to traverse from.

        Returns:
            Count of number of caves originating from current node with
            small_caves available to end, i.e. the number of unique paths from
            cave using small_caves, to end.
        """
        path_count = 0

        for next_cave in adj[cave]:
            next_is_small_cave = next_cave.lower() == next_cave

            if next_cave == "end":
                path_count += 1
            elif next_is_small_cave and next_cave not in small_caves:
                continue
            else:
                if next_is_small_cave:
                    small_caves.remove(next_cave)
                path_count += self._get_path_count(adj, small_caves, next_cave)
                if next_is_small_cave:
                    small_caves.add(next_cave)

        return path_count

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            adj = defaultdict(list)
            small_caves = set()

            for row in csv_reader:
                node1, node2 = row[0].split("-")
                adj[node1].append(node2)
                adj[node2].append(node1)

            for cave in adj:
                if cave[0].lower() == cave[0]:
                    small_caves.add(cave)
            # Remove "start" from remaining caves
            small_caves.remove("start")

            print(self._get_path_count(adj, small_caves, "start"))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
