from InputMethod        import InputMethod
from PlayLogicHardCoded import PlayLogicHardCoded
from PlayLogicHuman     import PlayLogicHuman
from GameScenario       import GameScenario
from Deck               import Deck

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

    # Card deck sequences. Order starts at RIGHT since values are "popped" from the left
    decks_list = [[8, 7, 6, 5, 5, 4, 4, 3, 3, 2, 2, 1, 1, 1, 1, 1],  # Un-shuffled (8 is out)
                  [1, 4, 1, 4, 1, 3, 2, 1, 3, 2, 1, 7, 8, 6, 5, 5],  # forces 5+7 on first turn (in 4-player game)
                  [1, 2, 3, 4, 1, 2, 3, 4, 1, 5, 6, 7, 8, 1, 5, 1],  # nothing special
                  [1, 5, 5, 1, 1, 1, 8, 2, 4, 4, 3, 1, 6, 2, 3, 7],  # nothing special (copied from a human run)
                 ]

    decks_and_moves_lists = [\
                    {'deck': decks_list[0], 'moves': [1, 2, 4, 2, 1, 2, 2, 1, 3, 2, 2, 2, 2, 2, 1, 1, 2, 4, 1, 2, 2]},
                    {'deck': decks_list[0], 'moves': [1, 4, 7, 1, 1, 8, 1, 4, 6, 1, 2, 6, 2, 2, 2, 1, 4, 1, 3, 2, 4, 2]},
                    {'deck': decks_list[3], 'moves': [1, 2, 1, 2, 2, 2, 1, 2, 1, 3, 2, 3, 8, 1, 4, 8, 1, 3]}
                   ]

    # Card sequences are defines by passing a permutation, from "initial sequence" to a specific sequence.
    # NOTE: this is a really clunky implementation. In order to get the "default" card order, I'm accessing a "private"
    #       data member of Deck ("cards_"). Might want to re-consider.
    deck_unshuffled = Deck(shuffle_mode='none') # Do this once to get the un-shuffled deck
    initial_sequence = [card.get_value() for card in deck_unshuffled.cards_]


    scenarios = {} # This will be a dictionary of GameScenario objects. Keys are the scenario names


    # Scenario 1 - all players are Human

    scenarios['humans'] = GameScenario(
        title               = 'All players are Human',
        num_of_players      = num_of_players,
        input_methods_list  = [InputMethod(name="Human", play_logic=PlayLogicHuman(name='XXX'), print_request=False) for k in range(1,num_of_players+1)],
        deck_order          = [], # Shuffled
        deck_shuffle_mode   = 'random',
        seed                = 0,
        card_style          = card_style)

    # Scenario 1 - all players are Human

    scenarios['humans-unshuffled'] = GameScenario(
        title='All players are Human, deck is unshuffled',
        num_of_players=num_of_players,
        input_methods_list=[InputMethod(name="Human", play_logic=PlayLogicHuman(name='XXX'), print_request=False) for
                            k in range(1, num_of_players + 1)],
        deck_order=find_order_from_sequence(initial_sequence = initial_sequence,
                                            new_sequence = decks_and_moves_lists[2]['deck']),
        deck_shuffle_mode='deck_order',
        seed=0,
        card_style=card_style)

    # Scenario 3 - all players are hard-coded, deck and moves are taken from decks_and_moves_lists:
    #       input method: ONE OBJECT FOR ALL INPUTS

    decks_and_moves_lists_index = 0
    input_computer_hardcoded = InputMethod(name="Computer - HardCoded (same)",
                                             play_logic=PlayLogicHardCoded(
                                                 moves_list=decks_and_moves_lists[decks_and_moves_lists_index]['moves']),
                                             print_request=True)
    scenarios['hard_coded1'] = GameScenario(
        title        =
            f"""Scenario 3 - all players are hard-coded.
            Input method: one object for all inputs.
            Deck order - {deck_order}""",
        num_of_players      = num_of_players,
        input_methods_list  = [input_computer_hardcoded] * num_of_players,
        deck_order          = find_order_from_sequence(initial_sequence = initial_sequence,
                                                       new_sequence = decks_and_moves_lists[decks_and_moves_lists_index]['deck']),
        deck_shuffle_mode   = 'deck_order',
        seed                = 0,
        card_style          = card_style)


    return(scenarios)