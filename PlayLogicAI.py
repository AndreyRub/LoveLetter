import random
from InputMethod import InputMethod
import play_logic_infra

class PlayLogicAI:
    # Defines a play logic with some AI behind it. Relevant AI is chosen in init
    def __init__(self, ai_type='random', seed=1):

        self.ai_type = ai_type

        if self.ai_type == 'random':
            random.seed(seed)




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

        # In case only Guards are in play, we must play another card, knowing it will fail
        if len(valid_guesses)==0:
            valid_guesses = list(range(2,9))

        return(random.choice(valid_guesses))
