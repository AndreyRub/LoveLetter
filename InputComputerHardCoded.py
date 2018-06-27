from InputMethodInterface import InputMethodInterface
import collections
from RequestInfo import RequestInfo

class InputComputerHardCoded(InputMethodInterface):
# Class InputComputerHardCoded(InputMethodInterface):
#     properties:
#         output_moves list: a hard-coded output moves_list iterator. Used for hard-coded unit tests with non-random decks. E.g. [1,2,6,2,2,4,1,...]
#
#             Note: this class can be used for each player separately, or as the same class for all 4 players
#
#     methods:
#         init:   sets output_moves_list iterator from input at creation.
#         get_player_input(request_info): loads current moves list value, updates the state index and returns the next move value
#                 function returns:
#                     played_move: int value as per current moves_list value

    def __init__(self, moves_list, name='Player'):

        super().__init__()
        self.name = name


        def iter_const(v):
            while True:
                yield v

        if isinstance(moves_list, collections.Iterable):  # Check if moves_list is iterable. If so, make an iterable out of it
            self.moves_list = iter(moves_list)
        elif isinstance(moves_list,int):                  # Check if it's an integer. If so, make an endless iterable out of it
            self.moves_list = iter_const(moves_list)
        else:                                           # Default to a constant int of 1. Not sure this is such a good idea
            self.moves_list = iter_const(v=1)


    def get_player_input(self, request_info):
        # Loads current moves_list value, updates the state index and returns the moves_list value
        #     function returns:
        #     played_move: int value as per current moves_list value

        self.check_request_info_type(request_info)

        print(request_info.get_request_info()['human_string'])

        try:
            return(next(self.moves_list))
        except StopIteration:
            print(self.name + ' input moves list exhausted!')
            return(None)

