class Player:

    def __init__(self,card):
        self.last_card = card
        self.new_card = None

    def play(self,new_card):
        self.new_card = new_card

    def __repr__(self):
        print("%d,%d" %(self.last_card,self.new_card))
