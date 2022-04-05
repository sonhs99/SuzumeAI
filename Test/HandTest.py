from Game import Hand, Display
import unittest

class HandTest(unittest.TestCase):
    def setUp(self):
        self.test_list = [
            # No Point
            (([0, 1, 2, 4, 5], 20), 0),         # 1 1 1 2g2g, 5
            (([0, 1, 2, 32, 36], 40), 0),       # 1 1 1 9 R , G

            # Simple
            (([0, 1, 2, 4, 5], 6), 4),          # 1 1 1 2g2g, 2g
            (([0, 1, 3, 4, 5], 7), 6),          # 1 1 1r2g2g, 2r
            (([0, 4, 8, 16, 17], 18), 3),       # 1 2g3g5 5 , 5
            (([0, 1, 4, 5, 8], 9), 4),          # 1 1 2g2g3g, 3g
            (([0, 4, 5, 8, 9], 12), 2),         # 1 2g2g3g3g, 4g
            (([0, 4, 5, 6, 7], 8), 4),          # 1 2g2g2g2r, 3g
            (([4, 8, 12, 20, 22], 23), 5),      # 2g3g4g5 5 , 5r

            # Complex
            (([0, 1, 3, 36, 37], 39), 19),      # 1 1 1rR R , R
            (([36, 37, 39, 40, 41], 43), 19),   # R R R G G , G
            (([3, 7, 11, 15, 19], 23), 22),     # 1r2r3r4r5r, 6r
            (([4, 5, 8, 9, 12], 14), 12),       # 2g2g3g3g4g, 4g
            (([4, 7, 8, 9, 12], 14), 4),        # 2g2r3g3g4g, 4g
        ]

    def test_point_count(self):
        for (hand_arr, draw), point in self.test_list:
            with self.subTest(
                f'{Display.serise_to_string(hand_arr)}, {Display.card_to_string(draw)}\x1b[0m'):
                self.assertEqual(Hand.Hand(hand_arr).point(draw, 43), point)