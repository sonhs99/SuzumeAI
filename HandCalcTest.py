from Game import Hand, Display

print('=== Hand Creation Test ===')
arr1 = [0, 1, 4, 5, 8]
arr2 = [7, 8, 9, 10, 11]
print('Init Hand1 Array :', arr1)
print('Init Hand2 Array :', arr2)
hand1 = Hand.Hand(arr1)
hand2 = Hand.Hand(arr2)
print('Hand Object :', hand1, hand2)
print('Hand :',
    Display.serise_to_string(hand1.toArray()),
    Display.serise_to_string(hand2.toArray()))

print('\n=== Hand1 Calculation Test ===')
draw = 9
dora = 0
print('Draw Card idx :', draw)
print('Dora :', dora)
print('Hand :',
    Display.serise_to_string(hand1.toArray()) + ' '
    + Display.card_to_string(draw) + '\x1b[0m')
print('Score :', hand1.point(draw, dora))

print('\n=== Hand2 Calculation Test ===')
draw = 12
print('Draw Card idx :', draw)
print('Hand :',
    Display.serise_to_string(hand2.toArray()) + ' '
    + Display.card_to_string(draw) + '\x1b[0m')
print('Score :', hand2.point(draw, dora))