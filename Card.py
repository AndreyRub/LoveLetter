class Card:
# Class Card:
# 	properties:
# 		value: int, range: 1..8
# 		description: str, same as in game (for display purposes only)
# 			(implemented in __repr__? I think it's not advisable)
#
# 	Methods:
# 		init: define [value, description] data values

	def __init__(self, value, description):
		self.value = value
		self.description = description

	def __repr__(self):
		return(f"Value: {self.value}. Description: {self.description}")

	def get_value(self):
		return self.value

	def get_description(self):
		return self.description

