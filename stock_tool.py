#stock_tool.py - Excercise 3
#Author: Maxine Coimin

class StockLookup:
    """ This is a tool that only knows how much stock is available for each product """

    def __init__(self, stock):
        """Store the stock this tool can look up."""
        self.stock = stock

    def find_product(self, text):
        """Return the first known product name mentioned in text, or None."""
        for product in self.stock:
            if product in text.lower():
                return product
        return None

    def total_stock(self, product):
        """Return the stock of named product, or None if unknown product."""
        if product in self.stock:
            return self.stock[product]
        return None