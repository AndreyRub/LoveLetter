from Game import Game
from build_scenarios import build_scenarios

# Build all game scenarios
scenarios = build_scenarios()

# CHOOSE A GAME SCENARIO

# scenario = scenarios['Humans_only']            # All players are Human
# scenario = scenarios['human_vs_3_AI_random2']         # Human vs. 3 Random2 AIs
# scenario = scenarios['AI_4_random']                 # AI player - random selection for AI bot
# scenario = scenarios['AI_3_random_1_random2'] # 3 Random AIs, 1 "Random2" AI
# scenario = scenarios['AI_1_random2_3_random1'] # 3 Random AIs, 1 "Random2" AI
# scenario = scenarios['AI_4_random2']         # 4 Random2 AIs
# scenario = scenarios['AI_4_simple_logic']         # 4 simple_logic AIs
scenario = scenarios['human_vs_3_AI_simple_logic']         ## Human vs. 3 simple_logic AIs
# scenario = scenarios['hard_coded1']         # Hard coded - need to un-comment from build_scenarios.py



def print_winner(winners):

    if len(winners) == 1:
        str = Game.header_prompt(f"And the winner is: {winners[0].get_name()}!")
    else:
        strs = ", ".join([w.get_name() for w in winners])
        str = Game.header_prompt(f"And the winners are: {strs}!")

    print(str)

# # Construct the game
# game = Game(scenario)
#
# # Run a single game and get results (winners - list of Player objects)
# winners, winners_idx = game.play()
#
# if len(winners) == 1:
#     str = Game.header_prompt(f"And the winner is: {winners[0].get_name()}!")
# else:
#     strs = ", ".join([w.get_name() for w in winners])
#     str = Game.header_prompt(f"And the winners are: {strs}!")
#
# print(str)
#
# print(f"Game record:\n{game.get_game_record()}")






# Run multiple games (with same scenario) using AI and get statistics
wins_count = [0]*scenario.num_of_players
for k in range(3000):
    winners, winners_idx = Game(scenario).play()
    print_winner(winners)
    for w in winners_idx:
        wins_count[w] += 1

print('Wins count:')
print(list(enumerate([0]+wins_count))[1:])