from collections import Iterable
from InputMethodInterface import InputMethodInterface

class PlayLogicHardCoded:
    # Defines a play logic which outputs values from a moves list defined at init. Useful for tests
    def __init__(self, moves_list):

        def iter_const(v):
            while True:
                yield v

        if isinstance(moves_list, Iterable):  # Check if moves_list is iterable. If so, make an iterable out of it
            self.moves_list = iter(moves_list)
        elif isinstance(moves_list, int):  # Check if it's an integer. If so, make an endless iterable out of it
            self.moves_list = iter_const(moves_list)
        else:  # Default to a constant int of 1. Not sure this is such a good idea
            self.moves_list = iter_const(v=1)

    def get_next_value(self, request_info):

        InputMethodInterface.check_request_info_type(request_info)

        try:
            return (next(self.moves_list))
        except StopIteration:
            print(self.name + ' input moves list exhausted!')
            return (None)


    def update_state(self, move_summary, hand = []):
        print(f'Hard-coded AI is (not) updating state..')

    def init_hand_options(self, hand, dp_list):
        print(f'Hard-coded AI is (not) initializing hand options..')
