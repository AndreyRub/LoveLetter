import random
from InputMethod import InputMethod
import play_logic_infra
from time import sleep

class PlayLogicAI:

    @staticmethod
    def get_next_player_index(current_index, num_of_players, active_status):
        next_index = (current_index + 1) % num_of_players
        while not active_status[next_index]:
            next_index = (next_index + 1) % num_of_players
        return next_index



    # Defines a play logic with some AI behind it. Relevant AI is chosen in init
    def __init__(self, player_index=None, ai_type='random', seed=0, num_of_players=4):

        self.num_of_players = num_of_players
        self.player_index = player_index

        hand_options = list(range(1,9)) # List of opponent hand options. Will be overridden using discard pile and play history

        self.ai_type = ai_type
        self.state = {'hand_options'     :  [hand_options]*num_of_players,   # If player's card is known, only one option remains
                      'knows_my_card'   :   [False]*num_of_players,           # If not None, specifies which card value opponent knows I have
                      'played_the_7'    :   [False]*num_of_players,          # Has this player played the 7 on their last turn?
                      'number_of_1s_played' : [0]*num_of_players
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
        self.state['hand_options'][self.player_index] = [card.get_value() for card in hand]
        print(f"AI player #{self.player_index} is initializing hand options...")

    def remove_new_card_from_opponents_hand_options_before_move(self, card):
        for i in list(set(range(self.num_of_players)) - {self.player_index}):
            if len(self.state['hand_options'][i]) > 1:
                play_logic_infra.remove_one_card_from_list(self.state['hand_options'][i], card)

    def update_state(self, move_summary, hand = []):
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

        my_hand = hand

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
                for i in list(  set(range(self.num_of_players)) - {opponent}):
                    if len(self.state['hand_options'][i]) > 1 :
                        play_logic_infra.remove_one_card_from_list(self.state['hand_options'][i], result.get_value())

            elif card_played_value == 3 and result!=1:                                # We compared cards and it was a draw
                self.state['hand_options'][opponent] = [remaining_card_value]
            elif card_played_value == 6:                                              # We swapped cards
                self.state['hand_options'][opponent] = [remaining_card_value]
                self.state['knows_my_card'][opponent] = True

        if not this_was_my_turn:
            # If player played his previously-known card, reset the hand options:
            if card_played_value in self.state['hand_options'][player_num]:
                self.state['hand_options'][player_num] = play_logic_infra.get_active_cards_list(dp_list)

            # Remove played card from all other players' hand options
            # Note: we're doing this instead of just looking at the discard pile, in order
            # to retain any information about cards known not to be in this player's deck
            # (e.g. Player 1 plays guard w/ 5 against player 4 and fails. Player 2 plays a 3. We need to remember Player 4 does not have a 5)

            for i in list(set(range(self.num_of_players)) - {player_num}):
                if len(self.state['hand_options'][i])>1:
                    play_logic_infra.remove_one_card_from_list(self.state['hand_options'][i],card_played_value)

            if card_played_value == 1:
                self.state['number_of_1s_played'][player_num] += 1

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
                    raise TypeError("When playing the 3, result passed through move_summary should be in the form of a tuple (winner, discarded_card)")
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
                    if len(self.state['hand_options'][i]) > 1 :
                        play_logic_infra.remove_one_card_from_list(self.state['hand_options'][i], result)

            if card_played_value == 6:                                  # Swap knowledge about players' hands
                temp = self.state['hand_options'][opponent]
                self.state['hand_options'][opponent] = self.state['hand_options'][player_num]
                self.state['hand_options'][player_num] = temp
                if self.player_index == opponent: # If I'm the opponent, the player knows my card
                    self.state['knows_my_card'][player_num] = True

            if card_played_value == 7:
                self.state['played_the_7'][player_num] = True # TODO: consider how to add information from the 5,7 / 6,7 rule


    def get_next_move(self, request_info):
        # Used in simple_logic AI - at start of player's current move, decide on card to play, opponent and guess (if needed)

        InputMethod.check_request_info_type(request_info)
        request_info_data = request_info.get_request_info()

        valid_inputs        = request_info_data['valid_moves']
        dp_list             = request_info_data['discard_pile']
        hand                = request_info_data['current_hand']
        players_active      = request_info_data['players_active']
        players_protected   = request_info_data['players_protected']

        players_relevant = [active and not protected for active,protected in zip(players_active,players_protected)]
        players_relevant[self.player_index] = False

        everyone_is_protected = not any(players_relevant)

        hand_options = self.state['hand_options']

        i_know_their_card = [players_relevant[i] and len(hand_options[i]) == 1 for i in range(self.num_of_players)]

        their_card_value = [hand_options[i][0] for i in range(self.num_of_players)]

        state = self.state

        # Get old and new card values. This will be needed later
        old_card = hand[0]
        new_card = hand[1]
        hand_pair = [c.get_value() for c in hand]
        action_pair = (min(old_card.get_value(),new_card.get_value()) , max(old_card.get_value(),new_card.get_value()))


        # Some data collection:

        number_of_players = len(players_active)

        # Get number of cards still in play, for each card value
        # 1. Start with discard pile
        num_cards_still_in_play = [dp_list[v][1]-dp_list[v][0] for v in range(1,9)]
        num_cards_still_in_play = [0] + num_cards_still_in_play # Align indices with card values. E.g. num_cards_still_in_play[4] accesses number of 4(Handmaiden) cards in play
        # 2. Remove cards in current hand from cards in play
        for card in hand:
            num_cards_still_in_play[card.get_value()] -= 1

        # Get number of "5" cards still in play (these lower the expected number of turns remaining)
        num_5s_still_in_play = num_cards_still_in_play[5]

        # Get number of expected remaining turns per player, assuming both 5s are played. Remember 1 card is out of the deck!
        remaining_turns_per_player = [0] * number_of_players
        next_player_index = self.player_index
        for ind in range(sum(num_cards_still_in_play) - num_5s_still_in_play - 1):
            next_player_index = PlayLogicAI.get_next_player_index(current_index=next_player_index,
                                                                         num_of_players=number_of_players,
                                                                         active_status=players_active)
            remaining_turns_per_player[next_player_index] += 1
        remaining_turns_for_me = remaining_turns_per_player[self.player_index]

        # is_threat - Has this player looked at my hand, it's over 1, they have another turn remaining and they might have a 1?
        is_threat = [self.state['knows_my_card'][i] and
                     old_card.get_value() != 1 and
                     remaining_turns_per_player[i] > 0 and
                     num_cards_still_in_play[1] > 0 and
                     players_active[i]
                     for i in range(number_of_players)]

        i_am_threatened = any(is_threat)
        threatening_player = None if not i_am_threatened else is_threat.index(True)
        threatening_player_is_protected = None if not i_am_threatened else players_protected[threatening_player]
        threatened_but_they_have_1 = i_am_threatened and i_know_their_card[threatening_player] and their_card_value[threatening_player] == 1
        threatened_but_unable = i_am_threatened and (threatening_player_is_protected or their_card_value[threatening_player] == 1)


        # Definitions:
        # most_1s_played_first = Sorted list(descending) of  # of 1s played (i.e. player with MOST 1s played is best target)
        # least_1s_played_first = Sorted list(ascending) of  # of 1s played (i.e. player with LEAST 1s played is best target)
        # this_is_my_last_turn = true if deck_size < number_of_players[+1 if there's at least one active 5 card in play]
        # this_is_the_last_move = true if deck_size == 0

        most_1s_played_first = list(
            sorted(range(number_of_players), key=lambda k: self.state['number_of_1s_played'][k]+100*players_relevant[k]+1000*players_active[k],reverse=True))
        most_1s_played_first.pop(most_1s_played_first.index(self.player_index))
        least_1s_played_first = list(
            sorted(range(number_of_players), key=lambda k: self.state['number_of_1s_played'][k]-100*players_relevant[k]-1000*players_active[k] ))
        least_1s_played_first.pop(least_1s_played_first.index(self.player_index))
        this_is_my_last_turn = remaining_turns_per_player[self.player_index]==0
        this_is_the_last_move = sum(num_cards_still_in_play)==1 # Remember there's one card out of the deck

        # Tests: define IF this card should be played (used during full logic stage. Not always sufficient)
        # 3-test(N=other_card): Anyone has (1,2,...N-1)?
        # 5-test(): Anyone has 6,7,8?
        # 6-test(): anyone has 7,8?
        # Princess-test: does anyone have a princess?


        # 3-test(N=other_card): Anyone has (1,2,...N-1)? E.g. test3_result[other_card_value]
        # TODO: if all other hand_options are lower than my other card (i.e. a guaranteed win), I can play this card as well
        test3_result = [any([players_relevant[i] and i_know_their_card[i] and their_card_value[i]<N for i in range(number_of_players)])
                        for N in range(0,9)]

        # 5-test(): Anyone has 6,7,8? Also if threatening player has a 1
        test5_result = threatened_but_they_have_1 or \
                       any([players_relevant[i] and i_know_their_card[i] and their_card_value[i] in [6,7,8] for i in
                             range(number_of_players)])
        # 6-test(): anyone has 7,8? Also if threatening player has a 1
        test6_result = threatened_but_they_have_1 or \
                       any([players_relevant[i] and i_know_their_card[i] and their_card_value[i] in [7,8] for i in
                             range(number_of_players)])

        # Princess-test: does anyone have a princess? (Note: this makes that opponent the target. It does *not* mean we should play the Princess...)
        test8_result = any([players_relevant[i] and i_know_their_card[i] and their_card_value[i] == 8 for i in
                             range(number_of_players)])

        #    Targets - If a card is chosen, this picks the opponent (if required):
        #        Result should be an list of equal-probability targets
        #    1-target:
        #       before everything: if I am threatened - choose the threatening player
        #        Is there a player whose card is known and isn't a 1?
        #            If so - make this player the current 1-target
        #        If there is more than one 1-target: sort them by known card value. Append the remaining players
        #        otherwise: random opponent, guess from remaining non-1 active cards
        if i_am_threatened and not threatening_player_is_protected and players_active[threatening_player]:
            target1 = threatening_player
        else:
            target1 = [i for i in range(self.num_of_players) if players_relevant[i] and i_know_their_card[i] and their_card_value[i]>1 ]
            if len(target1) > 1: # Get target with largest card value
                target_values = [their_card_value[target1[k]] for k in range(len(target1))]
                target1 = target1[target_values.index(max(target_values))]
                # target1 = target1[target1.index(max([their_card_value[i] for i in target1]))] # Get target with largest card value
            elif len(target1) == 1:
                target1 = target1[0]
            elif len(target1) == 0 and any(players_relevant):
                target1 = random.choice([i for i in range(self.num_of_players) if players_relevant[i]])
            else: #probably all players are protected. Doesn't matter.
                target1 = -100 # This value should never be used

        if target1 != -100 and not players_relevant[target1]  and not everyone_is_protected:
            temp_active = [v for v in players_active]
            temp_active[self.player_index] = False
            target1 = temp_active.index(True)


        #    2-target:
        #        most_1s_played_first
        target2 = most_1s_played_first[0]
        if players_protected[target2]  and not everyone_is_protected:
            temp_active = [v for v in players_active]
            temp_active[self.player_index] = False
            target2 = temp_active.index(True)


        #    3-target(hand=current_card):
        #        Do I know what they're holding AND it's lower than my hand?
        #            If so - make this player the current 3-target
        #        Otherwise:
        #            least_1s_played_first
        target3 = [None] * 9
        for N in range(0,9): # 0 is just a filler
            good_3_target = [i_know_their_card[i] and their_card_value[i]<N for i in range(number_of_players)]
            if any(good_3_target):
                target3[N] = good_3_target.index(True)
            else:
                target3[N] = least_1s_played_first[0]

        #    5-target:
        #        Is anyone threatening me, with a known 1?   If so - make this player the current 5-target
        #        If anyone holding the princess?             If so - make this player the current 5-target
        #        If anyone holding 6 or 7?                   If so - make this player the current 5-target
        #        Otherwise: avoid 1s
        #            most_1s_played_first
        if threatened_but_they_have_1 and not threatened_but_unable:
            target5 = threatening_player
        elif any([i_know_their_card[i] and their_card_value[i] == 8 for i in range(number_of_players)]):
            target5 = [i_know_their_card[i] and their_card_value[i] == 8 for i in range(number_of_players)].index(True)
        elif any([i_know_their_card[i] and their_card_value[i] in [6,7] for i in range(number_of_players)]):
            target5 = [i_know_their_card[i] and their_card_value[i] in [6,7] for i in range(number_of_players)].index(True)
        else:
            target5 = most_1s_played_first[0]

        #    6-target:
        #        Is anyone threatening me, with a known 1?   If so - make this player the current 6-target
        #        Is anyone holding 7 or 8?                   If so - make this player the current 6-target
        #        Otherwise:
        #            If this_is_my_last_turn: avoid 1s:
        #                most_1s_played_first
        #            If not this_is_my_last_turn: prefer 1s:
        #                least_1s_played_first
        if threatened_but_they_have_1 and not threatened_but_unable:
            target6 = threatening_player
        elif any([i_know_their_card[i] and their_card_value[i] in [7,8] for i in range(number_of_players)]):
            target6 = [i_know_their_card[i] and their_card_value[i] in [7,8] for i in range(number_of_players)].index(True)
        else:
            if this_is_my_last_turn:
                target6 = most_1s_played_first[0]
            else:
                target6 = least_1s_played_first[0]

        #    1-guess: If known, use it.
        #             Otherwise: most threatening card, based on the other card left.
        #                if I'm holding a Princess, go for the 5 or 6
        #                if I'm holding a 7: go for 8 (or a 6? depending on #turns left)
        #                If I'm holding a lower card: go for the most-likely card of a higher value
        if isinstance(target1,list):
            a=2
        if target1==-100:  # All players are protected. Shouldn't get here
            guess1 = None
        elif i_know_their_card[target1]:
            guess1 = their_card_value[target1]
        else:
            other_card_value = max([c.get_value() for c in hand])
            target_hand_options = hand_options[target1]
            target_cards_of_higher_value = [v for v in target_hand_options if v>other_card_value]
            if other_card_value == 8:
                if 5 in target_hand_options: guess1 = 5
                elif 6 in target_hand_options: guess1 = 6
                else: guess1 = random.choice(target_hand_options)
            elif other_card_value == 7:
                if 8 in target_hand_options: guess1 = 8
                else: guess1 = random.choice(target_hand_options)
            elif len(target_cards_of_higher_value)>0:
                guess1 = random.choice(target_cards_of_higher_value)
            else:
                guess1 = random.choice(target_hand_options)

        if guess1 == 1:  # This is a case where the threatening player knows my card, but has a (known) card value of 1
            guess1 = 8


        # NEXT MOVE LOGIC
        if action_pair == (1,1):    next_card_value = 1
        elif action_pair == (1, 2): next_card_value = 2 if threatened_but_unable else 1 if i_am_threatened else 2 if not this_is_my_last_turn else 1
        elif action_pair == (1, 3): next_card_value = 1
        elif action_pair == (1, 4): next_card_value = 4 if threatened_but_unable else 1 if i_am_threatened else 1 if this_is_my_last_turn else 4
        elif action_pair == (1, 5): next_card_value = 5 if threatened_but_unable else 1
        elif action_pair == (1, 6): next_card_value = 6 if threatened_but_unable else 1 if i_am_threatened else 6 if this_is_the_last_move and test6_result else 1
        elif action_pair == (1, 7): next_card_value = 1
        elif action_pair == (1, 8): next_card_value = 1

        elif action_pair == (2, 2): next_card_value = 2
        elif action_pair == (2, 3): next_card_value = 3 if test3_result[2] else 2
        elif action_pair == (2, 4): next_card_value = 4 if any(is_threat) else 2
        elif action_pair == (2, 5): next_card_value = 5 if test5_result else 2
        elif action_pair == (2, 6): next_card_value = 6 if test6_result else 2
        elif action_pair == (2, 7): next_card_value = 2
        elif action_pair == (2, 8): next_card_value = 2

        elif action_pair == (3, 3): next_card_value = 3
        elif action_pair == (3, 4): next_card_value = 3 if test3_result[4] else 4
        elif action_pair == (3, 5): next_card_value = 5 if test5_result else 3 if test3_result[5] else random.choice([3,5])
        elif action_pair == (3, 6): next_card_value = 3 if test3_result[6] else 6 if test6_result else 3
        elif action_pair == (3, 7): next_card_value = 3
        elif action_pair == (3, 8): next_card_value = 3

        elif action_pair == (4, 4): next_card_value = 4
        elif action_pair == (4, 5): next_card_value = 5 if test5_result else 4
        elif action_pair == (4, 6): next_card_value = 6 if test6_result else 4
        elif action_pair == (4, 7): next_card_value = 4
        elif action_pair == (4, 8): next_card_value = 4

        elif action_pair == (5, 5): next_card_value = 5
        elif action_pair == (5, 6): next_card_value = 5 if test8_result else 6 if test6_result else 5 if test5_result else random.choice([5,6])
        elif action_pair == (5, 7): next_card_value = 7
        elif action_pair == (5, 8): next_card_value = 5

        elif action_pair == (6, 6): next_card_value = 6
        elif action_pair == (6, 7): next_card_value = 7
        elif action_pair == (6, 8): next_card_value = 6

        elif action_pair == (7, 7): next_card_value = 7
        elif action_pair == (7, 8): next_card_value = 7

        next_card =       hand_pair.index(next_card_value) + 1

        if   next_card_value == 1: next_opponent = target1 + 1
        elif next_card_value == 2: next_opponent = target2 + 1
        elif next_card_value == 3: next_opponent = target3[hand_pair[1 - hand_pair.index(3)]] + 1 # get 3-target for other card in hand
        elif next_card_value == 4: next_opponent = None
        elif next_card_value == 5: next_opponent = target5 + 1
        elif next_card_value == 6: next_opponent = target6 + 1
        elif next_card_value == 7: next_opponent = None
        elif next_card_value == 8:
            raise ValueError("Princess is not supposed to be chosen, exiting")

        next_guess = guess1

        # Set the next move to be played
        self.next_move['next_card']      = [next_card]
        self.next_move['next_opponent']  = [next_opponent]
        self.next_move['next_guess']     = [next_guess]

        print(next_opponent)
        if next_opponent and next_opponent!=-99 and not players_active[next_opponent-1]:
            print(f'card: {next_card} opponent: {next_opponent}  guess: {next_guess}')


       # # NEXT MOVE LOGIC - currently just random for testing
        # next_card = [1,2]
        # next_opponent_set =  set([k+1 for k in range(len(players_active)) if players_active[k]]) - {self.player_index+1}
        # protected_set = set([k+1 for k in range(len(players_active)) if players_protected[k]])
        # next_opponent = list(next_opponent_set - protected_set)
        # next_guess = list(range(2,9))



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
                self.remove_new_card_from_opponents_hand_options_before_move(hand[1].get_value())
                self.get_next_move(request_info)

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
