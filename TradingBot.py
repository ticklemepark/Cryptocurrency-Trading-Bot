import getopt, sys
import PoloniexAPI.py as poloniex
import time
import datetime



def main(argv):

    period = 10
    currency_pair = "BTC_USDT"
    prices = []
    start_time = False
    end_time = False
    historical_data = False
    trade_placed = False
    data_date = ""
    order_number = ""
    data_points = []
    local_max = []


    try:
        opts, args = getopt.getopt(argv,"hp : c : s : e : ",["period=","currency="])
    except getopt.GetoptError:
        print ("Bot.py -p <period length> -c <currency pair>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print ("Bot.py -p <period length> -c <currency pair>")
            sys.exit()
        elif opt in ("-p", "--period"):
            if int(arg) in [300,900,1800,7200,14400,86400]:
                period = arg
            else:
                print ("Error: Poloniex requires periods in 300,900,1800,7200,14400, or 86400 second increments")
                sys.exit(2)
        elif opt in ("-c", "--currency"):
            currency_pair = arg
        elif opt in ("-s"):
            start_time = arg
        elif opt in ("-e"):
            end_time = arg


    poloniex = poloniex("API Key goes here", "API Secret goes here")


    if start_time:
		historical_data = poloniex.returnChartData({"currency_pair":pair,"start":startTime,"end":endTime,"period":period})


    while True:
        if start_time and historical_data:
            next_data_point = historical_data.pop(0)
            last_pair_price = next_data_point["weighted_average"]
            data_date = datetime.datetime.fromtimestamp(int(next_data_point["date"])).strftime("%Y-%m-%d %H:%M:%S")
        elif start_time and not historical_data:
            exit()
        else:
            current_values = poloniex.returnTicker
            last_pair_price = current_values[currency_pair]["last"]
            data_date = datetime.datetime.now()



        data_points.append({"date" : data_date, "price" : str(last_pair_price), "trend" : str(current_resistance), "label" : "null", "desc" : "null"})

        if len(data_points) > 2 and (data_points[-2]["price"] > data_points[-1]["price"]) and (data_points[-2]["price"] > data_points[-3]["price"]):           #determines the local maximum
            data_points[-2]["label"] = "MAXIMUM"
            data_points[-2]["desc"] = "Local Maximum"
            number_of_similar_local_maxes = 0
            for old_max in local_max:
                if (float(old_max) > float(data_points[-2]["price"]) - .0001) and (float(old_max) < float(data_points[-2]["price"]) + .0001):          #determines which data points to base the resistance lines on
                    number_of_similar_local_maxes += 1
            if number_of_similar_local_maxes > 2:
                current_resistance = data_points[-2]["price"]
                data_points[-2]["trend"] = data_points[-2]["price"]          #draws the
                data_points[-1]["trend"] = data_points[-2]["price"]          #resistance line
            local_max.append(data_points[-2]["price"])

        else:
            exit()

        if len(local_max) > 0:
            if not trade_placed:
                if data_points[-2]["price"] > current_resistance:
                    print ("BUY ORDER")
                    order_number = poloniex.buy(currency_pair, last_pair_price, 0.1)
                    trade_placed = True
                elif data_points[-2]["price"] < current_resistance:
                    print ("SELL ORDER")
                    order_number = poloniex.sell(currency_pair, last_pair_price, 0.1)
                    trade_placed = True
                else:
                    print ("EXIT TRADE")
                    poloniex.cancel(currency_pair, order_number)
                    trade_placed = False
        else:
            exit()





if __name__ == "__main__":
    main(sys.argv[1:])
