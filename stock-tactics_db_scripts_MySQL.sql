-- drop table tactics_for_tests;
create table tactics_categories
(
 `tactic_category_id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY, -- unique setting identifier
 `tactic_category_name` varchar(255) DEFAULT NULL,
 `tactic_category_status_id` varchar(255) DEFAULT 0, -- 0 - ready, 1 - tested
 `tactic_category_priority` bigint NULL
);


-- drop table tactics_tests;
create table tactics_tests
(
 `tactic_id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY, -- unique setting identifier
  `download_settings_id` int(11) NULL, -- unique setting identifier
  -- at this moment columns listed below can be fethed by download_settings_id in other APP
  -- `market` varchar(10) DEFAULT NULL, -- market pair ie. BTCUSDT; ETHUSDT etc.
  -- `tick_interval` varchar(50) DEFAULT NULL, -- kline interval ie. 1m, 5m, 15m, 1h, 1M etc.
  -- `data_granulation`varchar(50) DEFAULT NULL, -- data granulation ie. klines, trades, aggregated trades
  -- `stock_type` varchar(255) DEFAULT NULL,  -- type of exchanege ie. spot
  -- `stock_exchange` varchar(255) DEFAULT NULL,  -- stock exchange name ie. Binance.com, ByBit.com etc.
  `test_stake` double DEFAULT NULL,
  `buy_indicator_1_name` varchar(50) DEFAULT NULL,
  `buy_indicator_1_value` double DEFAULT NULL,
  `sell_indicator_1_name` varchar(255) DEFAULT NULL,
  `sell_indicator_1_value` double DEFAULT NULL,
  `yield_expected` double DEFAULT NULL,
  `wait_periods` int DEFAULT NULL,
  `stoploss` double DEFAULT NULL,
  `stock_fee`  double DEFAULT NULL,
  `tactic_status_id` int NULL, -- 0 - ready ; 1 - checked
  `tactic_category_id` int(11), -- FK to tactic_category_id. 
  `insert_ux_timestamp` int(10) NULL -- record insert date
);


-- drop table tactics_tests_results;
create table tactics_tests_results
(
 `tactics_tests_results_id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY, -- unique setting identifier
  `download_settings_id` int(11) NULL, -- unique setting identifier
  `tactic_id` bigint NULL,
  `result_string_1` varchar(4000) DEFAULT NULL,
  `result_string_2` varchar(4000) DEFAULT NULL,
  `result_string_3` varchar(4000) DEFAULT NULL,
  `score_1` bigint NULL,
  `score_2` bigint NULL,
  `score_3` bigint NULL,
  `insert_ux_timestamp` int(10) NULL -- record insert date
);

-- SETTINGS & TACTICS
-- CREATE VIEW

