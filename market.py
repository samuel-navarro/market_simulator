import threading
import random

from buyer import Buyer
from seller import Seller


def _send_buyer_to_market(buyer, market):
    buyer.go_to_market(market)


class Market:
    def __init__(self, n_buyers, n_sellers, min_sell_price, max_sell_price):
        self._sellers_lock = threading.Lock()

        self._buyers = [Buyer(random.uniform(min_sell_price, max_sell_price)) for i in range(0, n_buyers)]
        self._sellers = [Seller(random.uniform(min_sell_price, max_sell_price)) for i in range(0, n_sellers)]
        self._locked_sellers = set()

    def _get_buyer_thread(self, buyer):
        return threading.Thread(target=_send_buyer_to_market, args=(buyer, self,))

    def run_market_day(self):
        buyer_threads = [self._get_buyer_thread(buyer) for buyer in self._buyers]
        for thread in buyer_threads:
            thread.start()
        for thread in buyer_threads:
            thread.join()

    def close_market_day(self):
        while self._locked_sellers:
            self._locked_sellers.pop()

        for seller in self._sellers:
            seller.refill()

    def get_buyers(self):
        return self._buyers

    def get_sellers(self):
        return self._sellers

    def lock_one_seller(self):
        with self._sellers_lock:
            available_sellers = [seller for seller in self._sellers
                                 if seller.is_available() and (seller not in self._locked_sellers)]
            if len(available_sellers) == 0:
                return None
            else:
                seller = random.choice(available_sellers)
                self._locked_sellers.add(seller)
                return seller

    def release_seller(self, seller):
        with self._sellers_lock:
            if seller in self._locked_sellers:
                self._locked_sellers.remove(seller)
