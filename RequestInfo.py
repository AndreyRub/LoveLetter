class RequestInfo:
    def __init__(self,
                 human_string,                      # human-readable string (will be printed for Human object)
                 action_requested,                  # action requested ('card' + index of card / 'opponent' / 'guess')
                 current_hand = [],                 # player's current hand
                 discard_pile = [],                 # discard pile
                 move_history = [],                 # list of player moves
                 players_active_status = [],        # players' active status (active / lost)
                 players_protection_status = [],    # players' protection status (protected / not protected)
                 invalid_moves = [],                # invalid moves (optional) - an assist from Game
                 valid_moves = [],                  # valid moves (optional) - an assist from Game
                 players_active = [],               # list of currently active players
                 players_protected = []):           # Protection status of all players (including inactive ones)

        self.human_string               = human_string
        self.action_requested           = action_requested
        self.current_hand               = current_hand
        self.discard_pile               = discard_pile
        self.move_history               = move_history
        self.players_active_status      = players_active_status
        self.players_protection_status  = players_protection_status
        self.invalid_moves              = invalid_moves
        self.valid_moves                = valid_moves
        self.players_active             = players_active
        self.players_protected          = players_protected

    def get_request_info(self):
        return ({'human_string'              : self.human_string,
				 'action_requested'          : self.action_requested,
				 'current_hand'              : self.current_hand,
				 'discard_pile'              : self.discard_pile,
				 'move_history'              : self.move_history,
				 'players_active_status'     : self.players_active_status,
				 'players_protection_status' : self.players_protection_status,
				 'invalid_moves'             : self.invalid_moves,
                 'valid_moves'               : self.valid_moves,
                 'players_active'            : self.players_active,
                 'players_protected'         : self.players_protected})






