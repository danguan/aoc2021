#! /usr/bin/python3.8
import csv
from functools import lru_cache
from typing import List


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        # Evenly distributed, 27 total combinations
        self.roll_counts = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

    def _advance(self, player_pos: int, steps: int) -> int:
        """Return new position of player after advancing `steps` spaces.

        Args:
            player_pos: Location of player from 1 to 10.
            steps: Number of steps to advance player position.

        Returns:
            Player position from 1 to 10 after advancing `steps` spaces.
        """
        return ((player_pos - 1 + steps) % 10) + 1

    @lru_cache
    def _recurse(
        self,
        positions: List[int],
        scores: List[int],
        target_score: int,
        curr_universes: int,
        turn: int,
    ):
        """Recursively identifies # of wins per player from current state.

        Current state can be cached, and is defined as a function of current
        player positions, scores, and turn.

        Args:
            positions: List of current positions of p1 and p2 respectively.
            scores: List of current scores of p1 and p2 respectively.
            target_score: Score at which game should conclude.
            curr_universes: Number of universe that will reach current state.
            turn: Current turn of game, determining who will play next.

        Returns:
            Number of universes in which p1 and p2 win respectively.
        """
        p1_pos, p2_pos = positions
        p1_score, p2_score = scores
        p1_wins = 0
        p2_wins = 0

        for roll_total in self.roll_counts:
            roll_count = self.roll_counts[roll_total]

            if turn % 2 == 0:
                new_pos = self._advance(p1_pos, roll_total)
                new_score = p1_score + new_pos

                if new_score >= target_score:
                    p1_wins += curr_universes * roll_count
                else:
                    new_p1_wins, new_p2_wins = self._recurse(
                        (new_pos, p2_pos),
                        (new_score, p2_score),
                        target_score,
                        curr_universes * roll_count,
                        turn + 1,
                    )
                    p1_wins += new_p1_wins
                    p2_wins += new_p2_wins
            else:
                new_pos = self._advance(p2_pos, roll_total)
                new_score = p2_score + new_pos

                if new_score >= target_score:
                    p2_wins += curr_universes * roll_count
                else:
                    new_p1_wins, new_p2_wins = self._recurse(
                        (p1_pos, new_pos),
                        (p1_score, new_score),
                        target_score,
                        curr_universes * roll_count,
                        turn + 1,
                    )
                    p1_wins += new_p1_wins
                    p2_wins += new_p2_wins

        return p1_wins, p2_wins

    def solve(self, target_score: int):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            positions = []
            for row in csv_reader:
                positions.append(int(row[0][-1]))

            p1_wins, p2_wins = self._recurse(
                tuple(positions), (0, 0), target_score, 1, 0
            )
            print(p1_wins, p2_wins)
            print(max(p1_wins, p2_wins))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve(21)
