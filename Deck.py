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

    def get_descriptions(self,cards_style="Japanese"):
        if cards_style=="Japanese":
            names = ['Guard','Courtier','Diplomat','Shugenja','Hatamoto','Manipulator','Sensei','Princess']
        elif cards_style=="Batman":
            names = ['Batman','Catwoman','Bane','Robin','Poison Ivy','Two Face','Harley Quinn','Joker']
        elif cards_style=="Classic":
            names = ['Guard','Priest','Baron','Handmaiden','Prince','King','Countess','Pricess']
        descriptions = [
                    '%s(5) - Guess a player\'s hand' % names[0],
                    '%s(2) - Look at a hand' % names[1],
                    '%s(2) - Compare hands' % names[2],
                    '%s(2) - Protection until your next turn' % names[3],
                    '%s(2) - One player discards his or her hand' % names[4],
                    '%s(1) - Trade hands' % names[5],
                    '%s(1) - Discard if caught with %s or %s' % (names[6],names[4],names[5]),
                    '%s(1) - Lose if discarded' %names[7]]


        return descriptions

    def __init__(self, num_of_unused_cards=1,cards_style = "Japanese"):
        self.num_of_unused_cards = num_of_unused_cards

        # Create cards as per the game (5 "1"s, 2 "2","3","4","5"s, 1 "6","7","8", etc.)
        descriptions = self.get_descriptions(cards_style)
        cards =[Card(1,descriptions[0]),
                Card(1,descriptions[0]),
                Card(1,descriptions[0]),
                Card(1,descriptions[0]),
                Card(1,descriptions[0]),
                Card(2,descriptions[1]),
                Card(2,descriptions[1]),
                Card(3,descriptions[2]),
                Card(3,descriptions[2]),
                Card(4,descriptions[3]),
                Card(4,descriptions[3]),
                Card(5,descriptions[4]),
                Card(5,descriptions[4]),
                Card(6,descriptions[5]),
                Card(7,descriptions[6]),
                Card(8,descriptions[7]),
                ]

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



