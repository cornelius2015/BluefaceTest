"""cart.py: Shopping Cart functions to create and sum receipts with currency conversion"""

__author__ = "Con Daly"
__copyright__ = "Copyright 2020, Con daly"
__credits__ = ["Blueface"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Con Daly"
__status__ = "Production"

import typing
import json
from datetime import datetime
import logging
from currency_converter import CurrencyConverter
from . import abc

logging.basicConfig(filename='cart.log',level=logging.INFO)

class ShoppingCart(abc.ShoppingCart):
    def __init__(self,product_prices_json_path:str):
        """ Initilaisation constructor
        Parameters:
        product_prices_json_path: Path to JSON file prices
        """
        self._items = dict()
        logging.info(str(datetime.now())+': Shopping Cart Created')
        self._product_prices = None
        self._product_prices_json_path = product_prices_json_path
        self._currency_converter = CurrencyConverter()
        self.get_json_data(self._product_prices_json_path)

    def add_item(self, product_code: str, quantity: int):
        """Adding item to the shopping cart
        Parameters:
        product_code: Item's product code
        quantity: Quantity of items
        """
        if quantity>0:
            if product_code in self._product_prices.keys():
                if product_code not in self._items:
                    self._items[product_code] = quantity
                else:
                    q = self._items[product_code]
                    self._items[product_code] = q + quantity
            else:
                logging.warning(str(datetime.now())+" Product Code: '"+product_code+"' is incorrect.")
        else:
            logging.warning(str(datetime.now())+" Quantity: '" +str(quantity) +"' for product code: '"+product_code+"' is incorrect.")
        
    def print_receipt(self) -> typing.List[str]:
        """Produce the Shopping Cart Receipt with totals in EURO, USD and GBP currencies
        Returns:
        Receipt as a list
        """
        lines = []
        euro_total=0
        usd_total=0
        gbp_total=0

        for item in self._items.items():
            euro_price = self._get_product_price(item[0]) * item[1]
            usd_price = self.get_price_in_currency(euro_price,"USD")
            gbp_price = self.get_price_in_currency(euro_price,"GBP")

            euro_total += euro_price
            usd_total += usd_price
            gbp_total += gbp_price

            euro_price_string = "€%.2f" % euro_price
            usd_price_string = "$%.2f" % usd_price
            gbp_price_string = "£%.2f" % gbp_price
            
            lines.append(item[0] + " - " + str(item[1]) + ' - ' + euro_price_string  + ' - ' + \
                usd_price_string   + ' - ' + gbp_price_string)
        
        euro_total_str="€%.2f" % euro_total
        usd_total_str="$%.2f" % usd_total
        gbp_total_str="£%.2f" % gbp_total

        lines.append("Total = "+euro_total_str+ ' - ' + usd_total_str  + ' - ' + gbp_total_str)
        logging.info(str(datetime.now())+': Receipt =' +str(lines))
        return lines

    def get_json_data(self, json_file:str):
        """Reads the JSON data from the file and stores it in the _product_prices dictionary
        Parameters:
        json_file: Path to the json File
        """
        with open(json_file) as json_data:
            self._product_prices = json.load(json_data)

    def get_price_in_currency(self,price:float,new_currency:str) -> float:
        """Converts the price from Euros to the new currency
        Parameters:
        price: the current price in Euros
        new_currency: the currency to convert to.
        Returns:
        The converted price
        """
        converted_price=0
        try:
            converted_price = self._currency_converter.convert(round(price, 2), 'EUR', new_currency)
        except Exception as inst:
            logging.error(str(datetime.now())+" Currency Converter Exception: "+ str(inst))
        return converted_price

    def _get_product_price(self, product_code: str) -> float:
        """Gets the price for a given product code
        Parameters:
        product_code: The product code
        Returns:
        Price of product
        """
        return float(self._product_prices[product_code])

