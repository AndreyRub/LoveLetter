from Deck import Deck
from Card import Card
from Player import Player
from RequestInfo import RequestInfo
import random
import play_logic_infra
from time import time

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
            prompt = f"Note: you may only play card {validity.index(True)+1} (i.e. you must play the {hand[validity.index(True)].get_value()}. Your choice: "
        return prompt

    def header_prompt(str):
        stars = "*" * len(str) + "\n"
        return("\n" + stars + str + "\n" + stars + "\n")

    def __init__(self, scenario, print_moves=False):

        # Load data from scenario
        input_methods_list  = scenario.get_input_methods_list()
        cards_style         = scenario.get_card_style()
        deck_order          = scenario.get_deck_order()
        shuffle_mode        = scenario.get_deck_shuffle_mode()
        num_of_players = scenario.get_num_of_players()

        if not num_of_players in range(2, 5):
            print("Number of players must be between 2 and 4")
            return (None)

        # init:			init the deck, init all players, give each 1 card. Input: number of players + names (optional)

        # Set whether to print out each player's chosen move and its effect.
        # Note: this can also be printed from each player's InputMethod object,
        #       through its play_logic property (especially for the PlayLogicHuman object)
        self.print_moves = print_moves

        # Set number of players
        self.num_of_players = num_of_players

        # Get player names / set them to defaults ("Player 1", "Player 2", etc.)
        self.player_names = [f"{Game.default_player_name(i + 1)} ({input_methods_list[i].get_name()})" for i in range(num_of_players)]

        # Init all players
        self.players                = [Player(player_logic, name) for (player_logic, name) in zip(input_methods_list, self.player_names)]
        self.player_active_status   = [True] * self.num_of_players
        self.current_player_index   = 0
        self.protected              = [False] * self.num_of_players
        self.winners                = []

        # Init current turn number (start at 1)
        self.current_turn_number = 1

        # Init game record
        self.game_record = [] # List of dicts of (turn, player, move, description)

        # Input a random seed (system-time based) to the random module. Can be overridden later with a different seed value
        random.seed(time())

        # Init the deck
        self.deck = Deck(cards_style=cards_style,deck_order=deck_order,shuffle_mode=shuffle_mode, seed=scenario.get_seed())
        self.deck_for_debug = [c.get_value() for c in self.deck.cards_]

        # Init discard pile
        self.discard_pile = []
        dp_list, dp_verbose = self.show_discard_pile()

        # Give each player a card
        [self.give_player_card(p) for p in self.players]

        # Update each player's input_method's state with the new discard_pile information
        for player_idx in range(len(self.players)):
            self.players[player_idx].input_method.play_logic.init_hand_options(self.players[player_idx].get_hand(),dp_list)



    def prompt_player_for_input(self, player):
        name = player.get_name()
        hand = player.get_hand()
        new_line = '\n'
        card_values = [card.get_value() for card in hand]
        dp_list, dp_verbose = self.show_discard_pile()
        prompt = Game.header_prompt(f"Turn #{self.current_turn_number}, {name}\'s turn:") + \
                                 f"{name}, this is your hand:" + new_line + new_line + \
                                 f"1: Value: {card_values[0]}, {hand[0].get_description()}" + new_line + \
                                 f"2: Value: {card_values[1]}, {hand[1].get_description()}" + new_line + new_line + \
                                 f"d: Show discard pile" + new_line + new_line + \
                                 f"Choose your card to play.\n"
        validity = Game.get_validity(hand)
        validity_prompt = Game.get_validity_prompt(hand)
        valid_moves = [i+1 for (i,x) in enumerate(validity) if x]
        players_active = self.player_active_status
        players_protected = self.protected
        full_prompt = prompt + validity_prompt
        request_info = RequestInfo(human_string=full_prompt,
                                   action_requested='card',
                                   discard_pile=dp_list,
                                   current_hand=hand,
                                   valid_moves=valid_moves,
                                   players_active=players_active,
                                   players_protected=players_protected)
        while True:
            # selection = input(prompt + validity_prompt)
            selection = player.input_method.get_player_input(request_info)
            if isinstance(selection, int) and selection in [1, 2] and validity[selection - 1]:
                hand_vals = [c.get_value() for c in player.get_hand()]
                selected_card = player.play_card(int(selection) - 1)
                self.add_to_discard_pile(selected_card)
                out_string = f"{name} selects option {selection}: card value: {selected_card.get_value()} - {selected_card.get_description()}"
                if self.print_moves:
                    print("\n" + out_string)
                self.record_move(selection, description=out_string, hand=hand_vals)
                return (selected_card)
            elif selection == 'd':
                print(dp_verbose)
            else:
                request_info.invalid_moves += [selection]
                print('\n*** Invalid value. Try again...\n')


    def record_move(self, move, description = '',hand=[0,0]):
        turn = self.current_turn_number
        player = self.players[self.current_player_index]
        self.game_record.append({'turn'        : turn,
                                 'player'      : player,
                                 'hand'        : hand,
                                 'move'        : move,
                                 'description' : description})

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
        # show_discard_pile:	generate a dictionary of how many cards have been discarded so far of each card type
        # dict format: {card value (1-8) :  [#discarded, #total, card description]}

        num_of_cards_per_value = self.deck.get_num_of_cards_per_type()
        card_values = list(num_of_cards_per_value.keys())
        nums = list(num_of_cards_per_value.values())
        dp_list = {card_values[i] : [0, nums[i], self.deck.descriptions[i]] for i in range(len(nums))}

        for card in self.discard_pile:
            dp_list[card.get_value()][0] += 1

        dp_verbose = Game.header_prompt('Discard pile')

        format_str = "{:<8}{:<13}{:<10}{:<10}{:<40}\n"
        dp_verbose += format_str.format('Value', '# discarded', '# in play', '# in deck', 'Description')
        dp_verbose += "-"*130 + '\n'
        for v in card_values:
            dp_verbose += format_str.format(v, dp_list[v][0], dp_list[v][1]-dp_list[v][0], dp_list[v][1], dp_list[v][2])

        return dp_list, dp_verbose

    def do_next_player_turn(self):
        # 		do_player_turn:			remove protection, draw a card and give it to a player, show user both cards
        #                               (+ discard pile), ask for input, check validity, run card logic
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
        self.current_turn_number += 1

    def is_game_over(self):
        if sum(self.player_active_status) == 1:
            return('Game over - 1 player remaining')
        elif self.deck.is_empty():
            card_desc = [(f"{self.players[i].get_hand()[0].get_value()} - " + \
                          f"{self.players[i].get_hand()[0].get_description()}")
                         * self.player_active_status[i] for i in range(self.num_of_players)
                         if self.players[i].get_hand()]
            player_names = [self.players[i].get_name() * self.player_active_status[i] for i in
                            range(self.num_of_players) if self.players[i].get_hand()]
            final_state = [' - '.join([a,b]) for (a,b) in zip(player_names, card_desc)]
            return(f'Game over - deck is depleted. Current active players\' hands:\n'+'\n'.join(final_state))
        return (False)

    def get_game_record(self):

        out_string = f"Move list - full version:\n"

        out_string += "{:<10}{:<40}{:<10}{:<10}{:<40}\n".format('Turn', 'Player', 'Hand', 'Move', 'Description')
        out_string += "-"*130 + '\n'

        for r in self.game_record:
            s1 = r['turn']
            s2 = r['player'].get_name()
            s3 = f"{r['hand']}"
            s4 = r['move']
            s5 = r['description']

            out_string += "{:<10}{:<40}{:<10}{:<10}{:<40}\n".format(s1,s2,s3,s4,s5)

        out_string += f"\nMove list - short version:\nDeck:{self.deck_for_debug}\nMoves:{[r['move'] for r in self.game_record]}"

        return(out_string)

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
        current_player_name = current_player.get_name()
        prompt_str_1 = f"{current_player_name}, select your target:\n"
        prompt_str_2 = '\n'.join([f"{i+1} - {self.players[i].get_name()} {protection_str[self.protected[i]]}" for i in opponent_indices])
        prompt_str = prompt_str_1 + prompt_str_2 + '\n'
        valid_moves = [i+1 for i in opponent_indices if not self.protected[i]]
        players_active = self.player_active_status
        players_protected = self.protected
        request_info = RequestInfo(human_string=prompt_str,
                                   action_requested='opponent',
                                   valid_moves=valid_moves,
                                   players_active=players_active,
                                   players_protected=players_protected)

        while True:

            index = current_player.input_method.get_player_input(request_info)

            try:
                val = int(index)
                output_str = (f"{current_player_name} selects player index {index} ({self.players[index-1].get_name()})")
                if self.print_moves:
                    print(output_str)
                hand_vals = [c.get_value() for c in current_player.get_hand()]
                self.record_move(index, description=output_str, hand=hand_vals)

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
        current_player_name = current_player.get_name()

        prompt_str_1 = f"{current_player_name}, guess the card (2 or higher):\n"
        prompt_str_2 = self.deck.show_descriptions()
        prompt_str = prompt_str_1 + prompt_str_2 + '\n'
        valid_moves = list(range(2,9))
        players_active = self.player_active_status
        players_protected = self.protected
        request_info = RequestInfo(human_string=prompt_str,
                                   action_requested='guess',
                                   valid_moves=valid_moves,
                                   discard_pile=self.show_discard_pile()[0],
                                   current_hand=current_player.get_hand(),
                                   players_active=players_active,
                                   players_protected=players_protected)


        while True:

            # index = int(input(prompt_str_1 + prompt_str_2 + "\n"))
            index = current_player.input_method.get_player_input(request_info)
            output_str = f"{current_player_name} guesses card value of: {index}"
            hand_vals = [c.get_value() for c in current_player.get_hand()]
            self.record_move(index, description=output_str, hand=hand_vals)

            if self.print_moves:
                print(output_str)

            if index in range(2, 9):
                return index

            request_info.invalid_moves += [index]
            print(f"** Incorrect value entered ({index}), try again: **")

    def set_player_lose(self, index):
        # Set a player status to "lose"
        self.player_active_status[index] = False
        if self.players[index].get_hand(): # If player had just played the princess, their hand is empty
            self.add_to_discard_pile(self.players[index].play_card())

        return (f"{self.players[self.current_player_index].get_name()} loses and is out of the game.")

    def run_logic(self, active_player_index, opponent_index, played_card_value, guessed_value=0):

        result = None           # Default value for cards without an opponent. winner == 1: Player wins. 2: Opponent wins
                                # If card played is 2(Look), the result is the Card object the opponent is holding

        # Quick check for all-opponents-protected scenario
        if opponent_index==-1:
            return_str = "All opponents protected. Nothing happens"
            return(return_str,result)

        # Performs the actual logic behind each played card
        current_player = self.players[active_player_index]
        opponent = self.players[opponent_index]
        current_player_card = current_player.get_hand()[0] # This is the card the player is still holding, i.e. that wasn't played
        opponent_card = opponent.get_hand()[0]
        current_player_name = current_player.get_name()
        opponent_name = opponent.get_name()
        current_player_value = current_player_card.get_value()
        opponent_value = opponent_card.get_value()

        if played_card_value == 1:    # Guess
            if opponent_value == guessed_value:
                self.set_player_lose(opponent_index)
                result = 1
                return_str = f"Correct! {opponent_name} has a card value: {opponent_value}. {opponent_name} loses and is out of the game"
            else:
                return_str = f"Incorrect! {opponent_name} has a different card value. Nothing happens"


        elif played_card_value == 2:  # Look

            return_str = f"{opponent_name}'s hand is: {opponent_value} - {opponent_card.get_description()}"
            result = opponent_card

        elif played_card_value == 3:  # Compare

            if current_player_value > opponent_value:
                self.set_player_lose(opponent_index)
                result = (1, opponent_value)
                return_str = f"{current_player_name} (card value: {current_player_value}) wins.\n" + \
                        f"{opponent_name} (card value: {opponent_value}) loses and is out of the game"
            elif current_player_value < opponent_value:
                self.set_player_lose(active_player_index)
                result = (2, current_player_value)
                return_str = f"{opponent_name} (card value: {opponent_value}) wins.\n" + \
                        f"{current_player_name} (card value: {current_player_value}) loses and is out of the game"
            else:
                result = (0,0)
                return_str = f"It's a draw! Both players have card value: {opponent_value}. Nothing happens"

        elif played_card_value == 5:  # Discard

            discarded_card = opponent.play_card()
            discarded_card_value = discarded_card.get_value()
            result = discarded_card_value

            self.add_to_discard_pile(discarded_card)
            if discarded_card_value == 8:
                self.set_player_lose(opponent_index)
                return_str = f"{opponent_name} discards a Princess and loses this round"
            elif self.deck.is_empty():
                self.set_player_lose(opponent_index)
                return_str = f"Deck is empty - {opponent_name} cannot take a new card and loses this round"
            else:
                new_card = self.draw_card()
                opponent.add_card(new_card)
                return_str = f"{opponent_name} discards a card value of {discarded_card_value} and draws a new card"

        elif played_card_value == 6:  # Trade hands
            current_player.play_card()
            opponent.play_card()
            current_player.add_card(opponent_card)
            opponent.add_card(current_player_card)
            return_str = f"{current_player_name} and {opponent_name} have traded hands"

        return(return_str,result)

    def enable_protection(self, player_index):
        # Set protection to player
        current_player_name = self.players[player_index].get_name()
        self.protected[player_index] = True
        return (f"{current_player_name} is now protected")

    def disable_protection(self, player_index):
        # Remove protection from player
        if self.protected[player_index]:
            current_player_name = self.players[player_index].get_name()
            self.protected[player_index] = False
            return (f"{current_player_name} is no longer protected")
        return ("")

    def run_card_logic(self, selected_card):
        # 		run_card_logic:			run card logic. Make sure to check for protection. E.g. card==1, prompt for non-protected targets and guesses card value.
        # 								If all targets are protected, do nothing. Compare guess to card value. If matched, remove player from the game.
        # 									Also: check if princess was forced to be discarded when running 5's logic

        opponent_index = None    # Default value for cards without an opponent
        guessed_value = None    # Default value for cards without a guess (i.e. 2-8)
        result = None           # Default value for cards without an opponent (2,4,6,7).
                                    #  winner_idx == 1: Player wins. 2: Opponent wins
                                    #  for the 2(Look at card), result is the opponent's card value
                                    #  Note: if a 5 is played against a Princess (8), winner_idx == 1
        result_private = None   # Default value for viewed opponent's card when playing the 2 (Look)

        selection = selected_card.get_value()
        current_player_index = self.current_player_index

        # Get remaining card (hand before action - needed for summary):
        remaining_card = self.players[self.current_player_index].get_hand()[0]

        if selection == 8:  # Princess - lose this round

            output_str = self.set_player_lose(current_player_index)
            result = 2 # Player actually loses here. Not really important though

        elif selection == 7:  # Sensei - do nothing

            output_str = f"{self.players[current_player_index].get_name()} discards a card value of {selected_card.get_value()}. Nothing happens."

        elif selection == 4:

            output_str = self.enable_protection(current_player_index)

        elif selection == 2:            # Look at a player's card - only the active player gets the result

            opponent_index = self.get_opponent_index()
            output_str, result_private = self.run_logic(current_player_index, opponent_index, selection)

        elif selection in [3, 5, 6]:    # Compare/Discard/Trade - everyone can see the discarded cards

            opponent_index = self.get_opponent_index()
            output_str, result = self.run_logic(current_player_index, opponent_index, selection)

        elif selection == 1:  # Guard - pick an opponent and guess their hand

            opponent_index = self.get_opponent_index()
            guessed_value = self.get_guessed_value()
            output_str, result = self.run_logic(current_player_index, opponent_index, selection, guessed_value)
        else:

            output_str = (f"Error - bad value {selection} entered")

        if result_private == None:
            result_private = result

        if self.print_moves:
            print(output_str)

        dp_list, dp_verbose = self.show_discard_pile()

        # Public summary - all other players get this
        move_summary_public = {'player_num'    : current_player_index,
                        'card_played'   : selected_card,
                        'remaining_card': None,                             # This is the player's remaining hand
                        'opponent'      : opponent_index,
                        'guessed_value' : guessed_value,
                        'result'        : result,
                        'discard_pile'  : dp_list
                        }

        # Private summary - only the active player gets this
        move_summary_private = {'player_num'    : current_player_index,
                        'card_played'   : selected_card,
                        'remaining_card': remaining_card,
                        'opponent'      : opponent_index,
                        'guessed_value' : guessed_value,
                        'result'        : result_private,
                        'discard_pile'  : dp_list
                        }

        move_summary = {'move_summary_public' :move_summary_public,
                        'move_summary_private':move_summary_private}
        return(move_summary)

    def decide_winner(self):
        # decide_winner:			returns winner from all remaining players (highest card value wins). Returns a list, in case of a draw

        remaining_players = [self.players[i] for i in range(self.num_of_players) if self.players[i].get_hand() and self.player_active_status[i]]
        remaining_card_values = [p.get_hand()[0].get_value() for p in remaining_players]
        winners = [remaining_players[i] for i, x in enumerate(remaining_card_values) if x == max(remaining_card_values)]
        winners_indices = [i for i, x in enumerate(remaining_card_values) if x == max(remaining_card_values)]

        return(winners, winners_indices)

    def send_updates(self, move_summary):
        # Give the private summary one to active player, and give the public one to everyone else
        # Note: only difference between public and private is the value of the looked-at card when playing the 2(Look)
        player_idx = move_summary['move_summary_private']['player_num']
        # Give private summary to current player, and public summary to all other players
        [p.input_method.update_state(move_summary['move_summary_public'])  for p in self.players[:player_idx]]
        self.players[player_idx].input_method.update_state(move_summary['move_summary_private'])
        [p.input_method.update_state(move_summary['move_summary_public'])  for p in self.players[(player_idx+1):]]

    def play(self):
        # play:					runs the main game loop until a winner is declared. Returns winner index

        game_over = False
        while not game_over:
            selected_card = self.do_next_player_turn()
            move_summary = self.run_card_logic(selected_card)
            self.send_updates(move_summary)
            self.advance_current_player()
            game_over = self.is_game_over()


        self.winners = self.decide_winner()
        # return (game_over + '\n' + str(self.winners))
        print(game_over)
        return(self.winners)

