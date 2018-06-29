def get_num_of_cards_in_play(dp_list, hand=[]):
    num_in_play = [0] * (len(dp_list) + 1)
    for k in dp_list.keys():
        num_discarded = dp_list[k][0]
        num_in_deck = dp_list[k][1]
        num_in_play[k] = num_in_deck - num_discarded

    for c in hand:
        num_in_play[c.get_value()] -= 1

    return(num_in_play)