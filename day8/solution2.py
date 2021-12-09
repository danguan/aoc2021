#! /usr/bin/python3.8
import csv
from typing import Dict


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.number_segments = [
            set(["a", "b", "c", "e", "f", "g"]),
            set(["c", "f"]),  # Unique - 1
            set(["a", "c", "d", "e", "g"]),
            set(["a", "c", "d", "f", "g"]),
            set(["b", "c", "d", "f"]),  # Unique - 4
            set(["a", "b", "d", "f", "g"]),
            set(["a", "b", "d", "e", "f", "g"]),
            set(["a", "c", "f"]),  # Unique - 7
            set(["a", "b", "c", "d", "e", "f", "g"]),  # Unique - 8
            set(["a", "b", "c", "d", "f", "g"]),
        ]
        self.length_number_mapping = {2: 1, 3: 7, 4: 4, 7: 8}

    def _easy_solve(self, right: str) -> int:
        """Identifies 4-digit number if all nums are in [1,4,7,8].

        Args:
            right: A string containing 4 sequences of segments.

        Returns:
            4-digit number if all sequences can be mapped uniquely to a number,
            or -1 if not.
        """
        result = 0

        for sequence in right.split(" "):
            if len(sequence) not in self.length_number_mapping:
                return -1
            result *= 10
            result += self.length_number_mapping[len(sequence)]
        return result

    def _chars_in(self, shorter: str, longer: str) -> int:
        """Counts number of chars from shorter are in longer.

        Args:
            shorter: A valid string.
            longer: A valid string.

        Returns:
            Count of chars in shorter that are in longer.
        """
        count = 0
        longer_set = set(longer)

        for c in shorter:
            if c in longer_set:
                count += 1

        return count

    def _handle_ambiguous(
        self,
        sequence: str,
        mapped_numbers: Dict[int, str],
        mapped_sequences: Dict[str, int],
    ) -> int:
        """Map out which number the given 5-length sequence could correspond to.

        Uses existing mapped sequences/numbers to identify and eliminate
        possibilities for which number the given sequence could correspond to.

        Args:
            sequence: A string sequence corresponding to a number.
            mapped_numbers: Mapping of numbers to their sorted sequence str.
            mapped_sequences: Mapping of sorted sequence strs to their numbers.

        Returns:
            Digit that the given sequence corresponds to, or -1 otherwise.
        """

        possible_sequences = (
            set([2, 3, 5]) if len(sequence) == 5 else set([0, 6, 9])
        )

        found_digit_sequence = (-1, "")

        # Found other 2 possible sequences already
        if (
            len(possible_sequences.intersection(set(mapped_numbers.keys())))
            == 2
        ):
            for digit in possible_sequences:
                if digit not in mapped_numbers:
                    found_digit_sequence = (digit, sequence)
                    break
        elif len(sequence) == 5:
            if 1 in mapped_numbers and self._chars_in(
                mapped_numbers[1], sequence
            ) == len(mapped_numbers[1]):
                found_digit_sequence = (3, sequence)
            elif 7 in mapped_numbers and self._chars_in(
                mapped_numbers[7], sequence
            ) == len(mapped_numbers[7]):
                found_digit_sequence = (3, sequence)
            elif (
                4 in mapped_numbers
                and self._chars_in(mapped_numbers[4], sequence) == 2
            ):
                found_digit_sequence = (2, sequence)
        else:
            if (
                1 in mapped_numbers
                and self._chars_in(mapped_numbers[1], sequence) == 1
            ):
                found_digit_sequence = (6, sequence)
            elif (
                7 in mapped_numbers
                and self._chars_in(mapped_numbers[7], sequence) == 2
            ):
                found_digit_sequence = (6, sequence)
            elif (
                4 in mapped_numbers
                and self._chars_in(mapped_numbers[4], sequence) == 4
            ):
                found_digit_sequence = (9, sequence)
            elif (
                3 in mapped_numbers
                and self._chars_in(mapped_numbers[3], sequence) == 5
            ):
                found_digit_sequence = (9, sequence)
            elif (
                5 in mapped_numbers
                and self._chars_in(mapped_numbers[5], sequence) == 4
            ):
                found_digit_sequence = (0, sequence)

        # Could not determine sequence digit value
        if found_digit_sequence[0] == -1:
            return -1

        mapped_numbers[found_digit_sequence[0]] = "".join(
            sorted(found_digit_sequence[1])
        )
        mapped_sequences[found_digit_sequence[1]] = found_digit_sequence[0]
        return found_digit_sequence[0]

    def _get_right_value(self, left: str, right: str) -> int:
        """Returns value represented by right 4 sequences, in digits.

        Args:
            left: Valid "input" value.
            right: Valid "output" value.

        Returns:
            4-digit value represented by 4 sequences in given right str.
        """
        sequences_to_decode = set()
        right_sequences_to_decode = set()
        mapped_numbers = {}
        mapped_sequences = {}

        for sequence in left.split(" "):
            sequences_to_decode.add("".join(sorted(sequence)))

        for sequence in right.split(" "):
            sequences_to_decode.add("".join(sorted(sequence)))
            right_sequences_to_decode.add("".join(sorted(sequence)))

        # Identify known numbers
        for sequence in sequences_to_decode.copy():
            if len(sequence) in self.length_number_mapping:
                mapped_numbers[
                    self.length_number_mapping[len(sequence)]
                ] = "".join(sorted(sequence))
                mapped_sequences[
                    "".join(sorted(sequence))
                ] = self.length_number_mapping[len(sequence)]
                sequences_to_decode.remove(sequence)
                right_sequences_to_decode.discard(sequence)

        # Iterate through ambiguous numbers until all are decoded
        while sequences_to_decode and right_sequences_to_decode:
            remaining_sequences = sequences_to_decode.copy()

            for sequence in remaining_sequences:
                if (
                    self._handle_ambiguous(
                        sequence, mapped_numbers, mapped_sequences
                    )
                    != -1
                ):
                    sequences_to_decode.remove(sequence)
                    right_sequences_to_decode.discard(sequence)
            if remaining_sequences == sequences_to_decode:
                print("not enough info")
                raise

        result = 0
        for sequence in right.split(" "):
            result *= 10
            result += mapped_sequences["".join(sorted(sequence))]
        return result

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            total = 0

            for row in csv_reader:
                left, right = row[0].split(" | ")
                if self._easy_solve(right) > 0:
                    total += self._easy_solve(right)
                    continue
                total += self._get_right_value(left, right)

            print(total)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
