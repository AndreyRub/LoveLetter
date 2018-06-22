class Player:

    def __init__(self,name):
        self.cards = []
        self.name = name

    def get_first_card(self, new_card):
        self.cards.append(new_card)

    def play(self,new_card):
        self.cards.append(new_card)
        return self.cards.pop()

    def __repr__(self):
        print(self.cards)
        print(self.name)
