from src.poker.common import *


def get_suit(card):
    return card[-1]


def get_number(card):
    return card[:-1]


def is_ace(card):
    return get_number(card) == '14'


# Unpacks aces (14S, 14H, 14D, 14C) into itself and its dual-cards: (1S, 1H, 1D, 1C)
def unpack_aces(cards):
    return [*cards, *['1' + get_suit(c) for c in cards if is_ace(c)]]


# Undoes the unpack
def repack_aces(cards):
    return ['14' + get_suit(c) if get_number(c) == '1' else c for c in cards]


def has_royal_flush(hand, river):
    return get_royal_flush(hand, river) is not None


def get_royal_flush(hand, river):
    big_hand = [*hand, *river]
    count_suits = {s: 0 for s in suits}
    for c in big_hand:
        count_suits[get_suit(c)] += 1

    max = sorted(count_suits.items(), key=lambda x: x[1], reverse=True)[0]
    if max[1] < 5:
        return None

    suit = max[0]
    big_hand = [c for c in big_hand if get_suit(c) == suit]
    big_hand = sorted(big_hand, key=lambda x: int(get_number(x)), reverse=True)

    numbers = [get_number(c) for c in big_hand]
    if numbers == [cards[-i] for i in range(1, 6)]:
        return big_hand[:5]
    return None


def has_flush(hand, river):
    return get_flush(hand, river) is not None


def get_flush(hand, river):
    big_hand = [*hand, *river]
    count_suits = {s: 0 for s in suits}
    for c in big_hand:
        count_suits[get_suit(c)] += 1

    max = sorted(count_suits.items(), key=lambda x: x[1], reverse=True)[0]
    if max[1] >= 5:
        return sorted([c for c in big_hand if get_suit(c) == max[0]], key=lambda x: int(get_number(x)), reverse=True)[:5]
    return None


def has_straight(hand, river):
    return get_straight(hand, river) is not None


def get_straight(hand, river):
    big_hand = unpack_aces([*hand, *river])
    big_hand = sorted(big_hand, key=lambda x: int(get_number(x)), reverse=True)

    straight = [big_hand[0]]
    for i in range(len(big_hand)):
        if i == 0:
            continue
        diff = int(get_number(big_hand[i])) - int(get_number(big_hand[i - 1]))
        if diff == 0:
            continue
        elif diff == -1:
            straight.append(big_hand[i])
            if len(straight) >= 5:
                return repack_aces(straight[:5])
        else:
            straight = [big_hand[i]]
    return None


def has_straight_flush(hand, river):
    return get_straight_flush(hand, river) is not None


def get_straight_flush(hand, river):
    big_hand = [*hand, *river]

    count_suits = {s: 0 for s in suits}
    for c in big_hand:
        count_suits[get_suit(c)] += 1

    max = sorted(count_suits.items(), key=lambda x: x[1], reverse=True)[0]
    if max[1] < 5:
        return None

    flush = sorted([c for c in big_hand if get_suit(c) == max[0]], key=lambda x: int(get_number(x)), reverse=True)
    flush = unpack_aces(flush)

    straight = [flush[0]]
    for i in range(len(flush)):
        if i == 0:
            continue

        diff = int(get_number(flush[i])) - int(get_number(flush[i - 1]))
        if diff == 0:
            continue
        elif diff == -1:
            straight.append(flush[i])
            if len(straight) >= 5:
                return repack_aces(straight[:5])
        else:
            straight = [flush[i]]
    return None


def has_four_of_a_kind(hand, river):
    return get_four_of_a_kind(hand, river) is not None


def get_four_of_a_kind(hand, river):
    big_hand = [*hand, *river]
    count = {c: 0 for c in cards}

    for c in big_hand:
        count[get_number(c)] += 1

    # Should only be possible to have one four-of-a-kind in a big-hand, since this is 7 cards total.
    # Can order numbers in desc to get highest four-of-a-kind if this assumption changes.
    number = [n for n, c in count.items() if c >= 4]
    if len(number) == 0:
        return None

    return [number[0] + s for s in suits]


def has_full_house(hand, river):
    return get_full_house(hand, river) is not None


def get_full_house(hand, river):
    big_hand = [*hand, *river]
    count = {c: 0 for c in cards}

    for c in big_hand:
        count[get_number(c)] += 1

    # Sort it by count primary, card number secondary
    counts = sorted(count.items(), key=lambda x: (x[1], int(x[0])), reverse=True)
    if not (counts[0][1] >= 3 and counts[1][1] >= 2):
        return None

    house = [c for c in big_hand if get_number(c) == counts[0][0]][:3]
    full_of = [c for c in big_hand if get_number(c) == counts[1][0]][:2]
    return [*house, *full_of]


def has_three_of_a_kind(hand, river):
    return get_three_of_a_kind(hand, river) is not None


def get_three_of_a_kind(hand, river):
    big_hand = [*hand, *river]
    count = {c: 0 for c in cards}

    for c in big_hand:
        count[get_number(c)] += 1

    three_of_a_kind = sorted([n for n, c in count.items() if c >= 3], reverse=True)[0]
    return [*[c for c in big_hand if get_number(c) == three_of_a_kind],
            *sorted([c for c in big_hand if get_number(c) != three_of_a_kind], key=lambda c: int(get_number(c)), reverse=True)[:2]]


def has_two_pair(hand, river):
    return get_two_pair(hand, river) is not None


def get_two_pair(hand, river):
    big_hand = [*hand, *river]
    count = {c: 0 for c in cards}

    for c in big_hand:
        count[get_number(c)] += 1

    # Sort it by count primary, card number secondary
    counts = sorted(count.items(), key=lambda x: (x[1], int(x[0])), reverse=True)
    if not(counts[0][1] >= 2 and counts[1][1] >= 2):
        return None

    return [
        *[c for c in big_hand if get_number(c) == counts[0][0]][:2],
        *[c for c in big_hand if get_number(c) == counts[1][0]][:2],
        sorted([c for c in big_hand if get_number(c) not in {counts[0][0], counts[1][0]}], key=lambda c: int(get_number(c)), reverse=True)[0],
    ]


def has_pair(hand, river):
    return get_pair(hand, river) is not None


def get_pair(hand, river):
    big_hand = [*hand, *river]
    count = {c: 0 for c in cards}

    for c in big_hand:
        count[get_number(c)] += 1

    # Sort it by count primary, card number secondary
    counts = sorted(count.items(), key=lambda x: (x[1], int(x[0])), reverse=True)[0]
    if not counts[1] >= 2:
        return None

    return [
        *[c for c in big_hand if get_number(c) == counts[0]][:2],
        *sorted([c for c in big_hand if get_number(c) != counts[0]],
               key=lambda c: int(get_number(c)), reverse=True)[:3],
    ]


def get_high_card(hand, river):
    big_hand = [*hand, *river]
    return sorted(big_hand, key=lambda c: int(get_number(c)), reverse=True)[:5]


def has_high_card(hand, river):
    return True


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





