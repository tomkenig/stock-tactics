SELECT * FROM m1174_stock_dwh.tactics_tests_results  ttr
left join tactics_tests tt on ttr.tactic_id = tt.tactic_id
 where score_2 >= 1000
  -- and buy_indicator_1_name not like '%roc%'
  -- and score_4 = 1
 -- and wait_periods <= 20
  -- and tt.download_settings_id <> 3
order by score_3 desc, score_2 desc
limit 1000
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