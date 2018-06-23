import Deck, Player

class Game:
# Class Game

# 	properties:
# 		deck:			current deck
# 		*valid_moves:	a list with valid moves for current player (e.g. [3,4], or [6]).
# 						Note: this still allows useless / sacrificing moves (e.g. playing a 1 when all players have a 4, or playing the 8 and losing the round). It only serves to avoid playing 5/6 when having the 7.
# 		protection:		list of True/False per each player. Set to True if player is currently protected by a 4
# 		discard_pile:	list of all discarded cards
# 		players:		list of player object in current game
# 		player_status:	list of Booleans for each player status in the game: True: active, False: inactive (out of the round)
		


# 	methods:
# 		init:					init the deck, init all players, give each 1 card. Init discard pile. Input: number of players + names (optional)
# 		play:					runs the main game loop until a winner is declared. Returns winner index
# 		draw_card:				draw a card from the deck. Returns False if deck is depleted
# 		give_player_card: 		draw a card from the deck and add it to a player's hand.
# 		add_to_discard_pile:  	add a card to the discard pile
# 		show_discard_pile:		generate a list of how many cards have been discarded so far
# 		do_player_turn:			draw a card and give it to a player, show user both cards + discard pile, ask for input, check validity, run card logic
# 									Note: if deck is empty, draw_card will return false and decide_winner should be called
# 		run_card:				run card logic. Make sure to check for protection. E.g. card==1, prompt for non-protected targets and guesses card value. 					If all targets are protected, do nothing. Compare guess to card value. If matched, remove player from the game.
# 									Also: check if princess was forced to be discarded when running 5's logic
# 		decide_winner:			returns winner from all remaining players (highest card value wins). Returns a list, in case of a draw
	
	def get_player_name(index):
		return("Player " + str(index))

	def get_validity(hand):
		if hand[0].get_value()==7:
			if hand[1].get_value() in [5,6]: # [7,5] or [7,6] requires playing the 7
				return([True,False])
		if hand[1].get_value()==7:
			if hand[0].get_value() in [5,6]: # [5,7] or [6,7] requires playing the 7
				return([False,True])
		return([True, True])

	def get_validity_prompt(hand):
		validity = get_validity(hand)
		if all(validity)
			prompt = f"Note: you may any card. Your choice: "
		else:
			prompt = f"Note: you may only play card {validity.index(True)+1} (i.e. you must play the 7). Your choice: "
		return prompt


	def __init__(self, num_of_players, names=None):
		# init:			init the deck, init all players, give each 1 card. Input: number of players + names (optional)
		self.num_of_players = num_of_players

		# Get player names / set them to defaults ("Player 1", "Player 2", etc.)
		if not names:
			self.player_names = [get_player_name(idx) for idx in range(1,1+num_of_players)]
		else:
			self.player_names = names

		# Init all players
		self.players = [Player(n) for n in self.player_names]

		# Init the deck
		self.deck = Deck()

		# Init discard pile
		self.discard_pile = []

		# Give each player a card
		[self.give_player_card(self,p) for p in self.players] # Q: are the first 2 "self"s necessary?
						# REMOVE THIS:
						# [p.add_card(self.draw_card(self)) for p in self.players] # Q: are the first 2 "self"s necessary?
						# for p in self.players:
						# 	card = self.deck.deal_card()
						# 	p.add_card(card)


	def draw_card(self):
		# draw_card:		draw a card from the deck. Returns False if deck is depleted
		return self.deck.deal_card()

	def give_player_card(self,player):
		# give_player_card: draw a card from the deck and add it to a player's hand.
		card = self.draw_card(self)
		return player.add_card(card)

	def add_to_discard_pile(self,card):
		# add_to_discard_pile:  add a card to the discard pile
		self.discard_pile.append(card)

	def show_discard_pile(self):
		# show_discard_pile:	generate a list of how many cards have been discarded so far of each card type

		dp_verbose = dict(self.deck.descriptions,[0]*len(self.deck.descriptions))
		for card in self.discard_pile:
			dp_verbose[card.get_description()]+=1
		print(dp_verbose)
		return(dp_verbose)

# 		play:					runs the main game loop until a winner is declared. Returns winner index
# 		do_player_turn:			draw a card and give it to a player, show user both cards + discard pile, ask for input, check validity, run card logic
# 									Note: if deck is empty, draw_card will return false and decide_winner should be called
# 		run_card:				run card logic. Make sure to check for protection. E.g. card==1, prompt for non-protected targets and guesses card value.
# 								If all targets are protected, do nothing. Compare guess to card value. If matched, remove player from the game.
# 									Also: check if princess was forced to be discarded when running 5's logic
# 		decide_winner:			returns winner from all remaining players (highest card value wins). Returns a list, in case of a draw

	def prompt_player_for_input(self,player):
		name = player.show_name()
		hand = player.show_hand()
		prompt = f"{name}, this is your hand:\n1:{hand[0].get_description()}\n2:{hand[1].get_description()}\nChoose your card to play.\n"
		validity_prompt = get_validity_prompt(hand)
		return(prompt+validity_prompt)

	def do_player_turn(self,player):
# 		do_player_turn:			draw a card and give it to a player, show user both cards + discard pile, ask for input, check validity, run card logic
# 									Note: if deck is empty, draw_card will return false and decide_winner should be called
		self.give_player_card(self,player)
