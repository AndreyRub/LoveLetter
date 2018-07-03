def get_num_of_cards_in_play(dp_list, hand=[]):
    num_in_play = [0] * (len(dp_list) + 1)
    for k in dp_list.keys():
        num_discarded = dp_list[k][0]
        num_in_deck = dp_list[k][1]
        num_in_play[k] = num_in_deck - num_discarded

    for c in hand:
        num_in_play[c.get_value()] -= 1

    return(num_in_play)


def get_active_cards_list(dp_list, hand=[]):
    cards_in_play_nums = get_num_of_cards_in_play(dp_list, hand)
    cards_in_play_list = []
    for i in range(len(cards_in_play_nums)):
        [cards_in_play_list.append(i) for t in range(cards_in_play_nums[i])]
    return(cards_in_play_list)

def remove_all_cards_from_list(card_list, val):
    new_list = [c for c in card_list if c!=val]

    if len(new_list)==0:
        a=2

    card_list = new_list


def remove_one_card_from_list(card_list, val):
    removed = False
    new_list = []
    for i in range(len(card_list)):
        if not removed and card_list[i]==val:
            removed = True
        else:
            new_list += [card_list[i]]

    if len(new_list)==0:
        a=2

    card_list = new_list