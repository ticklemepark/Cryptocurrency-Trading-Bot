import time
import PoloniexAPI.py as poloniex
import BittrexAPI.py as bittrex


class ArbitrageBot:

    def __init__(self, currencypair):
        self.currencypair = currencypair
        self.feeRatioBittrex = 0.0025
        self.feeRatioPoloniex = 0.001
        self.coins = [currencypair[i:i+3] for i in range(0, len(currencypair), 3)]
        self.coinA = coins[0]
        self.coinB = coins[1]
        self.profit = 0.05

    def findorderbook(self):
        plx_order_book = poloniex.returnOrderBook
        btx_order_book = bittrex.get_market_summary
        bestAskPlx = [float(plx_order_book["ask"][-1][0])]
        bestBidPlx = [float(plx_order_book["buy"][-1][0])]
        bestAskBtx = [float(btx_order_book["ask"][0]]
        bestBidBtx = [float(btx_order_book)["buy"][0]]

    def balance(self):
        btxBalanceA = bittrex.get_balance("coinA")
        btxBalanceB = bittrex.get_balance("coinB")
        plxBalanceA = poloniex.returnBalances("coinA")
        plxBalanceB = poloniex.returnBalances("coinB")

    def max_amount(self, bid, ask, scenario):
        amount = 0
        #buy from Bittrex, sell to Poloniex
        if scenario == 1:
            maxCoinA = btxBalanceA / ((1 + self.feeRatioBittrex) * ask[0])
            maxCoinB = plxBalanceB / ((1 + self.feeRatioPoloniex) * bid[0])
            amount = min(maxCoinA, maxCoinb, ask[1], bid[1])
        #buy from Poloniex, sell to Bittrex
        elif scenario == 2:
            maxCoinA = plxBalanceA / ((1 + self.feeRatioPoloniex) * ask[0])
            maxCoinB = btxBalanceB / ((1 + self.feeRatioBittrex) * bid[0])
            amount = min(maxCoinA, maxCoinB, ask[1], bid[1])
        return amount

    def scenarios(self):
        scenario1 = best_bid_plx - best_ask_btx
        scenario2 = best_bid_btx - best_ask_plx
        if scenario1 > 0:
            maxAmount = max_amount(plx_order_book[0], btx_order_book[1], 1)
            fee = self.feeRatioPoloniex * maxAmount * best_bid_plx + self.feeRatioBittrex * maxAmount * best_ask_btx
            if abs(scenario1) * maxAmount - fee > self.profit:
                return {"scenario": 1, "ask": best_ask_btx, "bid": best_bid_plx, "amount": maxAmount}
            else:
                return {"scenario": 0}
        elif scenario2 > 0:
            maxAmount = max_amount(btx_order_book[0], plx_order_book[1], 2)
            fee = self.feeRatioPoloniex * maxAmount * best_ask_plx + self.feeRatioBittrex * maxAmount * best_bid_btx
            if abs(scenario2) * maxAmount - fee > self.profit:
                return {"scenario" : 2, "ask": best_ask_plx, "bid": best_bid_btx, "amount": maxAmount}
            else:
                return {"scenario": 0}
        elif scenario1 > 0 and scenario2 > 0:
            if abs(scenario1) > abs(scenario2):
                pass
            elif abs(scenario1) < abs(scenario2):
                pass
        elif scenario < 0 and scenario < 0:
            if abs(scenario1) < abs(scenario2):
                pass
            elif abs(scenario1) > abs(scenario2):
                pass
