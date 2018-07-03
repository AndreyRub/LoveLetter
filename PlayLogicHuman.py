from collections import Iterable
from InputMethodInterface import InputMethodInterface

class PlayLogicHuman:
    # Defines a "Human" play logic (i.e. prompts the user for input)
    def __init__(self, name):

        self.name = name

    def get_next_value(self, request_info):

        InputMethodInterface.check_request_info_type(request_info)

        request_data = request_info.get_request_info()

        user_input = input(request_data['human_string'])

        try:
            return (int(user_input)) # used when input is a number (typically in [1..8])
        except:
            return (user_input) # used when input is a string (typically "d", when the human requests the discard pile)

    def init_hand_options(self, hand, dp_list):
        print('Human is (not) initializing hand options...')

    def update_state(self, move_summary):
        player_num = move_summary['player_num'] + 1
        card_played = move_summary['card_played']
        card_value = card_played.get_value()
        card_description = card_played.get_description()
        opponent_idx = move_summary['opponent']
        if opponent_idx!=None: opponent_idx += 1 # opponent_idx could be None if action has no opponents (4,7,8)
        guessed_value = move_summary['guessed_value']
        result = move_summary['result']

        output_str = f"Player #{player_num} played [{card_value} - {card_description}]"
        if opponent_idx:
            output_str += f" against Player #{opponent_idx}"

        if guessed_value:
            output_str += f", with guessed value {guessed_value}.\n"
        else:
            output_str += '.\n'


        if card_value == 1:
            if result == 1:
                output_str += f"Player #{player_num} WON! Player #{opponent_idx} lost!"
            elif result == 2:
                output_str += f"Player #{player_num} LOST! Player #{opponent_idx} won!"
            else:
                output_str += f"Player #{player_num} guessed incorrectly. No change."
        elif card_value == 2 and result: # only show looked-at card if result was given to player ("private result")
            output_str += f"Player #{opponent_idx}\'s card is: [{result.get_value()} - {result.get_description()}]"
        elif card_value == 3:
            if result[0] == 1:
                output_str += f"Player #{player_num} WON! Player #{opponent_idx} lost! Losing card has value: {result[1]}"
            elif result[0] == 2:
                output_str += f"Player #{player_num} LOST! Player #{opponent_idx} won! Losing card has value: {result[1]}"
            elif result[0] == 0:
                output_str += f"Player #{player_num} and Player #{opponent_idx} have identical cards. No change."
        elif card_value == 5:
            output_str += f"Card discarded has value: {result}\n"
            if result == 8:
                output_str += f"Player #{opponent_idx} has discarded the Princess and is out of the game.\n"
        else:
            output_str += f"Nothing happens"


        print(output_str)