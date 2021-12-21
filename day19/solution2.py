#! /usr/bin/python3.8
import csv
from collections import Counter
from typing import List, Tuple


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.rotations = [
            lambda x, y, z: [x, y, z],
            lambda x, y, z: [y, z, x],
            lambda x, y, z: [z, x, y],
            lambda x, y, z: [-x, z, y],
            lambda x, y, z: [z, y, -x],
            lambda x, y, z: [y, -x, z],
            lambda x, y, z: [x, z, -y],
            lambda x, y, z: [z, -y, x],
            lambda x, y, z: [-y, x, z],
            lambda x, y, z: [x, -z, y],
            lambda x, y, z: [-z, y, x],
            lambda x, y, z: [y, x, -z],
            lambda x, y, z: [-x, -y, z],
            lambda x, y, z: [-y, z, -x],
            lambda x, y, z: [z, -x, -y],
            lambda x, y, z: [-x, y, -z],
            lambda x, y, z: [y, -z, -x],
            lambda x, y, z: [-z, -x, y],
            lambda x, y, z: [x, -y, -z],
            lambda x, y, z: [-y, -z, x],
            lambda x, y, z: [-z, x, -y],
            lambda x, y, z: [-x, -z, -y],
            lambda x, y, z: [-z, -y, -x],
            lambda x, y, z: [-y, -x, -z],
        ]

    def _distance(self, p1: List[int], p2: List[int]) -> List[int]:
        """Calculates total manhattan distance between p1 and p2.

        Args:
            p1: List containing x, y, z coords.
            p2: List containing x, y, z coords.

        Returns:
            Manhattan distance between p2 and p1.
        """
        return sum([abs(p2[0] - p1[0]), abs(p2[1] - p1[1]), abs(p2[2] - p1[2])])

    def _get_rotated_points(
        self, points: List[List[int]]
    ) -> List[List[List[int]]]:
        """Returns rotated input points in all 24 possible 90-degree rotations.

        Original rotation will be included as one of the possible rotations.

        Args:
            points: List containing all lists of x, y, z coords.

        Returns:
            List containing all rotated forms of input list in a 3D plane.
        """
        rotated_points = []

        for rot_func in self.rotations:
            curr_rotated_points = []

            for x, y, z in points:
                curr_rotated_points.append(rot_func(x, y, z))
            rotated_points.append(curr_rotated_points)

        for points in rotated_points:
            yield points

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            scanners = []
            curr_scanner = []

            for row in csv_reader:
                while len(row) == 3:
                    curr_scanner.append([int(num) for num in row])
                    try:
                        row = next(csv_reader)
                    except StopIteration:
                        row = []

                if curr_scanner:
                    scanners.append(curr_scanner)
                    curr_scanner = []

            aligned = scanners[0]
            unaligned = scanners[1:]
            next_unaligned = []
            scanner_locations = [[0, 0, 0]]

            while unaligned:
                for unaligned_scanner_points in unaligned:
                    found = False

                    for rotated_points in self._get_rotated_points(
                        unaligned_scanner_points
                    ):
                        counts = Counter()
                        for u_x, u_y, u_z in rotated_points:
                            for a_x, a_y, a_z in aligned:
                                counts[(a_x - u_x, a_y - u_y, a_z - u_z)] += 1

                        if counts.most_common()[0][1] >= 12:
                            vec_x, vec_y, vec_z = counts.most_common()[0][0]

                            for x, y, z in rotated_points:
                                aligned.append(
                                    [x + vec_x, y + vec_y, z + vec_z]
                                )
                            # All aligned beacons are aligned to [0, 0, 0]
                            scanner_locations.append([vec_x, vec_y, vec_z])
                            found = True
                            break
                    if not found:
                        next_unaligned.append(unaligned_scanner_points)
                unaligned = next_unaligned
                next_unaligned = []

            max_dist = 0

            for scanner_idx in range(len(scanner_locations)):
                scanner = scanner_locations[scanner_idx]
                for other_scanner_idx in range(len(scanner_locations)):
                    if scanner_idx == other_scanner_idx:
                        continue
                    other_scanner = scanner_locations[other_scanner_idx]
                    max_dist = max(
                        max_dist, self._distance(scanner, other_scanner)
                    )
            print(max_dist)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
