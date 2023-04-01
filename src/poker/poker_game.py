from src.poker.common import *
import random
import src.poker.poker_hands as poker


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
