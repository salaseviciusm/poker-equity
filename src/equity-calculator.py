import random

import src.poker.poker_game as poker


# Returns the multiple of the pot that your hand wins at a randomly generated game,
# where there are currently {table_cards} cards on the table, and {num_other_players} of
# other players at the table
def monte_carlo(deck, hand, table_cards, other_players):
    hands = [
        hand,
        *poker.generate_hands(deck, len([p for p in other_players if len(p) == 0])),
        *[p for p in other_players if len(p) != 0]
    ]

    river = None
    if len(table_cards) == 3:
        river = poker.generate_river(deck, poker.generate_turn(deck, table_cards))
    if len(table_cards) == 4:
        river = poker.generate_river(deck, table_cards)
    elif len(table_cards) == 0:
        river = poker.generate_river(deck, poker.generate_turn(deck, poker.generate_flop(deck)))

    assert river is not None

    winning_hands = poker.get_winning_hands(hands, river)
    if hand in [h[0] for h in winning_hands]:
        return 1/len(winning_hands)

    return 0


def calculate_equity(hand, table_cards, num_other_players, iterations):
    multiples = [monte_carlo(hand, table_cards, [[] for _ in range(num_other_players)]) for _ in range(iterations)]

    return f"{sum(multiples)/len(multiples):.1%}"


def calculate_equity_vs(hand, table_cards, other_players, num_other_players, iterations):
    multiples = [monte_carlo(hand, table_cards, [*other_players, *[[] for _ in range(num_other_players - len(other_players))]]) for _ in range(iterations)]

    return f"{sum(multiples)/len(multiples):.1%}"

import re


def decode_hand(hand, deck):
    cards = re.match(r'^[AJQKT2-9]+', hand).group()
    in_suit = re.match(r'[oi]$', hand)

    cards = [poker.card_mapping[cards[i]] for i in range(2)]
    chosen_cards = []
    if in_suit is None:
        for i in range(2):
            choices = [dc for dc in deck if poker.get_number(dc) == cards[i]]
            choice = random.choice(choices)
            deck.remove(choice)
            chosen_cards.append(choice)
    else:
        in_suit = in_suit.group()
        if in_suit == 'o':
            choices = [dc for dc in deck if poker.get_number(dc) == cards[0]]
            first_choice = random.choice(choices)
            deck.remove(first_choice)
            chosen_cards.append(first_choice)

            choices = [dc for dc in deck if poker.get_number(dc) == cards[1] and poker.get_suit(dc) != poker.get_suit(first_choice)]
            second_choice = random.choice(choices)
            deck.remove(second_choice)
            chosen_cards.append(second_choice)
        else:
            choices = [dc for dc in deck if poker.get_number(dc) == cards[0]]
            first_choice = random.choice(choices)
            deck.remove(first_choice)
            chosen_cards.append(first_choice)

            choices = [dc for dc in deck if
                       poker.get_number(dc) == cards[1] and poker.get_suit(dc) == poker.get_suit(first_choice)]
            second_choice = random.choice(choices)
            deck.remove(second_choice)
            chosen_cards.append(second_choice)

    return chosen_cards


def calculate_equity_vs_range(hand, table_cards, vs_range, iterations):
    multiples = []
    for i in range(int(iterations/max(len(vs_range), 1))):
        deck = poker.generate_deck()
        dhand = decode_hand(hand, deck)

        if len(vs_range) == 0:
            multiples.append(monte_carlo(deck, dhand, table_cards, [[], [], [], [], [], [], [], []]))
            continue

        for v in vs_range:
            deck_copy = [*deck]
            dv = decode_hand(v, deck_copy)
            multiples.append(monte_carlo(deck_copy, dhand, table_cards, [dv]))

    return f"{sum(multiples)/len(multiples):.1%}"


# print(calculate_equity_vs_range('AKo', [], ['KK', 'AK', 'AA'], 100_000))
