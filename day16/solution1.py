#! /usr/bin/python3.8
import csv
from typing import List


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.hex_bin = {
            "0": "0000",
            "1": "0001",
            "2": "0010",
            "3": "0011",
            "4": "0100",
            "5": "0101",
            "6": "0110",
            "7": "0111",
            "8": "1000",
            "9": "1001",
            "A": "1010",
            "B": "1011",
            "C": "1100",
            "D": "1101",
            "E": "1110",
            "F": "1111",
        }

    def _get_decimal(self, s: str, start: int, end: int) -> int:
        """Parses the decimal form of substring s in range [start, end).

        Args:
            s: A valid input string of 0s and 1s.
            start: Starting index from which to start parsing.
            end: Ending index from which to start parsing.

        Returns:
            Decimal form of chars in s on interval [start, end).
        """
        return int(s[start:end], 2)

    def _parse_literal(self, s: str, start: int) -> List[int]:
        """Parses literal packet and returns relevant info.

        Args:
            s: A valid input string of 0s and 1s.
            start: Starting index from which to start parsing.

        Returns:
            List containing:
                - Packet version
                - Packet ID (4)
                - Packet value
                - Index one past the last parsed char
        """
        version = self._get_decimal(s, start, start + 3)
        id = self._get_decimal(s, start + 3, start + 6)
        assert id == 4
        value_bin_str = ""
        value_idx = start + 6

        while s[value_idx] == "1":
            value_bin_str += s[value_idx + 1 : value_idx + 5]
            value_idx += 5

        value_bin_str += s[value_idx + 1 : value_idx + 5]
        value = self._get_decimal(value_bin_str, 0, len(value_bin_str))
        end_idx = value_idx + 5

        return [version, id, value, end_idx]

    def _is_literal(self, s: str, start: int) -> bool:
        """Returns whether packet at s[start] is a literal or not.

        Args:
            s: A valid input string of 0s and 1s.
            start: Starting index from which to start parsing.

        Returns:
            True if packet at start index of s is a literal, or False if it is
            an operator packet.
        """
        id = self._get_decimal(s, start + 3, start + 6)
        return id == 4

    def _parse_operator(self, s: str, start: int) -> List[int]:
        """Parses operator packet and returns relevant info.

        Args:
            s: A valid input string of 0s and 1s.
            start: Starting index from which to start parsing.

        Returns:
            List containing:
                - Summed version with all sub-packets' versions
                - Packet ID (not 4)
                - Index one past the last parsed char
        """
        version = self._get_decimal(s, start, start + 3)
        id = self._get_decimal(s, start + 3, start + 6)
        length_type = self._get_decimal(s, start + 6, start + 7)

        if length_type == 0:
            bit_count = self._get_decimal(s, start + 7, start + 22)
            next_packet_idx = start + 22
            start_packet_idx = start + 22

            while next_packet_idx - start_packet_idx < bit_count:
                if self._is_literal(s, next_packet_idx):
                    (
                        literal_version,
                        _,
                        _,
                        next_packet_idx,
                    ) = self._parse_literal(s, next_packet_idx)
                    version += literal_version
                else:
                    operator_version, _, next_packet_idx = self._parse_operator(
                        s, next_packet_idx
                    )
                    version += operator_version
        else:
            packet_count = self._get_decimal(s, start + 7, start + 18)
            next_packet_idx = start + 18

            for _ in range(packet_count):
                if self._is_literal(s, next_packet_idx):
                    (
                        literal_version,
                        _,
                        _,
                        next_packet_idx,
                    ) = self._parse_literal(s, next_packet_idx)
                    version += literal_version
                else:
                    operator_version, _, next_packet_idx = self._parse_operator(
                        s, next_packet_idx
                    )
                    version += operator_version

        return [version, id, next_packet_idx]

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            input_hex = next(csv_reader)[0]
            input_bin = ""

            for ch in input_hex:
                input_bin += self.hex_bin[ch]

            print(self._parse_operator(input_bin, 0)[0])


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
