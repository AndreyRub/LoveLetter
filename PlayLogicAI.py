import random
from InputMethod import InputMethod
import play_logic_infra

class PlayLogicAI:
    # Defines a play logic with some AI behind it. Relevant AI is chosen in init
    def __init__(self, player_index=None, ai_type='random', seed=0, num_of_players=4):

        self.num_of_players = num_of_players
        self.player_index = player_index

        hand_options = list(range(1,9)) # List of opponent hand options. Will be overridden using discard pile and play history

        self.ai_type = ai_type
        self.state = {'hand_options'     :  [hand_options]*num_of_players,   # If player's card is known, only one option remains
                      'knows_my_card'   :   [None]*num_of_players,           # If not None, specifies which card value opponent knows I have
                      'played_the_7'    :   [False]*num_of_players           # Has this player played the 7 on their last turn?
                      }

        self.next_move = {'next_card' : None,
                          'next_opponent' : None,
                          'next_guess' : None
                          }

        if self.ai_type == 'random' and seed != 0:
            random.seed(seed)

    def init_hand_options(self, hand, dp_list):
        #     Used to initialize self.state['hand_options'] after first card is dealt and before first turn
        other_player_indices = list(range(self.num_of_players))
        other_player_indices.pop(self.player_index)
        for ind in other_player_indices:
            self.state['hand_options'][ind] = play_logic_infra.get_active_cards_list(dp_list, hand)
        self.state['hand_options'][self.player_index] = hand
        print(f"AI player #{self.player_index} is initializing hand options...")

    def remove_new_card_from_opponents_hand_options_before_move(self, card):
        for i in list(set(range(self.num_of_players)) - {self.player_index}):
            play_logic_infra.remove_one_card_from_list(self.state['hand_options'][i], card)

    def update_state(self, move_summary):
        print(f'AI is updating state..')

        player_num              = move_summary['player_num']
        card_played             = move_summary['card_played']
        card_played_value       = card_played.get_value()
        remaining_card          = move_summary['remaining_card']
        if remaining_card:
            remaining_card_value= remaining_card.get_value()
        opponent                = move_summary['opponent']
        guessed_value           = move_summary['guessed_value']
        result                  = move_summary['result']
        dp_list                 = move_summary['discard_pile']

        this_was_my_turn = self.player_index==player_num
        all_opponents_protected = opponent == -1


        if this_was_my_turn:
            if all_opponents_protected:
                return  # Do nothing

            if card_played_value == 1:
                pass                                                                # There's actually very little to do here
            elif card_played_value == 2:
                self.state['hand_options'][opponent] = [result.get_value()]         # Remember to remove this if player plays it on their turn
                # Remove viewed card ("result") from all other players' hand options
                for i in list(  set(range(self.num_of_players)) - {player_num}):
                    play_logic_infra.remove_one_card_from_list(self.state['hand_options'][i], result.get_value())

            elif card_played_value == 3 and result!=1:                                # We compared cards and it was a draw
                self.state['hand_options'][opponent] = [remaining_card_value]
            elif card_played_value == 6:                                              # We swapped cards
                self.state['hand_options'][opponent] = [remaining_card_value]

        if not this_was_my_turn:
            # If player played his previously-known card, reset the hand options:
            if card_played_value in self.state['hand_options'][player_num]:
                self.state['hand_options'][player_num] = play_logic_infra.get_active_cards_list(dp_list)

            # Remove played card from all other players' hand options
            # Note: we're doing this instead of just looking at the discard pile, in order
            # to retain any information about cards known not to be in this player's deck
            # (e.g. Player 1 plays guard w/ 5 against player 4 and fails. Player 2 plays a 3. We need to remember Player 4 does not have a 5)

            for i in list(set(range(self.num_of_players)) - {player_num}):
                play_logic_infra.remove_one_card_from_list(self.state['hand_options'][i],card_played_value)

            # If all opponents were protected there's no more information available
            if all_opponents_protected:
                return  # Do nothing

            # Card-specific knowledge:

            if card_played_value == 1 and result!=1:                        # Player guessed wrong
                play_logic_infra.remove_all_cards_from_list(self.state['hand_options'][opponent], guessed_value)

            if card_played_value == 2 and opponent==self.player_index:
                self.state['knows_my_card'][player_num] = True

            if card_played_value == 3:
                if not isinstance(result,tuple):
                    a=2
                elif result[0] == 1:  # Player has a higher card value than opponent
                    for val in range(1, result[1] - 1):  # Remove all lower values from current player's list
                        play_logic_infra.remove_all_cards_from_list(self.state['hand_options'][player_num], val)
                elif result[0] == 2:  # Player has a lower card value than opponent
                    for val in range(1, result[1] - 1):  # Remove all lower values from current player's list
                        play_logic_infra.remove_all_cards_from_list(self.state['hand_options'][opponent], val)
                elif result[0] == 0:  # Player has a same card value as opponent - intersect hands and set to both players
                    shared_hand_options = [v for v in self.state['hand_options'][opponent] if v in self.state['hand_options'][player_num]]
                    self.state['hand_options'][opponent] = shared_hand_options
                    self.state['hand_options'][player_num] = shared_hand_options

            if card_played_value == 5:
                self.state['hand_options'][opponent] = play_logic_infra.get_active_cards_list(dp_list)
                # Remove discarded card ("result") from all other players' hand options
                for i in list(  set(range(self.num_of_players)) - {opponent}):
                    play_logic_infra.remove_one_card_from_list(self.state['hand_options'][i], result)

            if card_played_value == 6:                                  # Swap knowledge about players' hands
                temp = self.state['hand_options'][opponent]
                self.state['hand_options'][opponent] = self.state['hand_options'][player_num]
                self.state['hand_options'][player_num] = temp

            if card_played_value == 7:
                self.state['played_the_7'][player_num] = True # TODO: consider how to add information from the 5,7 / 6,7 rule



    def get_card_guess(self, request_info):

        InputMethod.check_request_info_type(request_info)
        request_info_data = request_info.get_request_info()

        valid_inputs        = request_info_data['valid_moves']
        dp_list             = request_info_data['discard_pile']
        hand                = request_info_data['current_hand']
        players_active      = request_info_data['players_active']
        players_protected   = request_info_data['players_protected']

        state = self.state

        # NEXT MOVE LOGIC - currently just random for testing
        next_card = [1,2]
        next_opponent_set =  set([k+1 for k in range(len(players_active)) if players_active[k]]) - {self.player_index+1}
        protected_set = set([k+1 for k in range(len(players_active)) if players_protected[k]])
        next_opponent = list(next_opponent_set - protected_set)
        next_guess = list(range(2,9))

        self.next_move['next_card']      = next_card
        self.next_move['next_opponent']  = next_opponent
        self.next_move['next_guess']     = next_guess



    def get_next_value(self, request_info):

        InputMethod.check_request_info_type(request_info)
        request_info_data = request_info.get_request_info()

        valid_inputs    = request_info_data['valid_moves']
        dp_list         = request_info_data['discard_pile']
        hand            = request_info_data['current_hand']

        valid_guesses = valid_inputs

        if self.ai_type == 'random':
            pass # Do nothing - just choose randomly from the valid inputs

        if self.ai_type == 'random2':
            # Like random, but:
            #   When using the Guard(1), chooses only cards that are in play
            #   Never choose the Princess(8) (actively choosing to lose is a rare, multiple-game strategy. Save it for later)

            if request_info_data['action_requested'] == 'card':
                is_princess = [c.get_value()==8 for c in hand]
                if any(is_princess):
                    valid_guesses = [valid_guesses[i] for i in range(len(valid_guesses)) if not is_princess[i]]

            if request_info_data['action_requested'] == 'guess':
                num_in_play = play_logic_infra.get_num_of_cards_in_play(dp_list, hand)

                # Manually remove the "Guard" option
                num_in_play[1] = 0

                valid_guesses = [i for (i,x) in enumerate(num_in_play) if x>0]

                # Keep only the values which are allowed by the caller
                valid_guesses = list(set(valid_guesses) & set(valid_inputs))

        if self.ai_type == 'simple_logic':


            if request_info_data['action_requested'] == 'card':
                # Start by removing the new card from all opponents' hand options
                self.remove_new_card_from_opponents_hand_options_before_move(hand[1])
                self.get_card_guess(request_info)

            if request_info_data['action_requested'] == 'card':
                return(random.choice(self.next_move['next_card']))
            if request_info_data['action_requested'] == 'opponent':
                return(random.choice(self.next_move['next_opponent']))
            if request_info_data['action_requested'] == 'guess':
                return(random.choice(self.next_move['next_guess']))



        # In case only Guards are in play, we must play another card, knowing it will fail
        if len(valid_guesses)==0:
            valid_guesses = list(range(2,9))

        return(random.choice(valid_guesses))
