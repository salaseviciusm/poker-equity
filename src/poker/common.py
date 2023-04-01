import re

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
suits = ['S', 'D', 'H', 'C']

card_mapping = {
    'A': cards[-1],
    'K': cards[-2],
    'Q': cards[-3],
    'J': cards[-4],
    'T': cards[-5],
    **{str(i): str(i) for i in range(2, 10)}
}


def decode_hand(hand, deck):
    cards = re.match(r'^[CSDHAJQKT2-9]+', hand).group()
    in_suit = re.match(r'[oi]$', hand)

    decoded = re.match('[2-9]{1,2}[CSDH]')

    if in_suit is not None:
        in_suit = in_suit.group()

