from cryptocmd import CmcScraper
import pandas as pd
import datetime


def ScrapeCoinMarketCap():
    coins = pd.read_excel(open("D:\Projects\CrytoCurrency\CryptoTrading\ListOfCryptoCurrencies.xlsx", 'rb'))
    return coins['Symbol']


def GetAllCoinData(day_to_buy):
    coins = ScrapeCoinMarketCap()
    all_coin_data = []
    for coin in coins[:20]:
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
    day_data = coin_data[coin_data['Date'] == buy_date]
    day_data = day_data.sort_values(by=['percentChange'], ascending=False)
    print day_data


def main():
    day_to_buy = 'Monday'
    start_date = datetime.date(2015,8,10)
    end_date = datetime.date(2018,7,23)
    all_coin_data = GetAllCoinData(day_to_buy)



    dates = pd.DataFrame(pd.date_range(start_date, end_date), columns={'date'})
    dates['day_of_week'] = pd.to_datetime(dates['date']).dt.weekday_name
    filtered_dates = dates[dates["day_of_week"] == day_to_buy]
    single_date = start_date
    while single_date < end_date:
        print single_date
        CoinsWithLargestMomentum(single_date, all_coin_data)
        single_date = single_date + datetime.timedelta(days=7)

main()




