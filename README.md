# Cryptocurrency-Trading-Bot

I created a trading bot that runs on the Poloniex Exchange, trading the currency pair of Bitcoin to US Dollars (BTC_USDT). 
For indicators on when to place buy and sell orders, I utilized resistance and support trend lines. Resistance trend lines are lines 
connecting two data points where the price of the commodity does not seem to go over. However, once the price breaks the resistance trend line,
it tends to increase sharply prompting the user to place a sell order. Support trend lines are when the price of the commodity
does not seem to get any lower than a certain point and when it does, decreases rapidly. When this happens, you should place a buy order

While making this bot, there are a few pitfalls to the logic of my trading strategy. First of all, when determining which data points
to use when drawing the resistance trend lines, I used a constant instead of analyzing the data beforehand. When picking the data points,
it is optimal to select two with the closest price. Because the cryptocurrency market is incredibly volatile, the price 
of these currency pairs are bound to change rapidly over a short period of time, rendering the constant useless. Another pitfall is that
this trading strategy is too sensitive to change and will not make you any money. I created this bot to learn more about blockchain
and finance. 









Acknowledgments:

I utilized the code from https://github.com/bwentzloff/trading-bot and tweaked some faulty areas within the Poloniex API and Bot code
while also adding a couple of my own methods. 
