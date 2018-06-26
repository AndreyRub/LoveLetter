from InputMethodInterface import InputMethodInterface
from RequestInfo import RequestInfo
class InputHuman(InputMethodInterface):

    def __init__(self, name=''):
        super().__init__()
        self.name = name


    def get_player_input(self, request_info):
        # Human: Prints the human-readable string and prompts the human for input.
        # Overrides parent function.
        # function returns:
        #                 played_move: int value as inputted by human from keyboard

        if not isinstance(request_info,RequestInfo):

            return None  # This is an error - request_info should be of type RequestInfo

        else:

            request_data = request_info.get_request_info()
            user_input = input(request_data['human_string'])
            return(int(user_input))
