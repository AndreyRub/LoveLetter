import collections
from RequestInfo import RequestInfo
from time import sleep

class InputMethod():
# Class InputMethod:
#     properties:
#               name
#               play_logic - a PlayerLogic object, used to process RequestInfo data and return play moves
#               print_request - handles whether to print out the "human" request string before passing the request_info
#                               to play_logic. Human PlayLogic objects typically print out the request so they should set
#                               this to False. Computer players can do either - for debugging it's useful to set to True
#
#     methods:
#         init:   sets player logic and other settings
#         get_player_input(request_info): Applies PlayerLogic object to RequestInfo data
#                 function returns:
#                     played_move: int value as per current moves_list value

    @staticmethod
    def check_request_info_type(request_info):
        # Check request_info is of type RequestInfo.
        if not isinstance(request_info, RequestInfo):
            raise TypeError("Input to get_player_input should be of RequestInfo type")


    def __init__(self, play_logic, name='Player', print_request = False):

        super().__init__()
        self.name = name
        self.play_logic = play_logic
        self.print_request = print_request


    def get_name(self):
        return(self.name)



    def get_player_input(self, request_info):
        # Sends the given RequestInfo object to the PlayLogic object to receive the player's next move

        InputMethod.check_request_info_type(request_info)

        if self.print_request:
            print(request_info.get_request_info()['human_string'])

        try:
            return(self.play_logic.get_next_value(request_info))
        except StopIteration:
            print(self.name + ' play logic failed! Aborting')
            return(None)


    def update_state(self, move_summary, hand=[]):
        return self.play_logic.update_state(move_summary, hand=hand)

    def reset_state(self, hand=[], dp_list=[]):
        return self.play_logic.reset_state(hand=hand, dp_list=dp_list)
