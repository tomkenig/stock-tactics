"""
pip install mysql-connector-python
pip install pandas
pip install numpy
"""
# libs
from db_works import db_connect, db_tables
import pandas as pd

db_schema_name, db_table_name, db_settings_table_name = db_tables()
cursor, cnxn = db_connect()


# todo: combination table. Can be stored in other schema
def get_combination(interval_param_):
    db_schema_name, db_table_name, db_settings_table_name = db_tables()
    cursor, cnxn = db_connect()
    print("todo")


market = "BTCUSDT"
tick_interval = "1mo"
data_granulation = "klines"
stock_type = "spot"
stock_exchange = "Binance.com"

def get_ohlc_data(interval_param_):
    print("done")


x = cursor.execute("SELECT * FROM m1174_stock_dwh.vw_binance_klines_anl where market = '"+market+"' and "
                                                                                                 "tick_interval = '" + tick_interval + "' and "
                                                                                                 "data_granulation = '"+ data_granulation + "' and "
                                                                                                 "stock_type = '" + stock_type + "' and "
                                                                                                 "stock_exchange = '" + stock_exchange + "' ")


df = pd.DataFrame(cursor.fetchall())

print(df)