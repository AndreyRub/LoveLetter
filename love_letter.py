from Game import Game

num_of_players = 4

game = Game(num_of_players)
winners = game.play()
if len(winners) == 1:
    print(f"And the winner is: {winners[0].show_name()}!")
else:
    strs = ", ".join([w.get_name() for w in winners])
    print(f"And the winners are: {strs}!")
