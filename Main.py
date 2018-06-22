import math
import random
import Player

cards = [1,1,1,1,1,2,2,3,3,4,4,5,6,7,8,9]
draw_pile = random.shuffle( list(cards))
discard_pile = list()

player1 = Player(draw_pile.pop())
player2 = Player(draw_pile.pop())

is_game_over = False
while not is_game_over:
    drawn_card = draw_pile.pop()