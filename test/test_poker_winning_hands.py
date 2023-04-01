import unittest
import src.poker.poker_game as poker


class TestWinningHands(unittest.TestCase):

    def setUp(self) -> None:
        self.hands = [
            ['3H', '3S'],
            ['4H', '4S'],
            ['10S', '11S'],
            ['2D', '14D'],
            ['14C', '14H'],
        ]

    def assert_winner_of_poker_game(self, river, expected):
        self.assertEqual(expected, poker.get_winning_hands(self.hands, river))

    def test_winning_hands(self):
        self.assertEqual(poker.get_winning_hands(
            self.hands[:2],
            ['3D', '4C', '5S', '5C', '14S']
        ), [
            (['4H', '4S'], ['4H', '4S', '4C', '5S', '5C'])
        ])

        self.assert_winner_of_poker_game(
            ['12S', '4C', '5S', '13S', '14S'],
            [
                (['10S', '11S'], ['14S', '13S', '12S', '11S', '10S'])
            ]
        )

        self.assert_winner_of_poker_game(
            ['3D', '4C', '5S', '5C', '14S'],
            [
                (['14C', '14H'], ['14C', '14H', '14S', '5S', '5C'])
            ]
        )

        self.assert_winner_of_poker_game(
            ['12S', '4C', '5S', '13D', '12H'],
            [
                (['4H', '4S'], ['4H', '4S', '4C', '12S', '12H'])
            ]
        )

