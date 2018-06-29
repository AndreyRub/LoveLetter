from InputMethod        import InputMethod
from PlayLogicHardCoded import PlayLogicHardCoded
from PlayLogicAI        import PlayLogicAI
from PlayLogicHuman     import PlayLogicHuman
from GameScenario       import GameScenario
from Deck               import Deck


def input_human_player(name = "Human"):
    input_method = InputMethod(name=name, play_logic=PlayLogicHuman(name='XXX'), print_request=False)
    return(input_method)

def input_computer_player_quiet(ai_type='random2'):
    computer_player = InputMethod(name=f"Computer - AI ({ai_type})",
                                           play_logic=PlayLogicAI(ai_type=ai_type, seed=2),
                                           print_request=False)
    return(computer_player)

def test_scenario(input_methods_list):
    scenario = GameScenario(
                            title=f"Test scenario - {len(input_methods_list)} players",
                            num_of_players=len(input_methods_list),
                            input_methods_list=input_methods_list,
                            deck_order=[],
                            deck_shuffle_mode = 'random',
                            seed = 0,
                            card_style = 'Classic')
    return(scenario)

def find_order_from_sequence(initial_sequence, new_sequence):
    initial_temp = initial_sequence + [None]
    num_of_elements = len(initial_sequence)
    order = [0]*num_of_elements
    for i in range(num_of_elements):
        order[i] = initial_temp.index(new_sequence[i])
        initial_temp[order[i]]=None
    return order

def build_scenarios():
    # Scenario defaults
    card_style = 'Classic'
    num_of_players = 4
    deck_order = []  # implies a shuffled (random) deck
    shuffle_mode = 'deck_order'

    scenarios = {} # This will be a dictionary of GameScenario objects. Keys are the scenario names


    # # Card deck sequences. Order starts at RIGHT since values are "popped" from the left
    # decks_list = [[8, 7, 6, 5, 5, 4, 4, 3, 3, 2, 2, 1, 1, 1, 1, 1],  # Un-shuffled (8 is out)
    #               [1, 4, 1, 4, 1, 3, 2, 1, 3, 2, 1, 7, 8, 6, 5, 5],  # forces 5+7 on first turn (in 4-player game)
    #               [1, 2, 3, 4, 1, 2, 3, 4, 1, 5, 6, 7, 8, 1, 5, 1],  # nothing special
    #               [1, 5, 7, 1, 1, 1, 8, 2, 4, 4, 3, 1, 6, 2, 3, 5],  # tests the last 5 - should make the opponent lose
    #               ]
    #
    # decks_and_moves_lists = [\
    #                 {'deck': decks_list[0], 'moves': [1, 2, 4, 2, 1, 2, 2, 1, 3, 2, 2, 2, 2, 2, 1, 1, 2, 4, 1, 2, 2]},
    #                 {'deck': decks_list[0], 'moves': [1, 4, 7, 1, 1, 8, 1, 4, 6, 1, 2, 6, 2, 2, 2, 1, 4, 1, 3, 2, 4, 2]},
    #                 {'deck': decks_list[3], 'moves': [1, 2, 1, 2, 2, 2, 1, 2, 1, 3, 2, 3, 8, 1, 4, 8, 1, 3]}
    #                ]
    #
    # # Card sequences are defines by passing a permutation, from "initial sequence" to a specific sequence.
    # # NOTE: this is a really clunky implementation. In order to get the "default" card order, I'm accessing a "private"
    # #       data member of Deck ("cards_"). Might want to re-consider.
    # deck_unshuffled = Deck(shuffle_mode='none') # Do this once to get the un-shuffled deck
    # initial_sequence = [card.get_value() for card in deck_unshuffled.cards_]
    #
    #
    # # Scenario 1 - all players are Human
    #
    # scenarios['humans'] = GameScenario(
    #     title               = 'All players are Human',
    #     num_of_players      = num_of_players,
    #     input_methods_list  = [InputMethod(name="Human", play_logic=PlayLogicHuman(name='XXX'), print_request=False) for k in range(1,num_of_players+1)],
    #     deck_order          = [], # Shuffled
    #     deck_shuffle_mode   = 'random',
    #     seed                = 0,
    #     card_style          = card_style)
    #
    # # Scenario 1 - all players are Human
    #
    # scenarios['humans-unshuffled'] = GameScenario(
    #     title='All players are Human, deck is unshuffled',
    #     num_of_players=num_of_players,
    #     input_methods_list=[InputMethod(name="Human", play_logic=PlayLogicHuman(name='XXX'), print_request=False) for
    #                         k in range(1, num_of_players + 1)],
    #     deck_order=find_order_from_sequence(initial_sequence = initial_sequence,
    #                                         new_sequence = decks_list[3]),
    #     deck_shuffle_mode='deck_order',
    #     seed=0,
    #     card_style=card_style)
    #
    # # Scenario 3 - all players are hard-coded, deck and moves are taken from decks_and_moves_lists:
    # #       input method: ONE OBJECT FOR ALL INPUTS
    #
    # decks_and_moves_lists_index = 0
    # input_computer_hardcoded = InputMethod(name="Computer - HardCoded (same)",
    #                                          play_logic=PlayLogicHardCoded(
    #                                              moves_list=decks_and_moves_lists[decks_and_moves_lists_index]['moves']),
    #                                          print_request=True)
    # scenarios['hard_coded1'] = GameScenario(
    #     title        =
    #         f"""Scenario 3 - all players are hard-coded.
    #         Input method: one object for all inputs.
    #         Deck order - {deck_order}""",
    #     num_of_players      = num_of_players,
    #     input_methods_list  = [input_computer_hardcoded] * num_of_players,
    #     deck_order          = find_order_from_sequence(initial_sequence = initial_sequence,
    #                                                    new_sequence = decks_and_moves_lists[decks_and_moves_lists_index]['deck']),
    #     deck_shuffle_mode   = 'deck_order',
    #     seed                = 0,
    #     card_style          = card_style)
    #
    #
    # # Scenario 4 - AI - random
    # #       input method: ONE OBJECT FOR ALL INPUTS
    #
    # decks_and_moves_lists_index = 0
    # input_computer_AI_random = InputMethod(name="Computer - AI (random)",
    #                                          play_logic=PlayLogicAI(ai_type='random',seed=2),
    #                                          print_request=True)
    # scenarios['AI1'] = GameScenario(
    #     title        =
    #         f"""Scenario 3 - all players are random
    #         Input method: one object for all inputs.
    #         Deck order - {deck_order}""",
    #     num_of_players      = num_of_players,
    #     input_methods_list  = [input_computer_AI_random] * num_of_players,
    #     deck_order          = find_order_from_sequence(initial_sequence = initial_sequence,
    #                                                    new_sequence = decks_and_moves_lists[decks_and_moves_lists_index]['deck']),
    #     deck_shuffle_mode   = 'deck_order',
    #     seed                = 0,
    #     card_style          = card_style)
    #
    # # Scenario 4 - AI - random
    # #       input method: ONE OBJECT FOR ALL INPUTS
    #
    # decks_and_moves_lists_index = 0
    # input_computer_AI_random = InputMethod(name="Computer - AI (random2)",
    #                                          play_logic=PlayLogicAI(ai_type='random2',seed=2),
    #                                          print_request=True)
    # scenarios['AI1_better_guesses'] = GameScenario(
    #     title        =
    #         f"""Scenario 3 - all players are random (ver 2 - better guesses).
    #         Input method: one object for all inputs.
    #         Deck order - {deck_order}""",
    #     num_of_players      = num_of_players,
    #     input_methods_list  = [input_computer_AI_random] * num_of_players,
    #     deck_order          = find_order_from_sequence(initial_sequence = initial_sequence,
    #                                                    new_sequence = decks_and_moves_lists[decks_and_moves_lists_index]['deck']),
    #     deck_shuffle_mode   = 'random',
    #     seed                = 0,
    #     card_style          = card_style)
    #
    #
    # # Scenario 4 - AI - random - quiet (for multiple runs)
    # #       input method: ONE OBJECT FOR ALL INPUTS
    #
    # decks_and_moves_lists_index = 0
    # input_computer_AI_random = InputMethod(name="Computer - AI (random)",
    #                                          play_logic=PlayLogicAI(ai_type='random',seed=2),
    #                                          print_request=False)
    # scenarios['AI1_quiet'] = GameScenario(
    #     title        =
    #         f"""Scenario 3 - all players are hard-coded.
    #         Input method: one object for all inputs.
    #         Deck order - {deck_order}""",
    #     num_of_players      = num_of_players,
    #     input_methods_list  = [input_computer_AI_random] * num_of_players,
    #     deck_order          = find_order_from_sequence(initial_sequence = initial_sequence,
    #                                                    new_sequence = decks_and_moves_lists[decks_and_moves_lists_index]['deck']),
    #     deck_shuffle_mode   = 'deck_order',
    #     seed                = 0,
    #     card_style          = card_style)
    #
    # # Scenario 5 - 1 human vs. 3 AIs
    # #       input method: ONE OBJECT FOR ALL INPUTS
    #
    # decks_and_moves_lists_index = 0
    # input_computer_AI_random = InputMethod(name="Computer - AI (random)",
    #                                          play_logic=PlayLogicAI(ai_type='random',seed=2),
    #                                          print_request=True)
    # input_human = InputMethod(name="Human", play_logic=PlayLogicHuman(name='XXX'), print_request=False)
    # scenarios['human_vs_AI1'] = GameScenario(
    #     title        =
    #         f"""1 Human 3 AIs (random)""",
    #     num_of_players      = num_of_players,
    #     input_methods_list  = [input_human] + [input_computer_AI_random] * (num_of_players-1),
    #     deck_order          = find_order_from_sequence(initial_sequence = initial_sequence,
    #                                                    new_sequence = decks_and_moves_lists[decks_and_moves_lists_index]['deck']),
    #     deck_shuffle_mode   = 'random',
    #     seed                = 14487832,
    #     card_style          = card_style)
    #
    # # Scenario 5 - 1 human vs. 3 AIs
    # #       input method: ONE OBJECT FOR ALL INPUTS
    #
    # decks_and_moves_lists_index = 0
    # input_computer_AI_random = InputMethod(name="Computer - AI (random)",
    #                                          play_logic=PlayLogicAI(ai_type='random',seed=2),
    #                                          print_request=False)
    # input_human = InputMethod(name="Human", play_logic=PlayLogicHuman(name='XXX'), print_request=False)
    # scenarios['human_vs_AI1_quiet'] = GameScenario(
    #     title        =
    #         f"""1 Human 3 AIs (random) - quiet""",
    #     num_of_players      = num_of_players,
    #     input_methods_list  = [input_human] + [input_computer_AI_random] * (num_of_players-1),
    #     deck_order          = find_order_from_sequence(initial_sequence = initial_sequence,
    #                                                    new_sequence = decks_and_moves_lists[decks_and_moves_lists_index]['deck']),
    #     deck_shuffle_mode   = 'random',
    #     seed                = 14487832,
    #     card_style          = card_style)
    #



    # Scenario generator
    hp = [input_human_player(name = 'Human') for k in range(4)]
    cp_ai1 = [input_computer_player_quiet(ai_type='random') for k in range(4)]
    cp_ai2 = [input_computer_player_quiet(ai_type='random2') for k in range(4)]

    scenarios['Humans_only']            = test_scenario(hp)
    scenarios['AI_4_random']            = test_scenario(cp_ai1)
    scenarios['AI_3_random_1_random2']  = test_scenario(cp_ai1[:-1] + [cp_ai2[0]])
    scenarios['AI_4_random2']           = test_scenario(cp_ai2)

    return(scenarios)