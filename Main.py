from Game import Game
from build_scenarios import build_scenarios

def print_winner(winners):
    if len(winners) == 1:
        str = Game.header_prompt(f"And the winner is: {winners[0][1].get_name()}!")
    else:
        strs = ", ".join([w[1].get_name() for w in winners])
        str = Game.header_prompt(f"And the winners are: {strs}!")
    print(str)


# Build all game scenarios
scenarios = build_scenarios()


# Andrey: choose here

# CHOOSE YOUR SCENARIO (Human vs. 3 computers, or 4 computers against themselves):
# scenario = scenarios['human_vs_3_AI_simple_logic']         # 4 simple_logic AIs
scenario = scenarios['AI_4_simple_logic']         # 4 simple_logic AIs


number_of_games_to_play = 2000

# Run multiple games (with same scenario) using AI and get statistics
wins_count = [0]*scenario.num_of_players
for k in range(number_of_games_to_play):
    winners = Game(scenario).play()
    print_winner(winners)
    for w in winners:
        wins_count[w[0]] += 1

print('Wins count:')
print(list(enumerate([0]+wins_count))[1:])


















# CHOOSE A GAME SCENARIO

# scenario = scenarios['Humans_only']            # All players are Human
# scenario = scenarios['human_vs_3_AI_random2']         # Human vs. 3 Random2 AIs
# scenario = scenarios['AI_4_random']                 # AI player - random selection for AI bot
# scenario = scenarios['AI_3_random_1_random2'] # 3 Random AIs, 1 "Random2" AI
# scenario = scenarios['AI_1_random2_3_random1'] # 3 Random AIs, 1 "Random2" AI
# scenario = scenarios['AI_4_random2']         # 4 Random2 AIs
# scenario = scenarios['AI_4_simple_logic']         # 4 simple_logic AIs
# scenario = scenarios['AI_4_simple_logic_fixed_seed_loud']         # 4 simple_logic AIs
# scenario = scenarios['human_vs_3_AI_simple_logic']         # 4 simple_logic AIs
# scenario = scenarios['human_vs_3_AI_simple_logic_seed']         # 4 simple_logic AIs
# scenario = scenarios['3_AI_simple_logic_vs_human']         # 4 simple_logic AIs
# scenario = scenarios['3_AI_simple_logic_vs_human_seed']         # 4 simple_logic AIs
# scenario = scenarios['hard_coded1']         # Hard coded - need to un-comment from build_scenarios.py

