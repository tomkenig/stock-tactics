-- create table tactics_tests_results_bak_20211015 as
SELECT 
ttr.*, tt.*,
score_2 / score_1  as score_5
 FROM m1174_stock_dwh.tactics_tests_results  ttr
left join tactics_tests tt on ttr.tactic_id = tt.tactic_id
 where 
score_2 >= 1000
and score_4 = 1 -- every year plus
-- and score_3 = 1 -- every month plus
and wait_periods <= 33
and score_3 >= 0.7
-- and buy_indicator_1_value > -3
 and score_1 > 1000
-- and buy_indicator_1_value between -2 and 0
 -- and ttr.tactic_id in (481832, 507327) -- good tactics
-- order by score_5 desc, score_3 desc, score_2 desc
-- ttr.download_settings_id = 2
order by score_5 desc, score_2 desc, score_3 desc
limit 10000
;

SELECT count(*)
,download_settings_id
,tactic_status_id
,buy_indicator_1_name
 FROM m1174_stock_dwh.tactics_tests
group by 
download_settings_id
,tactic_status_id
,buy_indicator_1_name;

select count(*) from m1174_stock_dwh.tactics_tests_results;

select count(*) from m1174_stock_dwh.tactics_tests;

SELECT count(*) FROM m1174_stock_dwh.tactics_tests where tactic_status_id=2;
-- 7221, next ~~12,2k

SELECT count(*) FROM m1174_stock_dwh.tactics_tests;

SELECT count(*),tactic_status_id, download_settings_id FROM m1174_stock_dwh.tactics_tests group by tactic_status_id, download_settings_id;

select * from binance_download_settings;

-- update m1174_stock_dwh.tactics_tests set tactic_status_id = 0;