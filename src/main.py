from cryptocmd import CmcScraper
import pandas as pd
import datetime
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

def ScrapeCoinMarketCap():
    coins = pd.read_excel(open("D:\Projects\CrytoCurrency\CryptoTrading\ListOfCryptoCurrencies.xlsx", 'rb'))
    return coins['Symbol']


def GetAllCoinData(day_to_buy):
    coins = ScrapeCoinMarketCap()
    all_coin_data = []
    for coin in coins[:100]:
        df = CmcScraper(coin).get_dataframe()
        df['day_of_week'] = pd.to_datetime(df['Date']).dt.weekday_name
        df['symbol'] = coin
        df['prior_date_close'] = df['Close**'].shift(-7)
        df['percentChange'] = df['Close**'] / df['Close**'].shift(-7) - 1.0
        df = df.drop(labels={'Open*', 'High','Low','Volume'}, axis=1)
        df = df[df['day_of_week'] == day_to_buy]
        all_coin_data.append(df)
    appended_data = pd.concat(all_coin_data, axis=0)
    return appended_data


def CoinsWithLargestMomentum(buy_date, coin_data):
    day_data = coin_data[coin_data['Date'] == pd.Timestamp(buy_date)]
    day_data = day_data[day_data['Market Cap'] != '']
    day_data = day_data.sort_values(by=['percentChange'], ascending=False)[:5]
    day_data = day_data[day_data['percentChange'] > 0.00]
    return day_data


def GetTotalMarketCap(coins):
    market_caps = map(long, coins['Market Cap'].values)
    return sum(market_caps)


def BuyCoin(date, coin, balance_sheet, total_market_cap):
    coin_market_cap = float(coin['Market Cap'])
    coin_performance = float(coin['percentChange'])
    amount_to_buy = coin_market_cap / total_market_cap * balance_sheet
    ownership = pd.DataFrame(data={'date': pd.Timestamp(date), 'symbol': [coin['symbol']], 'balance_sheet': amount_to_buy, 'prior_performance': coin_performance})
    return ownership


def purchase_coins(date, money, all_coin_data):
    coins_owned = []
    top_performers = CoinsWithLargestMomentum(date, all_coin_data)
    total_market_cap = GetTotalMarketCap(top_performers)
    for index, ind_coin in top_performers.iterrows():
        coins_owned.append(BuyCoin(date, ind_coin, money, total_market_cap))
    return pd.concat(coins_owned, axis=0)


def balance_sheet_update(coinsHeld, sell_date, all_coin_data):
    new_balance_sheet = 0.0
    coin_holdings = coinsHeld['symbol'].values.tolist()

    all_coins_sell_date = all_coin_data[all_coin_data['Date'] == pd.Timestamp(sell_date)]
    current_coin_data = all_coins_sell_date[all_coins_sell_date['symbol'].isin(coin_holdings)]
    for index, ind_coin in current_coin_data.iterrows():
        ind_coin_percent_ownership = ind_coin['percentChange']
        ind_coin_balance_sheet = coinsHeld[coinsHeld['symbol'] == ind_coin['symbol']]['balance_sheet'][0] # Returns your balance sheet capital for the specific coin
        new_balance_sheet += ((1.0 + ind_coin_percent_ownership) * ind_coin_balance_sheet)
    return new_balance_sheet


def main():
    day_to_buy = 'Monday'
    starting_money = 1000.0
    start_date = datetime.date(2017,1,2)
    end_date = datetime.date(2017,12,25)
    all_coin_data = GetAllCoinData(day_to_buy)

    transaction_date = start_date + datetime.timedelta(days=7)

    coin_ownership = purchase_coins(start_date, starting_money, all_coin_data)
    print coin_ownership
    money = starting_money
    while transaction_date <= end_date:
        money = balance_sheet_update(coin_ownership, transaction_date, all_coin_data)

        coin_ownership = purchase_coins(transaction_date, money, all_coin_data)

        print coin_ownership
        #print money

        transaction_date = transaction_date + datetime.timedelta(days=7)

main()




