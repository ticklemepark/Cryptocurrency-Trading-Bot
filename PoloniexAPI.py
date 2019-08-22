import urllib
import urllib2
import json
import time
import os
import hmac, hashlib


class Exchange:
    """Poloniex Exchange API"""

    def __init__(self):
        self.API_KEY = os.environ("POLONIEX_API_KEY")
        self.API_SECRET = os.environ("POLONIEX_API_SECRET")

    def private_method(self, command, req = {}):
        if command = "buy" or command = "sell" or command = "cancel":
            req["command"] = query
            req["nonce"] = int(time.time()*1000)
            post_data = urllib.urlencode(body)
            sign = hmac.new(self.Secret, post_data, hashlib.sha512).hexdigest()
            headers = {
                "Sign": sign,
                "Key": self.APIKey
            }
            ret = urllib2.urlopen(urllib2.Request("https://poloniex.com/tradingApi", post_data, headers))
            jsonRet = json.loads(ret.read())
            return self.post_process(jsonRet)




    def returnTicker(self, command):
        ret = urllib2.urlopen(urllib2.Request("https://poloniex.com/public?command=" + query))
        return json.loads(ret.read())

    def returnChartData(self, req = {}):
        ret= urllib2.urlopen(urllib2.Request("https://poloniex.com/public?command=returnChartData&currencyPair=" + str(req["currencyPair"]) + "&start=" + str(req["start"]) + "&end=" + str(req["end"]) + "&period=" + str(req["period"])))
        return json.loads(ret.read())

    def buy(self, currencyPair, rate, amount):
        return self.main_query("buy",{"currencyPair":currencyPair,"rate":rate,"amount":amount})

    def sell(self,currencyPair, rate, amount):
        return self.main_query("sell",{"currencyPair":currencyPair,"rate":rate,"amount":amount})

    def cancel(self, currencyPair, orderNumber):
         return self.main_query("cancelOrder",{"currencyPair":currencyPair,"orderNumber":orderNumber})
