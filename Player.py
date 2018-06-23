import random
class Player:
"""
Class Player

    properties:
        name:   defaults to "Player 1/2/3/..." but can be input by users
        hand:   list of Card objects. Can be of length 1 (out-of-turn) or 2 (during turn)
        *valid_move:    list of boolean values, length 2. Describes whether each card in hand (hand has 2 cards during the player's turn) can be played
                    Note: this still allows useless / sacrificing moves (e.g. playing a 1 when all players have a 4, or playing the 8 and losing the round). It only serves to avoid playing 5/6 when having the 7.

    methods:
        
        show_hand:      show the Game object the player's current card(s)
                        When hand size is 1: it will be checked against a player playing 1, shown to another player playing 2, or compared with a player playing 3
                        When hand size is 2: it will be shown to Game object to ensure move is valid
        play_card:      discards one card from 2-card hand (given an input index)
        discard_card:   return current card and discard it
        add_card:       add a card to current hand
"""
    def __init__(self, name='Player'+str(random.randint(10000,99999))):
        # init:           just initialize the name and hand data members
        self.hand = []
        self.name = name

    def __repr__(self):
        print(self.hand)
        print(self.name)


    def add_card(self, new_card):
        # add_card:       add a card to current hand. Check that hand size is not over 2
        if len(self.hand)>1:
            print('ERROR: Attempting to increase player\'s hand over 2. Returning card to caller...')
            return(new_card)
        self.hand.append(new_card)


    def play_card(self,index=0):
        # play_card:      discards one card from hand (given an input index, relevant only for 2-card hand) and return it to caller
        if len(self.hand)>=1: 
            return(self.hand.pop(index))
        else:
            print('ERROR: Attempting to discard from an empty hand. Returning None to caller...')
            return(None)


    def discard_card(self):
         # discard_card:   return current card and discard it
       return(self.play_card(self,0))


    def show_hand(self):
        # show_hand:      show the caller the player's current card(s)
        #                 When hand size is 1: it will be checked against a player playing 1, shown to another player playing 2, or compared with a player playing 3
        #                 When hand size is 2: it will be shown to Game object to ensure move is valid
        return(self.hand)

    def show_name(self):
        return(self.name)




# COMMENTED OUT (redundant)

    # def get_first_card(self, new_card):
    #     self.hand.append(new_card)

    # def play(self,new_card):
    #     self.hand.append(new_card)
    #     return self.hand.pop()

