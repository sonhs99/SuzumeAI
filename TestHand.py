from Game import Hand, Display

test_list = [
    # No Point
    ([0, 1, 2, 4, 5], 20),
    ([0, 1, 2, 32, 36], 40),

    # Simple
    ([0, 1, 2, 4, 5], 6),
    ([0, 1, 3, 4, 5], 7),
    ([0, 4, 8, 16, 17], 18),
    ([0, 1, 4, 5, 8], 9),
    ([0, 4, 5, 8, 9], 12),
    ([4, 8, 12, 20, 22], 23),

    # Complex
    ([0, 1, 3, 36, 37], 39),
    ([3, 7, 11, 15, 19], 23),
    ([4, 5, 8, 9, 12], 14),
]

for hand_arr, draw in test_list:
    print('Hand:', Display.serise_to_string(hand_arr))
    print('Draw:', Display.card_to_string(draw), '\x1b[0m')
    print('Point:', Hand.Hand(hand_arr).point(draw, 43))
    print()