import matplotlib.pyplot as plt
import numpy as np

from market import Market

__MIN_SELL_PRICE = 10
__MAX_SELL_PRICE = 100


def _get_histogram_bins():
    return np.linspace(__MIN_SELL_PRICE, __MAX_SELL_PRICE, 50)


def _get_demand_curve(market):
    demand_prices = [buyer.get_max_price() for buyer in market.get_buyers()]
    histogram, bins = np.histogram(demand_prices, _get_histogram_bins())
    return list(np.cumsum(histogram))


def _get_supply_curve(market):
    supply_prices = [seller.get_min_price() for seller in market.get_sellers()]
    histogram, bins = np.histogram(supply_prices, _get_histogram_bins())
    return list(reversed(np.cumsum(histogram)))


if __name__ == '__main__':
    MARKET_DAYS = 200
    market = Market(n_buyers=100, n_sellers=90, min_sell_price=__MIN_SELL_PRICE, max_sell_price=__MAX_SELL_PRICE)

    max_prices = list()
    min_prices = list()
    avg_prices = list()

    for day in range(0, MARKET_DAYS):
        market.run_market_day()
        transaction_prices = [seller.get_quotation() for seller in market.get_sellers() if not seller.is_available()]
        market.close_market_day()

        if len(transaction_prices) > 0:
            max_prices.append(max(transaction_prices))
            min_prices.append(min(transaction_prices))
            avg_prices.append(sum(transaction_prices) / len(transaction_prices))

    if len(max_prices) > 0:
        plt.plot(max_prices)
        plt.plot(min_prices)
        plt.plot(avg_prices)
    else:
        print('Too bad! No transactions this year')

    prices = _get_histogram_bins()[:-1]
    supply_quantities = _get_supply_curve(market)
    demand_quantities = _get_demand_curve(market)

    plt.figure()
    plt.plot(supply_quantities, prices)
    plt.plot(demand_quantities, prices)
    plt.show()
