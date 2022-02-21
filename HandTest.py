import random
from Game import Hand, Display

print('=== Hand Creation Test ===')
arr = random.sample(range(44), 6)
print('Init Hand Array:', arr[:5])
hand = Hand.Hand(arr[:5])
print('Hand Object:', hand)
print('Hand:', Display.serise_to_string(hand.toArray()))

print('\n=== Hand Change Test ===')
draw, discard = arr[5], hand.toArray()[0]
print('Draw Card idx:', draw)
print('Discard Card idx:', discard)
hand.change(draw, discard)
print('Hand Object:', hand)
print('Hand:', Display.serise_to_string(hand.toArray()))