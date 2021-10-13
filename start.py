# todo: update and lock records
# todo: zero-devide error in data frame
"""
pip install mysql-connector-python
pip install pandas
pip install numpy
"""
# libs
# import datetime
from db_works import db_connect, db_tables
import pandas as pd
import numpy as np
import pandas_ta as pta  # https://mrjbq7.github.io/ta-lib/
import talib as ta  # install from whl file < https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
from hashlib import md5
import json
import time

db_schema_name, db_table_name, db_settings_table_name = db_tables()
cursor, cnxn = db_connect()

TACTICS_PACK_SIZE = 5000

# create session identifier with md5
#app_session = md5(str(datetime.datetime.utcnow()).encode("ascii")).hexdigest()
#print(app_session)
#time.sleep(3)


# todo: not need to use all params. just use download_settings_id
# todo: combination table. Can be stored in other schema
def get_combination():
    cursor.execute("SELECT download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange FROM " + db_schema_name + ".vw_tactics_tests_to_analyse where tick_interval <> '15m' and tactic_status_id = 0 limit 1")
    download_setting = cursor.fetchall()
    if len(download_setting) > 0:
        download_settings_id = download_setting[0][0]
        market = download_setting[0][1]
        tick_interval = download_setting[0][2]
        data_granulation = download_setting[0][3]
        stock_type = download_setting[0][4]
        stock_exchange = download_setting[0][5]
        print("select done")
    else:
        print("no data to download")
        exit()
    return download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange

download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange = get_combination()

print(download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange)

# download OHLC data from DWH
def get_ohlc_data():
    cursor.execute("SELECT * FROM " + db_schema_name + ".vw_binance_klines_anl where market = '"+market+"' and "
                                                                                                     "tick_interval = '" + tick_interval + "' and "
                                                                                                     "data_granulation = '"+ data_granulation + "' and "
                                                                                                     "stock_type = '" + stock_type + "' and "
                                                                                                     "stock_exchange = '" + stock_exchange + "' ")
    df = pd.DataFrame(cursor.fetchall())
    df_bak = df.copy()  # absolutly needed. Simple assignment doesn't work
    print("data ready")
    return df, df_bak

df, df_bak = get_ohlc_data()

print(df)


def get_tactics_to_check():
    cursor.execute("SELECT tactic_id, download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value, yield_expected, wait_periods "
                   "FROM " + db_schema_name + ".vw_tactics_tests_to_analyse where tactic_status_id = 0 and download_settings_id = "+ str(download_settings_id) + " limit " + str(TACTICS_PACK_SIZE) +" ")
    tactics_data = cursor.fetchall()
    return tactics_data

tactics_data = get_tactics_to_check()


def get_test_result(test_stake_in, test_indicator_buy_1_in, test_indicator_value_1_in, test_yield_expect_in, test_wait_periods_in):
    df.columns =["open_time",
                 "open",
                 "high",
                 "low",
                 "close",
                 "volume",
                 "close_time",
                 "quote_asset_volume",
                 "number_of_trades",
                 "taker_buy_base_asset_volume",
                 "taker_buy_quote_asset_volume",
                 "ignore",
                 "market",
                 "tick_interval",
                 "data_granulation",
                 "stock_type",
                 "stock_exchange",
                 "insert_timestamp",
                 "open_datetime",
                 "close_datetime"]


    # basics
    df["open_time_dt"] = pd.to_datetime(df["open_datetime"], unit='ms')
    df["open_time_yr"] = df["open_time_dt"].dt.year
    df["open_time_mnt"] = df["open_time_dt"].dt.month
    df["open_time_dy"] = df["open_time_dt"].dt.day

    df["change_val"] = df.close - df.open
    df["change_perc"] = df.close / df.open - 1
    df["amplitude_val"] = df.high - df.low
    df["amplitude_perc"] = df.high - df.low / df.open
    df["up_down"] = np.where(df["close"] - df["close"].shift(1) > 0, 1, -1)

    # token: trend up/down 1 / -1
    # definition: in custom period sums of change are up or down.
    # you an combine it with ADX - trend strength by multiply both ie. -1 * 40
    df["token_change_7"] = df["change_val"].rolling(7).sum()
    df["token_trend_7"] = np.where(df["token_change_7"] > 0, 1, -1)
    df["token_change_14"] = df["change_val"].rolling(14).sum() # oryginal
    df["token_trend_14"] = np.where(df["token_change_14"] > 0, 1, -1)
    df["token_change_50"] = df["change_val"].rolling(50).sum()
    df["token_trend_50"] = np.where(df["token_change_50"] > 0, 1, -1)
    df["token_change_100"] = df["change_val"].rolling(100).sum()
    df["token_trend_100"] = np.where(df["token_change_100"] > 0, 1, -1)

    # indicators
    # Moving averages
    df["sma_7"] = pta.sma(df["close"], length=7)
    df["sma_25"] = pta.sma(df["close"], length=25)
    df["sma_99"] = pta.sma(df["close"], length=99)

    df["wma_7"] = pta.wma(df["close"], length=7)
    df["wma_25"] = pta.wma(df["close"], length=25)
    df["wma_99"] = pta.wma(df["close"], length=99)

    df["ema_7"] = pta.ema(df["close"], length=7)
    df["ema_25"] = pta.ema(df["close"], length=25)
    df["ema_99"] = pta.ema(df["close"], length=99)

    # MACD's


    # oscilators
    # RSI
    df["rsi_6"] = ta.RSI(df["close"], timeperiod=6) # tradingview corr, ok, checked
    df["rsi_10"] = ta.RSI(df["close"], timeperiod=10) # tradingview corr, ok, checked
    df["rsi_12"] = ta.RSI(df["close"], timeperiod=12) # tradingview corr, ok, checked
    df["rsi_14"] = ta.RSI(df["close"], timeperiod=14) # tradingview corr, ok, checked
    df["rsi_20"] = ta.RSI(df["close"], timeperiod=20) # tradingview corr, ok, checked
    df["rsi_24"] = ta.RSI(df["close"], timeperiod=24) # tradingview corr, ok, checked

    # Williams %R
    df["will_perc_r_6"] = pta.willr(df["high"], df["low"], df["close"], 6) #
    df["will_perc_r_10"] = pta.willr(df["high"], df["low"], df["close"], 10) # tradingview corr #williams default
    df["will_perc_r_14"] = pta.willr(df["high"], df["low"], df["close"], 14) # tradingview corr

    # CCI
    df["cci_14"] = pta.willr(df["high"], df["low"], df["close"], 14) # tradingview corr ------------------------------this isn't cci, < willr function

    # ROC - rate of change
    df["roc_5"] = pta.roc(df["close"], 5)  # trandingview, ok, checked
    df["roc_6"] = pta.roc(df["close"], 6)  # trandingview, ok, checked
    df["roc_9"] = pta.roc(df["close"], 9)  # trandingview, ok, checked
    df["roc_10"] = pta.roc(df["close"], 10)  # trandingview typical, ok, checked
    df["roc_12"] = pta.roc(df["close"], 12)  # trandingview typical, ok, checked
    df["roc_14"] = pta.roc(df["close"], 14)  # trandingview typical, ok, checked
    df["roc_24"] = pta.roc(df["close"], 24)  # trandingview typical, ok, checked

    # MFI - money flow index
    df["mfi_7"] = pta.mfi(df["high"], df["low"], df["close"], df["volume"])  # trandingview, ok, checked
    df["mfi_14"] = pta.mfi(df["high"], df["low"], df["close"], df["volume"])  # trandingview, ok, checked

    # stoch - stochastic oscilator
    df["stoch_slowk_5_3"], df["stoch_slowd_5_3"] = ta.STOCH(df["high"], df["low"], df["close"])  # ta-lib standard
    df["stoch_fastk_5_3"], df["stoch_fastd_5_3"] = ta.STOCHF(df["high"], df["low"], df["close"])  # ta-lib standard

    df["stoch_slowk_14_3"], df["stoch_slowd_14_3"] = ta.STOCH(df["high"], df["low"], df["close"])
    df["stoch_fastk_14_3"], df["stoch_fastd_14_3"] = ta.STOCHF(df["high"], df["low"], df["close"], fastk_period=14)  # tradingview ok, checked



    # StochRSI
    #df["stoch_rsi"] = pta.sto

    # ADX Average directional movement index
    df["adx_7"] = ta.ADX(df["high"], df["low"], df["close"], timeperiod=7)
    df["adx_14"] = ta.ADX(df["high"], df["low"], df["close"]) # standard
    df["adx_50"] = ta.ADX(df["high"], df["low"], df["close"], timeperiod=50)
    df["adx_100"] = ta.ADX(df["high"], df["low"], df["close"], timeperiod=100)


    df["adxr_14"] = ta.ADXR(df["high"], df["low"], df["close"]) # standard



    # token mod: Trend strength index
    df["token_tsi_14"] = df["token_trend_14"] * df["adx_14"]


    # volume indicators
    # OBV - On Balance Volume
    df["obv"] = pta.obv(df["close"], df["volume"])

    # candles

    df["cdl_doji"] = pta.cdl_doji(df["open"], df["high"], df["low"], df["close"])
    df["cdl_dragonfly_doji"] = ta.CDLDRAGONFLYDOJI(df["open"], df["high"], df["low"], df["close"])
    df["cdl_hammer"] = ta.CDLHAMMER(df["open"], df["high"], df["low"], df["close"])
    df["cdl_marubozu"] = ta.CDLMARUBOZU(df["open"], df["high"], df["low"], df["close"])
    df["cdl_longline"] = ta.CDLLONGLINE(df["open"], df["high"], df["low"], df["close"])
    df["cdl_longlinedoji"] = ta.CDLLONGLEGGEDDOJI(df["open"], df["high"], df["low"], df["close"])
    df["cdl_takuri"] = ta.CDLTAKURI(df["open"], df["high"], df["low"], df["close"])
    df["cdl_3white_soldiers"] = ta.CDL3WHITESOLDIERS(df["open"], df["high"], df["low"], df["close"])


    # combined token
    # RSI rise 1 period
    #df["rsi_6_rise_1_period"] = np.where(df["rsi_6"] > df["rsi_6"].shift(1), 1, 0)

    # MFI raise 1 period
    #df["mfi_7_rise_1_period"] = np.where(df["mfi_7"] > df["mfi_7"].shift(1), 1, 0)

    # volume twice, two green after red
    df["volume_twice_two_green_after_red"] = np.where((df["up_down"] == 1)
                                                      & (df["up_down"].shift(1) == 1)
                                                      & (df["up_down"].shift(2) == 0)
                                                      & (df["volume"] / df["volume"].shift(1) >= 1.2), 1, 0)

    # TESTS strategies
    # TESTS strategies
    # TESTS strategies


    # print(df)


    test_stake = int(test_stake_in)
    test_indicator_buy_1 = test_indicator_buy_1_in
    #test_indicator_buy_2 = "token_trend_50"
    #test_indicator_buy_3 = "token_trend_100"
    #test_indicator_buy_4 = "adx_7"
    test_indicator_value_1 = test_indicator_value_1_in
    #test_indicator_value_2 = 1
    #test_indicator_value_3 = 1
    #test_indicator_value_4 = 40
    test_yield_expect = test_yield_expect_in  # ie. 0.01=1%
    test_wait_periods = test_wait_periods_in  # ie. try to sell in next 6 periods (or 10)
    test_stoploss = -0.05  # must be minus
    test_stock_fee = -0.002  # must be minus

    df["tst_is_buy_signal"] = np.where((df[test_indicator_buy_1] < test_indicator_value_1)
    #                                   & (df[test_indicator_buy_2] < test_indicator_value_2)
    #                                   & (df[test_indicator_buy_3] < test_indicator_value_3)
    #                                   & (df[test_indicator_buy_4] > test_indicator_value_4)
                                       , 1, 0)

    df["tst_sell_price"] = df["close"] * test_yield_expect + df["close"]
    df["tst_sell_stoploss_price"] = df["close"] + df["close"] * test_stoploss # must be plus
    df["tst_high_in_sell_period"] = df["high"].rolling(test_wait_periods).max().shift(-test_wait_periods)
    df["tst_low_in_sell_period"] = df["low"].rolling(test_wait_periods).min().shift(-test_wait_periods)
    df["tst_sell_after_yield"] = np.where(df['tst_high_in_sell_period'] >= df["tst_sell_price"], 1, 0)
    df["tst_sell_after_stoploss"] = np.where(df['tst_low_in_sell_period'] <= df["tst_sell_stoploss_price"], 1, 0)
    df["tst_sold_price"] = np.where(df['tst_sell_after_yield'] == 1, df["tst_sell_price"], df["close"].shift(-1 * test_wait_periods)) # market after time
    df["tst_sold_diff_perc"] = df["tst_sold_price"] / df["close"]
    df["tst_single_game_result"] = np.where(df['tst_sold_diff_perc'] > 1, 1, -1)
    df["tst_buy_sell_fee"] = test_stake * test_stock_fee # todo: change later, but accuracy is good
    df["tst_single_game_earn"] = test_stake * df["tst_sold_diff_perc"] - test_stake
    df["tst_single_game_earn_minus_fees"] = (test_stake * df["tst_sold_diff_perc"] - test_stake) + df["tst_buy_sell_fee"]
    # todo: single game result with stoploss. Need improvement
    df["tst_single_game_earn_minus_fees_with_stoploss"] = np.where(df['tst_sell_after_stoploss'] == 1 , test_stake * test_stoploss + df["tst_buy_sell_fee"], df["tst_single_game_earn_minus_fees"])


    # test_name = "tst_" & market & "_" & tick_interval & "_" & test_indicator_buy_1

    # print(df.info(verbose=True))

    # last check
    #print(df)

    # df2 aggr
    df2 = df[df["tst_is_buy_signal"] == 1].groupby(["open_time_yr", "open_time_mnt"]).\
        aggregate({"tst_is_buy_signal": "sum",
                   #"tst_single_game_earn": "sum",
                   "tst_single_game_earn_minus_fees": "sum"
                   #"tst_single_game_earn_minus_fees_with_stoploss": "sum"
                   })
    df2['earn_sign'] = np.sign(df2["tst_single_game_earn_minus_fees"])
    # print(df2)


    df3 = df[df["tst_is_buy_signal"] == 1].groupby(["open_time_yr"]).\
        aggregate({"tst_is_buy_signal": "sum",
                   #"tst_single_game_earn": "sum",
                   "tst_single_game_earn_minus_fees": "sum"
                   #"tst_single_game_earn_minus_fees_with_stoploss": "sum"
                   })
    df3['earn_sign'] = np.sign(df3["tst_single_game_earn_minus_fees"])
    # print(df3)

    # statistics

    df4 = df[df["tst_is_buy_signal"] == 1].aggregate({"tst_is_buy_signal": "sum",
                   #"tst_single_game_earn": "sum",
                   "tst_single_game_earn_minus_fees": "sum"
                   #"tst_single_game_earn_minus_fees_with_stoploss": "sum"
                   })


    # print(df4)

    # jsons with results
    result_string_1 = pd.DataFrame.to_json(df2)
    result_string_2 = pd.DataFrame.to_json(df3)
    result_string_3 = pd.DataFrame.to_json(df4)
    score_1 = df4["tst_is_buy_signal"]
    score_2 = df4["tst_single_game_earn_minus_fees"]
    score_3 = df2["earn_sign"].sum() / df2["earn_sign"].count()
    score_4 = df3["earn_sign"].sum() / df3["earn_sign"].count()


    return result_string_1, result_string_2, result_string_3, score_1, score_2, score_3, score_4

print("main loop:")
print(len(tactics_data)-1)
###################################################### LICZBA NIE ELEMENT
for i in range(len(tactics_data)-1): # in tactics_data:
    #print(i)
    #i = 1
    result_string_1, result_string_2, result_string_3, score_1, score_2, score_3, score_4 = get_test_result(int(tactics_data[i][2]), tactics_data[i][3], tactics_data[i][4], tactics_data[i][5], tactics_data[i][6])
    print(result_string_1, result_string_2, result_string_3, score_1, score_2, score_3, score_4)



    # update - test status done
    cursor.execute("UPDATE " + db_schema_name + ".tactics_tests SET tactic_status_id = 2 where tactic_id = " + str(tactics_data[i][0]) + " ")
    print("update done")
    cnxn.commit()

    # insert results if results are good enough
    if score_2 >= 100:
        cursor.execute(
            "INSERT INTO " + db_schema_name + ".tactics_tests_results (download_settings_id, tactic_id, result_string_1, result_string_2, result_string_3, score_1, score_2, score_3, score_4)  values "
                                              "(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (
            download_settings_id, str(tactics_data[i][0]), result_string_1, result_string_2, result_string_3, str(int(score_1)), str(int(score_2)), str(score_3), str(score_4)))

    print("insert done or not")
    df = df_bak.copy()  # absolutly needed. Simple assignment doesn't work in pandas
    print(df)
    cnxn.commit()


