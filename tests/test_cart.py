"""test_cart.py: Test cases for cart.py."""

__author__ = "Con Daly"
__copyright__ = "Copyright 2020, Con daly"
__credits__ = ["Blueface"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Con Daly"
__status__ = "Production"


import unittest
import sys
import typing
sys.path.append('../')
from shoppingcart.cart import ShoppingCart


prices_json_path="../shoppingcart/product_prices.json"
class TestShoppingCart(unittest.TestCase):
    

    def test_add_item(self):
        cart = ShoppingCart(prices_json_path)
        cart.add_item("apple", 1)
        receipt = cart.print_receipt()
        self.assertEqual(receipt[0],"apple - 1 - €1.00 - $%.2f - £%.2f" % (cart.get_price_in_currency(1.00, "USD"), cart.get_price_in_currency(1.00, "GBP")))


    def test_add_item_with_multiple_quantity(self):
        cart = ShoppingCart(prices_json_path)
        cart.add_item("apple", 2)

        receipt = cart.print_receipt()
        self.assertEqual(receipt[0],"apple - 2 - €2.00 - $%.2f - £%.2f" % (cart.get_price_in_currency(2.00, "USD"), cart.get_price_in_currency(2.00, "GBP")))


    def test_add_different_items(self):
        cart = ShoppingCart(prices_json_path)
        cart.add_item("orange",2)
        cart.add_item("banana", 1)
        cart.add_item("pineapple", 3)
        cart.add_item("kiwi", 1)
        receipt = cart.print_receipt()

        self.assertEqual(receipt[0],"orange - 2 - €6.00 - $%.2f - £%.2f" % (cart.get_price_in_currency(6.00, "USD"), cart.get_price_in_currency(6.00, "GBP")))
        self.assertEqual(receipt[1],"banana - 1 - €1.10 - $%.2f - £%.2f" % (cart.get_price_in_currency(1.10, "USD"), cart.get_price_in_currency(1.10, "GBP")))
        self.assertEqual(receipt[2],"pineapple - 3 - €3.00 - $%.2f - £%.2f" % (cart.get_price_in_currency(3.00, "USD"), cart.get_price_in_currency(3.00, "GBP")))
        self.assertEqual(receipt[3],"kiwi - 1 - €3.00 - $%.2f - £%.2f" % (cart.get_price_in_currency(3.00, "USD"), cart.get_price_in_currency(3.00, "GBP")))
        self.assertEqual(receipt[4],"Total = €13.10 - $%.2f - £%.2f" % (cart.get_price_in_currency(13.10, "USD"), cart.get_price_in_currency(13.10, "GBP")))

    def test_add_incorrect_product_code(self):
        cart = ShoppingCart(prices_json_path)
        cart.add_item("orangeX",2)
        cart.add_item("banana", 1)
        cart.add_item("pineapple", 3)
        cart.add_item("kiwi", 1)
        receipt = cart.print_receipt()

        self.assertEqual(receipt[0],"banana - 1 - €1.10 - $%.2f - £%.2f" % (cart.get_price_in_currency(1.10, "USD"), cart.get_price_in_currency(1.10, "GBP")))
        self.assertEqual(receipt[1],"pineapple - 3 - €3.00 - $%.2f - £%.2f" % (cart.get_price_in_currency(3.00, "USD"), cart.get_price_in_currency(3.00, "GBP")))
        self.assertEqual(receipt[2],"kiwi - 1 - €3.00 - $%.2f - £%.2f" % (cart.get_price_in_currency(3.00, "USD"), cart.get_price_in_currency(3.00, "GBP")))
        self.assertEqual(receipt[3],"Total = €7.10 - $%.2f - £%.2f" % (cart.get_price_in_currency(7.10, "USD"), cart.get_price_in_currency(7.10, "GBP")))
    
    def test_add_incorrect_quantity_code(self):
        cart = ShoppingCart(prices_json_path)
        cart.add_item("pineapple", -3)
        cart.add_item("kiwi", 1)
        receipt = cart.print_receipt()

        self.assertEqual(receipt[0],"kiwi - 1 - €3.00 - $%.2f - £%.2f" % (cart.get_price_in_currency(3.00, "USD"), cart.get_price_in_currency(3.00, "GBP")))
        self.assertEqual(receipt[1],"Total = €3.00 - $%.2f - £%.2f" % (cart.get_price_in_currency(3.00, "USD"), cart.get_price_in_currency(3.00, "GBP")))

    def test_add_same_item_twice_code(self):
        cart = ShoppingCart(prices_json_path)
        cart.add_item("pineapple", 1)
        cart.add_item("pineapple", 1)
        receipt = cart.print_receipt()
        #print(receipt)

        self.assertEqual(receipt[0],"pineapple - 2 - €2.00 - $%.2f - £%.2f" % (cart.get_price_in_currency(2.00, "USD"), cart.get_price_in_currency(2.00, "GBP")))
        self.assertEqual(receipt[1],"Total = €2.00 - $%.2f - £%.2f" % (cart.get_price_in_currency(2.00, "USD"), cart.get_price_in_currency(2.00, "GBP")))

    def test_get_price_in_currency_exception(self):
        cart = ShoppingCart(prices_json_path)
        result = cart.get_price_in_currency(2.00, "US")
        self.assertEqual(result,0)

#if __name__ == '__main__':
#    unittest.main()