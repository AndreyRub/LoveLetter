from Deck import Deck
from Card import Card
from Player import Player
from RequestInfo import RequestInfo

class Game:
    # Class Game

    # 	properties:
    # 		deck:			current deck
    # 		*valid_moves:	a list with valid moves for current player (e.g. [3,4], or [6]).
    # 						Note: this still allows useless / sacrificing moves (e.g. playing a 1 when all players have a 4, or playing the 8 and losing the round). It only serves to avoid playing 5/6 when having the 7.
    # 		protection:		list of True/False per each player. Set to True if player is currently protected by a 4
    # 		discard_pile:	list of all discarded cards
    # 		players:		list of player object in current game
    # 		player_status:	list of Booleans for each player status in the game: True: active, False: inactive (out of the round)
    # 		winners:		list of winners for current game

    # 	methods:
    # 		init:					init the deck, init all players, give each 1 card. Init discard pile. Input: number of players + names (optional)
    # 		play:					runs the main game loop until a winner is declared. Returns winner index
    # 		draw_card:				draw a card from the deck. Returns False if deck is depleted
    # 		give_player_card: 		draw a card from the deck and add it to a player's hand.
    # 		add_to_discard_pile:  	add a card to the discard pile
    # 		show_discard_pile:		generate a list of how many cards have been discarded so far
    # 		do_player_turn:			remove protection, draw a card and give it to a player, show user both cards + discard pile, ask for input, check validity, run card logic
    # 									Note: if deck is empty, draw_card will return false and decide_winner should be called
    # 		run_card_logic:			run card logic. Make sure to check for protection. E.g. card==1, prompt for non-protected targets and guesses card value. 					If all targets are protected, do nothing. Compare guess to card value. If matched, remove player from the game.
    # 									Also: check if princess was forced to be discarded when running 5's logic
    # 		advance_current_player	advance the current active player index
    #		is_game_over			returns whether the game is over and a winner needs to be decided (either 1 player remaining or deck is empty)
    # 		decide_winner:			returns winner from all remaining players (highest card value wins). Returns a list, in case of a draw

    def default_player_name(index):
        return ("Player " + str(index))

    def get_validity(hand):
        if hand[0].get_value() == 7:
            if hand[1].get_value() in [5, 6]:  # [7,5] or [7,6] requires playing the 7
                return ([True, False])
        if hand[1].get_value() == 7:
            if hand[0].get_value() in [5, 6]:  # [5,7] or [6,7] requires playing the 7
                return ([False, True])
        return ([True, True])

    def get_validity_prompt(hand):
        validity = Game.get_validity(hand)
        if all(validity):
            prompt = f"Note: you may play any card. Your choice: "
        else:
            prompt = f"Note: you may only play card {validity.index(True)+1} (i.e. you must play the 7). Your choice: "
        return prompt

    def __init__(self, players_list, cards_style = "Japanese", shuffle_order=[]):
        # init:			init the deck, init all players, give each 1 card. Input: number of players + names (optional)
        num_of_players = len(players_list)
        if not num_of_players in range(2, 5):
            print("Number of players must be between 2 and 4")
            return (None)

        self.num_of_players = num_of_players

        # Get player names / set them to defaults ("Player 1", "Player 2", etc.)
        self.player_names = [players_list[i].get_name() if players_list[i].get_name() else Game.default_player_name(i+1) for i in range(num_of_players)]

        # Init all players
        self.players = [Player(player_logic, name) for (player_logic, name) in zip(players_list, self.player_names)]
        self.player_active_status = [True] * self.num_of_players
        self.current_player_index = 0
        self.protected = [False] * self.num_of_players
        self.winners = []

        # Init the deck
        self.deck = Deck(cards_style=cards_style,shuffle_order=shuffle_order)

        # Init discard pile
        self.discard_pile = []

        # Give each player a card
        [self.give_player_card(p) for p in self.players]


    def prompt_player_for_input(self, player):
        name = player.get_name()
        hand = player.show_hand()
        card_values = [card.get_value() for card in hand]
        prompt = f"{name}, this is your hand:\n1: Value: {card_values[0]}, {hand[0].get_description()}\n2: Value: {card_values[1]}, {hand[1].get_description()}\nChoose your card to play.\n"
        validity = Game.get_validity(hand)
        validity_prompt = Game.get_validity_prompt(hand)
        full_prompt = prompt + validity_prompt
        request_info = RequestInfo(human_string=full_prompt, action_requested='card')
        while True:
            # selection = input(prompt + validity_prompt)
            selection = player.input_method.get_player_input(request_info)
            if isinstance(selection, int) and selection in [1, 2] and validity[selection - 1]:
                selected_card = player.play_card(int(selection) - 1)
                self.add_to_discard_pile(selected_card)
                return (selected_card)
            request_info.invalid_moves += [selection]
            print('\n*** Invalid value. Try again...\n')


    def draw_card(self):
        # draw_card:		draw a card from the deck. Returns False if deck is depleted
        return self.deck.deal_card()

    def give_player_card(self, player):
        # give_player_card: draw a card from the deck and add it to a player's hand.
        card = self.draw_card()
        return player.add_card(card)

    def add_to_discard_pile(self, card):
        # add_to_discard_pile:  add a card to the discard pile
        self.discard_pile.append(card)

    def show_discard_pile(self):
        # show_discard_pile:	generate a list of how many cards have been discarded so far of each card type

        dp_verbose = dict(self.deck.descriptions, [0] * len(self.deck.descriptions))
        for card in self.discard_pile:
            dp_verbose[card.get_description()] += 1
        print(dp_verbose)
        return (dp_verbose)

    def do_next_player_turn(self):
        # 		do_player_turn:			remove protection, draw a card and give it to a player, show user both cards + discard pile, ask for input, check validity, run card logic
        # 									Note: if deck is empty, draw_card will return false and decide_winner should be called
        print(self.disable_protection(self.current_player_index))

        current_player = self.players[self.current_player_index]
        new_hand = self.give_player_card(
            current_player)  # TODO: len(new_hand) should be equal to 2. Otherwise card is returned. Not tested.
        if not isinstance(new_hand,
                          Card):  # card is returned if player's hand cannot accept a new card. Not supported yet.
            selected_card = self.prompt_player_for_input(current_player)
            return (selected_card)
        return False

    def advance_current_player(self):
        next_index = (self.current_player_index + 1) % self.num_of_players
        while not self.player_active_status[next_index]:
            next_index = (next_index + 1) % self.num_of_players
        self.current_player_index = next_index

    def is_game_over(self):
        if sum(self.player_active_status) == 1:
            return('Game over - 1 player remaining')
        elif self.deck.is_empty():
            card_desc = [(f"{self.players[i].show_hand()[0].get_value()} - " + \
                         f"{self.players[i].show_hand()[0].get_description()}")
                         * self.player_active_status[i] for i in range(self.num_of_players)
                         if self.players[i].show_hand()]
            player_names = [self.players[i].show_name() * self.player_active_status[i] for i in
                           range(self.num_of_players) if self.players[i].show_hand()]
            final_state = [' - '.join([a,b]) for (a,b) in zip(player_names, card_desc)]
            return(f'Game over - deck is depleted. Current active players\' hands:\n'+'\n'.join(final_state))
        return (False)

    def get_opponent_indices(self):
        # These are the displayed indices (start from 1). Used indices start from 0
        opponent_indices = [i for i, x in enumerate(self.player_active_status) if
                            x and (i) != self.current_player_index]
        return(opponent_indices)

    def get_opponent_index(self):
        # get_opponent_index - prompt the user to select an opponent to play the card against, from all currently active players

        opponent_indices = self.get_opponent_indices()
        # Run a quick check for protection - if all opponents are protected, skip the turn
        if all([self.protected[i] for i in opponent_indices]):
            return(-1)

        protection_str = ['', '(Protected)']

        current_player = self.players[self.current_player_index]
        current_player_name = current_player.show_name()
        prompt_str_1 = f"{current_player_name}, select your target:\n"
        prompt_str_2 = '\n'.join([f"{i+1} - {self.players[i].show_name()} {protection_str[self.protected[i]]}" for i in opponent_indices])
        prompt_str = prompt_str_1 + prompt_str_2 + '\n'
        request_info = RequestInfo(human_string=prompt_str, action_requested='opponent')
        while True:

            # index = input(prompt_str_1 + prompt_str_2 + "\n")
            index = current_player.input_method.get_player_input(request_info)

            try:
                val = int(index)
                if val-1 in opponent_indices:
                    if self.protected[val-1]:
                        print("That player is protected. Choose another player")
                        request_info.invalid_moves += [index]
                    else:
                        return (val-1)
            finally:
                pass

    def get_guessed_value(self):
        # Run a quick check for protection - if all opponents are protected, skip the turn
        if all([self.protected[i] for i in self.get_opponent_indices()]):
            return(-1)

        current_player = self.players[self.current_player_index]

        prompt_str_1 = f"Guess the card (2 or higher):\n"
        prompt_str_2 = self.deck.show_descriptions()
        prompt_str = prompt_str_1 + prompt_str_2 + '\n'
        request_info = RequestInfo(human_string=prompt_str, action_requested='guess')

        while True:

            # index = int(input(prompt_str_1 + prompt_str_2 + "\n"))
            index = current_player.input_method.get_player_input(request_info)

            if index in range(2, 9):
                return index

            request_info.invalid_moves += [index]
            print(f"** Incorrect value entered ({index}), try again: **")

    def set_player_lose(self, index):
        # Set a player status to "lose"
        self.player_active_status[index] = False
        if self.players[index].show_hand(): # If player had just played the princess, their hand is empty
            self.add_to_discard_pile(self.players[index].play_card())

        return (f"{self.players[self.current_player_index].show_name()} loses and is out of the game.")

    def run_logic(self, active_player_index, opponent_index, played_card_value, guessed_value=0):
        # Quick check for all-opponents-protected scenario
        if opponent_index==-1:
            return("All opponents protected. Nothing happens")

        # Performs the actual logic behind each played card
        current_player = self.players[active_player_index]
        opponent = self.players[opponent_index]
        current_player_card = current_player.show_hand()[0]
        opponent_card = opponent.show_hand()[0]
        current_player_name = current_player.show_name()
        opponent_name = opponent.show_name()
        current_player_value = current_player_card.get_value()
        opponent_value = opponent_card.get_value()

        if played_card_value == 1:    # Guess
            if opponent_value == guessed_value:
                self.set_player_lose(opponent_index)
                return (f"Correct! {opponent_name} has a card value: {opponent_value}. {opponent_name} loses and is out of the game")
            else:
                return (f"Incorrect! {opponent_name} has a different card value. Nothing happens")


        elif played_card_value == 2:  # Look

            return (f"{opponent_name}'s hand is: {opponent_value} - {opponent_card.get_description()}")

        elif played_card_value == 3:  # Compare

            if current_player_value > opponent_value:
                self.set_player_lose(opponent_index)
                return (f"{current_player_name} (card value: {current_player_value}) wins.\n" +
                        f"{opponent_name} (card value: {opponent_value}) loses and is out of the game")
            elif current_player_value < opponent_value:
                self.set_player_lose(active_player_index)
                return (f"{opponent_name} (card value: {opponent_value}) wins.\n" +
                        f"{current_player_name} (card value: {current_player_value}) loses and is out of the game")
            else:
                return (f"It's a draw! Both players have card value: {opponent_value}. Nothing happens")

        elif played_card_value == 5:  # Discard

            discarded_card = opponent.play_card()
            discarded_card_value = discarded_card.get_value()
            self.add_to_discard_pile(discarded_card)
            if discarded_card_value == 8:
                self.set_player_lose(opponent_index)
                return (f"{opponent_name} discards a Princess and loses this round")
            new_card = self.draw_card()
            opponent.add_card(new_card)
            return (f"{opponent_name} discards a card value of {discarded_card_value} and draws a new card")

        elif played_card_value == 6:  # Trade hands
            current_player.play_card()
            opponent.play_card()
            current_player.add_card(opponent_card)
            opponent.add_card(current_player_card)
            return (f"{current_player_name} and {opponent_name} have traded hands")

    def enable_protection(self, player_index):
        # Set protection to player
        current_player_name = self.players[player_index].show_name()
        self.protected[player_index] = True
        return (f"{current_player_name} is now protected")

    def disable_protection(self, player_index):
        # Remove protection from player
        if self.protected[player_index]:
            current_player_name = self.players[player_index].show_name()
            self.protected[player_index] = False
            return (f"{current_player_name} is no longer protected")
        return ("")

    def run_card_logic(self, selected_card):
        # 		run_card_logic:			run card logic. Make sure to check for protection. E.g. card==1, prompt for non-protected targets and guesses card value.
        # 								If all targets are protected, do nothing. Compare guess to card value. If matched, remove player from the game.
        # 									Also: check if princess was forced to be discarded when running 5's logic

        selection = selected_card.get_value()

        if selection == 8:  # Princess - lose this round

            output_str = self.set_player_lose(self.current_player_index)

        elif selection == 7:  # Sensei - do nothing

            output_str = f"{self.players[self.current_player_index].show_name()} discards a card value of {selected_card.get_description()}. Nothing happens."

        elif selection == 4:

            output_str = self.enable_protection(self.current_player_index)

        elif selection in [2, 3, 5, 6]:  # Look/Compare/Discard/Trade - pick an opponent

            opponent_index = self.get_opponent_index()
            output_str = self.run_logic(self.current_player_index, opponent_index, selection)

        elif selection == 1:  # Guard - pick an opponent and guess their hand

            opponent_index = self.get_opponent_index()
            guessed_value = self.get_guessed_value()
            output_str = self.run_logic(self.current_player_index, opponent_index, selection, guessed_value)

        else:

            output_str = (f"Error - bad value {selection} entered")

        print(output_str)
        return(output_str)

    def decide_winner(self):
        # decide_winner:			returns winner from all remaining players (highest card value wins). Returns a list, in case of a draw

        remaining_players = [ self.players[i] for i in range(self.num_of_players) if self.players[i].show_hand() and self.player_active_status[i] ]
        remaining_card_values = [p.show_hand()[0].get_value() for p in remaining_players]
        winners = [remaining_players[i] for i, x in enumerate(remaining_card_values) if x == max(remaining_card_values)]

        return(winners)

    def play(self):
        # play:					runs the main game loop until a winner is declared. Returns winner index

        game_over = False
        while not game_over:
            selected_card = self.do_next_player_turn()
            self.run_card_logic(selected_card)
            self.advance_current_player()
            game_over = self.is_game_over()


        self.winners = self.decide_winner()
        # return (game_over + '\n' + str(self.winners))
        print(game_over)
        return(self.winners)

