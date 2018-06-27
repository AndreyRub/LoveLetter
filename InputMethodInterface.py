from RequestInfo import RequestInfo
import abc

class InputMethodInterface:
    def __init__(self):
        self.name = ''

    @abc.abstractmethod
    def get_player_input(self, request_info):
        return None # Not implemented here, will be implemented in child functions

    @staticmethod
    def check_request_info_type(request_info):
        # Check request_info is of type RequestInfo.
        if not isinstance(request_info, RequestInfo):
            raise TypeError("Input to get_player_input should be of RequestInfo type")


    def get_name(self):
        return(self.name)