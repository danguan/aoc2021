#! /usr/bin/python3.8
import csv
import json
from typing import Optional, Union


class SnailPair:
    def __init__(
        self,
        left: Union["SnailPair", int],
        right: Union["SnailPair", int],
        parent: Optional["SnailPair"],
        side: int,
    ):
        self.left = left
        self.right = right
        self.parent = parent
        self.side = side

    def __str__(self):
        output = "["
        output += str(self.left)
        output += ", "
        output += str(self.right)
        output += "]"
        return output

    def is_valid_snail_num(self) -> bool:
        """Checks if current snail pair is fully reduced.

        Returns:
            True if current instance of SnailPair is fully reduced, else False.
        """

        def is_valid_pair(pair: SnailPair, depth: int):
            if depth == 5:
                return False

            first = True
            if type(pair.left) is int and pair.left >= 10:
                first = False
            elif type(pair.left) is SnailPair:
                first = is_valid_pair(pair.left, depth + 1)

            second = True
            if type(pair.right) is int and pair.right >= 10:
                second = False
            elif type(pair.right) is SnailPair:
                second = is_valid_pair(pair.right, depth + 1)

            return first and second

        return is_valid_pair(self, 1)

    def _explode_left(self) -> None:
        """Handles adding left int value of exploded pair to relevant parent.

        This will navigate upwards until a parent is found such that the
        current SnailPair is on the right side of the parent, and add the
        current SnailPair's left value to the rightmost int of the parent's
        left side.

        Examples:
            Exploding Pair: [2, 3]
            [1, [[2, 3], 4]] - Navigate to top level and add 2 to 1
            [[5, 6], [[2, 3], 4]] - Navigate to top level and add 2 to 6
        """
        left_node = self

        # Navigate up until reaching root, or finding right side SnailPair
        while left_node.parent and left_node.side == 0:
            left_node = left_node.parent
        # Exploding SnailPair is on left side all the way up
        if not left_node.parent:
            return
        left_node = left_node.parent

        # Parent's left is an int, e.g. [1, [[2, 3], 4]] - 1 is an int
        if type(left_node.left) is int:
            left_node.left += self.left
        # Carry over to rightmost int on left side
        else:
            curr_left_pair = left_node.left

            while type(curr_left_pair.right) is SnailPair:
                curr_left_pair = curr_left_pair.right
            curr_left_pair.right += self.left

    def _explode_right(self) -> None:
        """Handles adding right int value of exploded pair to relevant parent.

        This will navigate upwards until a parent is found such that the
        current SnailPair is on the left side of the parent, and add the
        current SnailPair's right value to the leftmost int of the parent's
        right side.

        Examples:
            Exploding Pair: [1, 2]
            [[[1, 2], 3], 4] - Navigate to 2nd level and add 2 to 3
            [[[1, 2], [5, 6]], 4] - Navigate to 2nd level and add 2 to 5
            [[3, [1, 2]], 4] - Navigate to top level and add 2 to 4
        """
        right_node = self

        # Navigate up until reaching root, or finding left side SnailPair
        while right_node.parent and right_node.side == 1:
            right_node = right_node.parent
        # Exploding SnailPair is on right side all the way up
        if not right_node.parent:
            return
        right_node = right_node.parent

        # Parent's right is an int, e.g. [[[1, 2], 3], 4] - 3 is an int
        if type(right_node.right) is int:
            right_node.right += self.right
        # Carry over to leftmost int on right side
        else:
            curr_right_pair = right_node.right

            while type(curr_right_pair.left) is SnailPair:
                curr_right_pair = curr_right_pair.left
            curr_right_pair.left += self.right

    def _explode(self) -> None:
        """Explodes current SnailPair, while updating all relevant parents.

        Will do the following:
            - Add current SnailPair's values to the relevant parents' side
            values, recursively navigating until finding a valid parent to
            update.
            - For immediate parent, update its left or right value depending
            on side of current SnailPair, to be an int instead of SnailPair.
        """
        self._explode_left()
        self._explode_right()

        if self.side == 0:
            self.parent.left = 0
        else:
            self.parent.right = 0

    def action(self) -> int:
        """Either explodes or splits first SnailPair that is invalid.

        Will attempt to explode first SnailPair with depth >= 5, or if no
        SnailPairs fitting that criteria are found, will instead look to
        split first int value with value >= 10.

        Returns:
            1 if action was taken, else 0.
        """

        def attempt_explode(snail_pair: SnailPair, depth: int):
            if depth >= 5:
                snail_pair._explode()
                return 1
            else:
                if type(snail_pair.left) is SnailPair:
                    if attempt_explode(snail_pair.left, depth + 1):
                        return 1
                if type(snail_pair.right) is SnailPair:
                    if attempt_explode(snail_pair.right, depth + 1):
                        return 1
            return 0

        def attempt_split(snail_pair: SnailPair):
            if type(snail_pair.left) is int and snail_pair.left >= 10:
                lower = snail_pair.left // 2
                snail_pair.left = SnailPair(
                    lower, snail_pair.left - lower, snail_pair, 0
                )
                return 1
            elif type(snail_pair.left) is SnailPair:
                if attempt_split(snail_pair.left):
                    return 1

            if type(snail_pair.right) is int and snail_pair.right >= 10:
                lower = snail_pair.right // 2
                snail_pair.right = SnailPair(
                    lower, snail_pair.right - lower, snail_pair, 1
                )
                return 1
            elif type(snail_pair.right) is SnailPair:
                if attempt_split(snail_pair.right):
                    return 1

        if attempt_explode(self, 1):
            return 1
        return attempt_split(self)

    def magnitude(self) -> int:
        """Returns magnitude of current SnailPair.

        Returns:
            Magnitude of given snail_sum.
        """
        magnitude = 0

        if type(self.left) is int:
            magnitude += 3 * self.left
        elif type(self.left) is SnailPair:
            magnitude += 3 * self.left.magnitude()

        if type(self.right) is int:
            magnitude += 2 * self.right
        elif type(self.right) is SnailPair:
            magnitude += 2 * self.right.magnitude()

        return magnitude


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def _snail_sum(
        self, snail_num_1: SnailPair, snail_num_2: SnailPair
    ) -> SnailPair:
        """Sums input SnailPairs in order they're given.

        Process for summing will continually explode and split new SnailPair
        until it is in a valid format that cannot be reduced any further.

        Args:
            snail_num_1: A valid SnailPair.
            snail_num_2: A valid SnailPair.

        Returns:
            Summed SnailPair as a result of summing the input SnailPair
            together, and performing all necessary explode/split operations.
        """
        snail_sum = SnailPair(-1, -1, None, -1)
        snail_num_1.parent = snail_sum
        snail_num_1.side = 0
        snail_sum.left = snail_num_1
        snail_num_2.parent = snail_sum
        snail_num_2.side = 1
        snail_sum.right = snail_num_2

        actioned = snail_sum.action()

        # Continue until no action is taken, i.e. fully reduced
        while actioned:
            actioned = snail_sum.action()

        return snail_sum

    def _parse_snail_pair(
        self, snail_number, parent: Optional[SnailPair], side: int
    ) -> SnailPair:
        """Creates a SnailPair object from given snail_number nested List.

        Args:
            snail_number: Nested list representation of a SnailPair.
            parent: Parent SnailPair object for current SnailPair.
            side: Side of parent SnailPair that current SnailPair resides on.
                Side of -1 is the root, 0 is left child, 1 is right child.

        Returns:
            SnailPair object representing the input snail_number.
        """
        curr_pair = SnailPair(-1, -1, parent, side)
        curr_pair.left = (
            snail_number[0]
            if type(snail_number[0]) is int
            else self._parse_snail_pair(snail_number[0], curr_pair, 0)
        )
        curr_pair.right = (
            snail_number[1]
            if type(snail_number[1]) is int
            else self._parse_snail_pair(snail_number[1], curr_pair, 1)
        )

        return curr_pair

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            snail_numbers = []

            for row in csv_reader:
                snail_numbers.append(
                    self._parse_snail_pair(json.loads(",".join(row)), None, -1)
                )
                assert snail_numbers[-1].is_valid_snail_num()

            current_sum = snail_numbers[0]

            for snail_number_idx in range(1, len(snail_numbers)):
                current_sum = self._snail_sum(
                    current_sum, snail_numbers[snail_number_idx]
                )

            print(current_sum.magnitude())


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
