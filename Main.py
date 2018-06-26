import math
import random
from Game import Game
from Player import Player
from InputHuman import InputHuman

player1 = Player(InputHuman(),"Player1")
player2 = Player(InputHuman(),"Player2")
players = [player1,player2]
game = Game(players,cards_style = "Classic")
game.play()

