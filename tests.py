import unittest
import data_parser


class TestDataParser(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.parser = data_parser.DataParser()

    def test_get_id(self):
        self.assertEqual(self.parser._get_id("btc"), 1)
        self.assertEqual(self.parser._get_id("111"), None)

    def test_get_price(self):
        self.assertIsInstance(self.parser._get_fiat_price("USD", "BTC"), float)
        self.assertIsInstance(self.parser._get_fiat_price("usd", "ltc"), float)
        self.assertIsInstance(self.parser.convert_to_fiat("USD", "eth", 5), float)
        self.assertIsInstance(self.parser.convert_to_fiat("eur", "eth", 5), float)


if __name__ == '__main__':
    unittest.main()
