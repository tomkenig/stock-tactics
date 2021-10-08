# libs
from db_works import db_connect, db_tables

# tactics_categories
tactic_category_name = "RSI first tests"
tactic_category_priority = 0


# tastics_for_tests
test_stake = 100
download_settings_id = [2,3,4,5,6,7,10,11]
buy_indicator_1_name = ["rsi_6", "rsi_10", "rsi_12", "rsi_14", "rsi_20", "rsi_24"]  # 6 elements
buy_indicator_1_value = [0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]  # 10 elements
# sell_indicator_1_name
# sell_indicator_1_value
yield_expected = [0.3, 0.4, 0.5, 0.7, 0.8, 1, 1.2, 1.35, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20]  # 23 elements
wait_periods = [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,25,40,45,50,60,70,80,90,100]  # 37 elements
