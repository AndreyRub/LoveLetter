import math
import random
from Game import Game
from Player import Player
from InputHuman import InputHuman

player1 = InputHuman()
player2 = InputHuman()
players = [player1,player2]
game = Game(players,cards_style = "Classic")
game.play()

