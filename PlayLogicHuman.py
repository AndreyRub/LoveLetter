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