import src.poker.poker_game as poker


# Returns the multiple of the pot that your hand wins at a randomly generated game,
# where there are currently {table_cards} cards on the table, and {num_other_players} of
# other players at the table
def monte_carlo(hand, table_cards, other_players):
    deck = poker.generate_deck()
    for c in hand:
        deck.remove(c)

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


def calculate_equity_vs_range(hand, table_cards, vs_range, iterations):
    multiples = []
    for v in vs_range:
        multiples = [*multiples, *[monte_carlo(hand, table_cards, [v]) for _ in range(int(iterations/len(vs_range)))]]

    return f"{sum(multiples)/len(multiples):.1%}"