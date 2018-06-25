import random
from Card import Card
class Deck:
# Class Deck:
# 	properties:
# 		cards: 	list of Card objects.
# 				order determines next card to draw
# 		num_of_unused_cards: int. Defines the deck size which causes the game to end (equivalent to setting aside 1 card or more)
#
#
# 	methods:
# 		init: 	create Values and descriptions as in game (5 "1"s, 2 "2","3","4","5"s, 1 "6","7","8", etc.)
# 				shuffle the cards list (using shuffle() method)
# 				set num_of_unused_cards to 1
# 		deck_size:	returns number of remaining playable cards (i.e. not including the card(s) set aside)
# 		is_empty:	returns True if number of cards remaining is equal to num_of_unused cards
# 		shuffle:	shuffles the "cards" list
# 		deal_card:	pop one card from the deck and return it.

    def get_num_of_cards_per_type(self):
        num_of_cards_per_type = {
            1: 5, 2: 2, 3: 2, 4: 2, 5: 2, 6: 1, 7: 1, 8: 1
        }
        return num_of_cards_per_type

    def get_descriptions(self,cards_style="Japanese"):
        if cards_style=="Japanese":
            names = ['Guard','Courtier','Diplomat','Shugenja','Hatamoto','Manipulator','Sensei','Princess']
        elif cards_style=="Batman":
            names = ['Batman','Catwoman','Bane','Robin','Poison Ivy','Two Face','Harley Quinn','Joker']
        elif cards_style=="Classic":
            names = ['Guard','Priest','Baron','Handmaiden','Prince','King','Countess','Princess']
        elif cards_style=="Coup":
            names = ['Guard', 'Captain', 'Duke', 'Ambassador', 'Inquisitor', 'Captain', 'Contessa', 'Princess']
        num_of_cards_per_type = self.get_num_of_cards_per_type()
        descriptions = [
                    '%s(%d) - Guess a player\'s hand' % (names[0],num_of_cards_per_type[1]) ,
                    '%s(%d) - Look at a hand' % (names[1],num_of_cards_per_type[2]),
                    '%s(%d) - Compare hands' % (names[2],num_of_cards_per_type[3]),
                    '%s(%d) - Protection until your next turn' % (names[3],num_of_cards_per_type[4]),
                    '%s(%d) - One player discards his or her hand' % (names[4],num_of_cards_per_type[5]),
                    '%s(%d) - Trade hands' % (names[5],num_of_cards_per_type[6]),
                    '%s(%d) - Discard if caught with %s or %s' % (names[6],num_of_cards_per_type[7],names[4],names[5]),
                    '%s(%d) - Lose if discarded' % (names[7],num_of_cards_per_type[8])]
        return descriptions

    def __init__(self, num_of_unused_cards=1,cards_style = "Japanese"):
        self.num_of_unused_cards = num_of_unused_cards
        # Create cards as per the game (5 "1"s, 2 "2","3","4","5"s, 1 "6","7","8", etc.)
        num_of_cards_per_type = self.get_num_of_cards_per_type()
        descriptions = self.get_descriptions(cards_style)
        cards = []
        for card_type in sorted(num_of_cards_per_type):
            num_of_cards = num_of_cards_per_type[card_type]
            for j in range(0,num_of_cards):
                cards.append( Card(card_type,descriptions[card_type-1]) )

        self.descriptions = descriptions
        self.cards = cards

        self.shuffle()

    def shuffle(self):
        # Shuffles the deck. Consider adding a check to only allow this when the deck is full
        random.shuffle(self.cards)

    def deck_size(self):
        # deck_size:	returns number of remaining playable cards (i.e. not including the card(s) set aside)
        return(len(self.cards) - self.num_of_unused_cards)

    def is_empty(self):
        # is_empty:	returns True if number of cards remaining is equal to num_of_unused cards
        return(self.deck_size() == 0)

    def deal_card(self):
        # deal_card:	pop one card from the deck and return it. If deck is empty, return False
        if self.is_empty():
            return(False)
        return(self.cards.pop())

    def show_descriptions(self):
        return('\n'.join([str(i+1) + " - " + self.descriptions[i] for i in range(len(self.descriptions))]))



