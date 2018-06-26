from InputMethodInterface import InputMethodInterface
import collections
from RequestInfo import RequestInfo

class InputComputerHardCoded(InputMethodInterface):
# Class InputComputerHardCoded(InputMethodInterface):
#     properties:
#         output_sequence: a hard-coded output sequence iterator. Used for hard-coded unit tests with non-random decks. E.g. [1,2,6,2,2,4,1,...]
#
#             Note: this class can be used for each player separately, or as the same class for all 4 players
#
#     methods:
#         init:   sets output_sequence iterator from input at creation.
#         get_player_input(request_info): loads current sequence value, updates the state index and returns the sequence value
#                 function returns:
#                     played_move: int value as per current sequence value

    def __init__(self, sequence, name='Player'):

        super().__init__()
        self.name = name


        def iter_const(v):
            while True:
                yield v

        if isinstance(sequence, collections.Iterable):  # Check if sequence is iterable
            self.sequence = sequence
        elif isinstance(sequence,list):                 # Check if it's a list. If so, make an iterable out of it
            self.sequence = iter(sequence)
        elif isinstance(sequence,int):                  # Check if it's an integer. If so, make an endless iterable out of it
            self.sequence = iter_const(sequence)
        else:                                           # Default to a constant int of 1. Not sure this is such a good idea
            self.sequence = iter_const(v=1)


    def get_player_input(self, request_info):
        # Loads current sequence value, updates the state index and returns the sequence value
        #     function returns:
        #     played_move: int value as per current sequence value

        try:
            return(next(self.sequence))
        except StopIteration:
            print(self.name + ' input sequence exhausted!')
            return(None)

