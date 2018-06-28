from Game import Game
from InputHuman import InputHuman
from InputComputerHardCoded import InputComputerHardCoded
from build_scenarios import build_scenarios

# Build all game scenarios
scenarios = build_scenarios()

# CHOOSE A GAME SCENARIO
# scenario = scenarios['humans'] # All players are Human
scenario = scenarios['humans-unshuffled'] # All players are Human, specific deck order - [8, 7, 6, 5, 5, 4, 4, 3, 3, 2, 2, 1, 1, 1, 1, 1] (8 is out)
# scenario = scenarios['hard_coded'] # all players are hard-coded, same (1) InputMethod object for all inputs
# scenario = scenarios['hard_coded2'] # all players are hard-coded, same (1) InputMethod object for all inputs
# scenario = scenarios['hard_coded3'] # all players are hard-coded, same (1) InputMethod object for all inputs


# Construct the game
game = Game(scenario)

# Run game and get results (winners - list of Player objects)
winners = game.play()


if len(winners) == 1:
    print(f"And the winner is: {winners[0].get_name()}!")
else:
    strs = ", ".join([w.get_name() for w in winners])
    print(f"And the winners are: {strs}!")

print(f"Game record:\n{game.get_game_record()}")