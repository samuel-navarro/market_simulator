import constants as cts


class Buyer:
    __MAX_BUY_ATTEMPTS = 3

    def __init__(self, max_price):
        self._max_buy_price = max_price
        self._current_buy_price = self._max_buy_price

    def get_max_price(self):
        return  self._max_buy_price

    def go_to_market(self, market):
        adaption_price = self._max_buy_price
        bought = False
        for i in range(0, self.__MAX_BUY_ATTEMPTS):
            seller = market.lock_one_seller()
            if seller:
                sell_price = seller.get_quotation()
                if sell_price <= self._current_buy_price:
                    seller.sell()
                    adaption_price = sell_price
                    bought = True

                market.release_seller(seller)

            if bought:
                break

        adapted_price = cts.RETENTION_RATE * self._current_buy_price + cts.ADAPTION_RATE * adaption_price
        self._current_buy_price = min(adapted_price, self._max_buy_price)




