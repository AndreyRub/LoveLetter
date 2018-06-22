import math
import random
from Player import Player

cards = [1,1,1,1,1,2,2,3,3,4,4,5,6,7,8,9]
draw_pile = list(cards)
random.shuffle(draw_pile)
discard_pile = list()

player1 = Player()
player2 = Player()
#players = [player1,player2]
player1.get_first_card(draw_pile.pop())
player2.get_first_card(draw_pile.pop())

is_game_over = False
while not is_game_over:
    drawn_card = draw_pile.pop()
    played_card_1 = player1.play(drawn_card)
    discard_pile.append(played_card_1)
    print("Player 1 played %d" % played_card_1)

    played_card_2 = player2.play(drawn_card)
    discard_pile.append(played_card_2)
    print("Player 2 played %d" % played_card_1)

    if not draw_pile:
        is_game_over = True