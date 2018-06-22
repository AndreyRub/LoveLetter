import math
import random
from Player import Player

cards = [1,1,1,1,1,2,2,3,3,4,4,5,6,7,8,9]
draw_pile = list(cards)
random.shuffle(draw_pile)
discard_pile = list()

#Discard one card (to avoid exact guessing)
discard_pile.append( draw_pile.pop())

#Give each player a starting card
players = [Player(1),Player(2)]
for player in players:
    player.get_first_card(draw_pile.pop())

#Play until there are no more cards or only one player stays
is_game_over = False
while not is_game_over:
    for player in players:
        drawn_card = draw_pile.pop()
        played_card = player.play(drawn_card)
        discard_pile.append(played_card)
        print("Player %d played %d" % (player.name,played_card))

    if not draw_pile:
        is_game_over = True