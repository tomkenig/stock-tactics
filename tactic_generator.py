# libs
from db_works import db_connect, db_tables
import itertools
# tactics_categories
tactic_category_name = "RSI first tests"
tactic_category_priority = 0

# configs
db_schema_name, db_table_name, db_settings_table_name = db_tables()
cursor, cnxn = db_connect()




# tastics_for_tests RSI


download_settings_id = [2, 3, 4, 5, 6, 7, 10, 11]
test_stake = [100]
buy_indicator_1_name = ["rsi_6", "rsi_10", "rsi_12", "rsi_14", "rsi_20", "rsi_24"]
buy_indicator_1_value = [0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
# sell_indicator_1_name
# sell_indicator_1_value
yield_expected = [0.3, 0.4, 0.5, 0.7, 0.8, 1, 1.2, 1.35, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20, 25, 30, 35, 40, 45, 50]
wait_periods = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 25, 40, 45, 50, 60, 70, 80, 90, 100]

x = []
somelists = [download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value, yield_expected, wait_periods ]
for element in itertools.product(*somelists):
    x.append(element)
    # print(element)

for y in x:
    cursor.execute("INSERT INTO " + db_schema_name + ".tactics_tests (download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value,"
                                          "yield_expected, wait_periods, stock_fee, tactic_status_id, tactic_category_id)  values "
                                          "(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (y[0], y[1], y[2], y[3], y[4], y[5], 0.0015, 0, 1))

print("insert done")
cnxn.commit()

################################################ive made faillure buy_indicator_1_value -2 not 2
#INSERT DATA AGAIN
#BUT THIS IS SIGNAL, THAT  + VALUES OF INDICATOR MAKE SENSE
# tastics_for_tests ROC
download_settings_id = [2, 3, 4, 5, 6, 7, 10, 11]
test_stake = [100]
buy_indicator_1_name = ["roc_5", "roc_6", "roc_9", "roc_10", "roc_12", "roc_14", "roc_24"]
buy_indicator_1_value = [-0.05, -0.1, -0.50, -1, -1.5, -2, -2.5, -3, -3.5, -4, -4.5, -5, -5.5, -6, -6.5,  -7, -8, -9, -10]
# sell_indicator_1_name
# sell_indicator_1_value
yield_expected = [0.3, 0.4, 0.5, 0.7, 0.8, 1, 1.2, 1.35, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20, 25, 30, 35, 40, 45, 50]
wait_periods = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 25, 40, 45, 50, 60, 70, 80, 90, 100]


x = []
somelists = [download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value, yield_expected, wait_periods ]
for element in itertools.product(*somelists):
    x.append(element)
    # print(element)

for y in x:
    cursor.execute("INSERT INTO " + db_schema_name + ".tactics_tests (download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value,"
                                          "yield_expected, wait_periods, stock_fee, tactic_status_id, tactic_category_id)  values "
                                          "(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (y[0], y[1], y[2], y[3], y[4], y[5], 0.0015, 0, 1))

print("insert done")
cnxn.commit()



# tastics_for_tests WILLIAMS %R
download_settings_id = [2, 3]
test_stake = [100]
buy_indicator_1_name = ["will_perc_r_6", "will_perc_r_10", "will_perc_r_14"]
buy_indicator_1_value = [-1, -0.9, -0.8, -0.75, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1]
# sell_indicator_1_name
# sell_indicator_1_value
yield_expected = [0.3, 0.4, 0.5, 0.7, 0.8, 1, 1.2, 1.35, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20, 25, 30, 35, 40, 45, 50]
wait_periods = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 25, 40, 45, 50, 60, 70, 80, 90, 100]


x = []
somelists = [download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value, yield_expected, wait_periods ]
for element in itertools.product(*somelists):
    x.append(element)
    # print(element)

for y in x:
    cursor.execute("INSERT INTO " + db_schema_name + ".tactics_tests (download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value,"
                                          "yield_expected, wait_periods, stock_fee, tactic_status_id, tactic_category_id)  values "
                                          "(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (y[0], y[1], y[2], y[3], y[4], y[5], 0.0015, 0, 1))

print("insert done")
cnxn.commit()