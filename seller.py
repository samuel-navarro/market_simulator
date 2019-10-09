import constants as cts


class Seller:
    def __init__(self, min_price):
        self._min_sell_price = min_price
        self._current_sell_price = min_price
        self._product_available = True

    def is_available(self):
        return self._product_available

    def sell(self):
        self._product_available = False

    def get_quotation(self):
        return self._current_sell_price

    def get_min_price(self):
        return self._min_sell_price

    def refill(self):
        is_product_sold = not self._product_available
        if is_product_sold:
            adaption_price = self._current_sell_price * 2
        else:
            adaption_price = self._min_sell_price

        adapted_price = cts.RETENTION_RATE * self._current_sell_price + cts.ADAPTION_RATE * adaption_price
        self._current_sell_price = max(adapted_price, self._min_sell_price)
        self._product_available = True

