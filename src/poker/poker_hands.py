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






