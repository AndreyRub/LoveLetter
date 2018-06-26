from InputHuman import InputHuman

from Game import Game
from InputHuman import InputHuman
num_of_players = 4

human_players = [InputHuman("Player " + str(k)) for k in range(1,num_of_players+1)]

# Set all players as Human
players_list = [k for k in human_players]

game = Game(players_list)
winners = game.play()
if len(winners) == 1:
    print(f"And the winner is: {winners[0].show_name()}!")
else:
    strs = ", ".join([w.get_name() for w in winners])
    print(f"And the winners are: {strs}!")
