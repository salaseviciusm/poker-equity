import unittest
import src.poker_hands as poker


class TestHands(unittest.TestCase):

    def test_has_royal_flush(self):
        self.assertTrue(poker.has_royal_flush(['10H', '14H'], ['11H', '5S', '13H', '3D', '12H']))

    def test_has_royal_flush_false(self):
        self.assertFalse(poker.has_royal_flush(['10H', '14H'], ['11H', '5S', '13C', '3D', '12H']))
        self.assertFalse(poker.has_royal_flush(['9H', '10H'], ['11H', '5S', '13H', '3D', '12H']))

    def test_has_straight(self):
        self.assertTrue(poker.has_straight(['10H', '14H'], ['11H', '5S', '13H', '3D', '12H']))
        self.assertTrue(poker.has_straight(['9H', '10H'], ['11H', '5S', '13H', '3D', '12H']))
        self.assertTrue(poker.has_straight(['6H', '7D'], ['5H', '4H', '3H', '3D', '12H']))
        self.assertTrue(poker.has_straight(['6H', '7D'], ['5H', '4H', '3H', '4D', '6H']))

    def test_has_straight_false(self):
        self.assertFalse(poker.has_straight(['9H', '10H'], ['11H', '5S', '7H', '3D', '12H']))

    def test_has_straight_flush(self):
        self.assertTrue(poker.has_straight_flush(['9H', '10H'], ['11H', '5S', '13H', '3D', '12H']))
        self.assertFalse(poker.has_straight_flush(['6H', '7D'], ['5H', '4H', '3H', '3D', '12H']))

    def test_has_flush(self):
        self.assertTrue(poker.has_flush(['6H', '7D'], ['5H', '4H', '3H', '3D', '12H']))

    def test_get_flush(self):
        self.assertEqual(poker.get_flush(['9H', '10H'], ['11H', '5S', '13H', '3D', '12H']),
                          ['13H', '12H', '11H', '10H', '9H'])
        self.assertEqual(poker.get_flush(['4H', '10H'], ['11H', '9H', '13H', '3D', '12H']),
                          ['13H', '12H', '11H', '10H', '9H'])
        self.assertIsNone(poker.get_flush(['4H', '10D'], ['11H', '9H', '13H', '3D', '12S']))

    def test_get_straight_flush(self):
        self.assertEqual(poker.get_straight_flush(['9H', '10H'], ['11H', '5S', '13H', '3D', '12H']),
                          ['13H', '12H', '11H', '10H', '9H'])
        self.assertEqual(poker.get_straight_flush(['13H', '4H'], ['3H', '2H', '5H', '6H', '12H']),
                          ['6H', '5H', '4H', '3H', '2H'])

    def test_ace_straights(self):
        self.assertEqual(poker.get_straight(['14H', '13H'], ['12H', '11H', '10H', '6H', '3S']),
                          ['14H', '13H', '12H', '11H', '10H'])
        self.assertEqual(poker.get_straight(['14H', '2H'], ['3H', '11H', '4H', '5H', '3S']),
                         ['5H', '4H', '3H', '2H', '14H'])
        self.assertEqual(poker.get_straight_flush(['14H', '2H'], ['3H', '11H', '4H', '5H', '3S']),
                         ['5H', '4H', '3H', '2H', '14H'])
        self.assertIsNone(poker.get_straight_flush(['14H', '2S'], ['3H', '11H', '4D', '5H', '3S']))

    def test_get_four_of_a_kind(self):
        self.assertEqual(set(poker.get_four_of_a_kind(['14H', '14S'], ['12S', '14D', '14C', '12H', '12C'])),
                         {'14H', '14C', '14D', '14S'})

    def test_get_full_house(self):
        self.assertEqual(poker.get_full_house(['14H', '14S'], ['12S', '12H', '14C', '12H', '13D']),
                         ['14H', '14S', '14C', '12S', '12H'])
        self.assertEqual(poker.get_full_house(['5H', '5S'], ['5D', '3S', '3C', '3H', '13D']),
                         ['5H', '5S', '5D', '3S', '3C'])
        self.assertEqual(poker.get_full_house(['5H', '7D'], ['5D', '3S', '3C', '3H', '13D']),
                         ['3S', '3C', '3H', '5H', '5D'])

    def test_three_of_a_kind(self):
        self.assertEqual(poker.get_three_of_a_kind(['14H', '14S'], ['14D', '13S', '13H', '13C']),
                         ['14H', '14S', '14D', '13S', '13H'])
        self.assertEqual(poker.get_three_of_a_kind(['12H', '11S'], ['14D', '13S', '13H', '13C']),
                         ['13S', '13H', '13C', '14D', '12H'])

    def test_get_two_pair(self):
        self.assertEqual(poker.get_two_pair(['14H', '12S'], ['6H', '13S', '12H', '14S', '7C']),
                         ['14H', '14S', '12S', '12H', '13S'])
        self.assertEqual(poker.get_two_pair(['6H', '12S'], ['6H', '13S', '12H', '14S', '14C']),
                         ['14S', '14C', '12S', '12H', '13S'])

    def test_get_pair(self):
        self.assertEqual(poker.get_pair(['6H', '6S'], ['2S', '3S', '3H', '5C', '7D']),
                         ['6H', '6S', '7D', '5C', '3S'])
