#! /usr/bin/python3.8
import csv
from typing import List, Tuple


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def _populateNextLists(
        self,
        search_list: List[str],
        bit_idx: int,
        next_list_zeroes: List[str],
        next_list_ones: List[str],
    ) -> Tuple[List[str], List[str]]:
        """Returns populated next lists based on if bit at bit_idx is 0 or 1.

        Returns:
            Copies of next_list_zeroes and next_list_ones populated with bit
            strings corresponding to whether the bit at bit_idx is 0 or 1.
        """
        next_list_zeroes_copy = next_list_zeroes.copy()
        next_list_ones_copy = next_list_ones.copy()

        for bit_str in search_list:
            if bit_str[bit_idx] == "0":
                next_list_zeroes_copy.append(bit_str)
            else:
                next_list_ones_copy.append(bit_str)

        return next_list_zeroes_copy, next_list_ones_copy

    def _getOxygenRating(self, search_list: List[str]) -> int:
        """Repeatedly reduce size of pool by keeping most common first bit.

        Returns:
            "Oxygen Generator Rating".
        """
        next_list_zeroes = []
        next_list_ones = []
        bit_idx = 0

        while len(search_list) > 1:
            next_list_zeroes, next_list_ones = self._populateNextLists(
                search_list, bit_idx, next_list_zeroes, next_list_ones
            )

            if len(next_list_ones) >= len(next_list_zeroes):
                search_list = next_list_ones
            else:
                search_list = next_list_zeroes

            next_list_ones, next_list_zeroes = [], []
            bit_idx += 1

        return int(search_list[0], 2)

    def _getCO2Rating(self, search_list: List[str]) -> int:
        """Repeatedly reduce size of pool by keeping least common first bit.

        Returns:
            "CO2 Scrubber Rating".
        """
        next_list_zeroes = []
        next_list_ones = []
        bit_idx = 0

        while len(search_list) > 1:
            next_list_zeroes, next_list_ones = self._populateNextLists(
                search_list, bit_idx, next_list_zeroes, next_list_ones
            )

            if len(next_list_ones) < len(next_list_zeroes):
                search_list = next_list_ones
            else:
                search_list = next_list_zeroes

            next_list_ones, next_list_zeroes = [], []
            bit_idx += 1

        return int(search_list[0], 2)

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            search_list = []

            for row in csv_reader:
                search_list.append(row[0])
        print(
            self._getOxygenRating(search_list.copy())
            * self._getCO2Rating(search_list.copy())
        )


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
