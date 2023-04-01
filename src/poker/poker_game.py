import random
from src.poker.poker_hands import *


def generate_deck():
    deck = [c + s for c in cards for s in suits]
    return deck


def take_card(deck):
    card = random.choice(deck)
    deck.remove(card)
    return card


def generate_hands(deck, num_players):
    return [(take_card(deck), take_card(deck)) for _ in range(num_players)]


def generate_flop(deck):
    return [take_card(deck) for _ in range(3)]


def generate_turn(deck, flop):
    return [*flop, take_card(deck)]


def generate_river(deck, turn):
    return [*turn, take_card(deck)]


def generate_game(players):
    deck = generate_deck()
    hands = generate_hands(deck, players)
    river = generate_river(deck, generate_turn(deck, generate_flop(deck)))

    return hands, river


def _get_list_of_winning_hand_tuples(hands, river, function):
    return [(hands[i], f) for i, f in enumerate([function(h, river) for h in hands]) if f is not None]


# Filters a list of winning hand tuples for the highest hand(s) possible.
# Assumes that the first card of a big hand is the highest in priority to check
def _get_highest_by_number(winning_tuples):
    highest = sorted(winning_tuples, key=lambda x: int(get_number(x[1][0])), reverse=True)
    best = highest[0]
    return [f for f in winning_tuples if get_number(f[1][0]) == get_number(best[1][0])]


# Returns a list where each element is a tuple containing the original winning hand and the winning big hand
def get_winning_hands(hands, river):

    royal_flushes = _get_list_of_winning_hand_tuples(hands, river, get_royal_flush)
    if len(royal_flushes) >= 1:
        return royal_flushes

    four_of_a_kinds = _get_list_of_winning_hand_tuples(hands, river, get_four_of_a_kind)
    if len(four_of_a_kinds) >= 1:
        return _get_highest_by_number(four_of_a_kinds)

    straight_flushes = _get_list_of_winning_hand_tuples(hands, river, get_straight_flush)
    if len(straight_flushes) >= 1:
        return _get_highest_by_number(straight_flushes)

    full_houses = _get_list_of_winning_hand_tuples(hands, river, get_full_house)
    if len(full_houses) >= 1:
        # Sort full houses by the number of the first 3 primarily, then the number of the last 2 cards secondarily
        highest = sorted(full_houses, key=lambda x: (int(get_number(x[1][0])), int(get_number(x[1][3]))), reverse=True)
        best = highest[0]
        return [f for f in full_houses if get_number(f[1][0]) == get_number(best[1][0]) and get_number(f[1][3]) == get_number(best[1][3])]

    flushes = _get_list_of_winning_hand_tuples(hands, river, get_flush)
    if len(flushes) >= 1:
        highest = sorted(flushes, key=lambda x: tuple(int(get_number(x[1][i])) for i in range(len(x[1]))), reverse=True)
        best = highest[0]
        # All cards in the big-hand have to match the best big-hand
        return [f for f in flushes if str(f[1]) == str(best[1])]

    straights = _get_list_of_winning_hand_tuples(hands, river, get_straight)
    if len(straights) >= 1:
        highest = sorted(straights, key=lambda x: tuple(int(get_number(x[1][i])) for i in range(len(x[1]))), reverse=True)
        best = highest[0]
        # All cards in the big-hand have to match the best big-hand
        return [f for f in flushes if str(f[1]) == str(best[1])]

    three_of_a_kinds = _get_list_of_winning_hand_tuples(hands, river, get_three_of_a_kind)
    if len(three_of_a_kinds) >= 1:
        highest = sorted(three_of_a_kinds, key=lambda x: (x[1][0], *tuple(int(get_number(x[1][i])) for i in range(3, len(x[1])))), reverse=True)
        best = highest[0]
        return [f for f in three_of_a_kinds if get_number(f[1][0]) == get_number(best[1][0]) and str(f[1][3:]) == str(best[1][3:])]

    two_pairs = _get_list_of_winning_hand_tuples(hands, river, get_two_pair)
    if len(two_pairs) >= 1:
        highest = sorted(two_pairs, key=lambda x: (int(get_number(x[1][0])), int(get_number(x[1][2]), int(get_number(x[1][5])))), reverse=True)
        best = highest[0]
        return [f for f in two_pairs if str(f[1]) == str(best[1])]

    pairs = _get_list_of_winning_hand_tuples(hands, river, get_pair)
    if len(pairs) >= 1:
        highest = sorted(pairs, key=lambda x: (int(get_number(x[1][0])), *tuple(int(get_number(x[1][i])) for i in range(2, len(x[1])))), reverse=True)
        best = highest[0]
        return [f for f in pairs if str(f[1]) == str(best[1])]

    high_cards = _get_list_of_winning_hand_tuples(hands, river, get_high_card)
    highest = sorted(high_cards, key=lambda x: tuple(int(get_number(x[1][i])) for i in range(len(x[1]))), reverse=True)
    best = highest[0]
    # All cards in the big-hand have to match the best big-hand
    return [f for f in flushes if str(f[1]) == str(best[1])]
