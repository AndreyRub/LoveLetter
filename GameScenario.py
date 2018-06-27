from InputHuman import InputHuman

class GameScenario:
    # Simply a container for the game scenario.
    # Specifies the:
    #  title - name of the scenario
    #  input_methods_list (instances of InputMethodInterface)
    #  deck_order - manual order of the deck used in the game. If [], will be shuffled using seed
    #  seed - seed value for random shuffle. if [], seed will not be used and a "true random" shuffle will be done
    #  card_style - determines card description. Can be: ["Japanese", "Batman", "Classic", "Coup"].

    def __init__(self,
                 title = 'Game scenario',
                 num_of_players = 4,
                 input_methods_list = [InputHuman(f'Player {k+1}') for k in range(1,5)],
                 deck_order = [],
                 deck_shuffle_mode='shuffle',
                 seed = [],
                 card_style = "Classic"
                 ):

        self.title = title
        self.num_of_players = num_of_players
        self.input_methods_list = input_methods_list
        self.deck_order = deck_order
        self.deck_shuffle_mode = deck_shuffle_mode
        self.seed = seed
        self.card_style = card_style

        # Inferred values (e.g. num_of_players

    def get_title(self):
        return self.title

    def get_num_of_players(self):
        return self.num_of_players

    def get_input_methods_list(self):
        return self.input_methods_list

    def get_deck_order(self):
        return self.deck_order

    def get_deck_shuffle_mode(self):
        return self.deck_shuffle_mode

    def get_seed(self):
        return self.seed

    def get_card_style(self):
        return self.card_style