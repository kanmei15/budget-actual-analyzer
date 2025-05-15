-- 予算損益テーブル
CREATE TABLE IF NOT EXISTS budget_profit_and_loss (
    id SERIAL PRIMARY KEY,
    order_code CHAR(10) NOT NULL, -- オーダーコード
    order_name VARCHAR(1000) NOT NULL, -- オーダー名
    deal_status CHAR(1) NOT NULL, -- 商談区分
    customer_code CHAR(5) NOT NULL, -- 取引先コード
    start_dt DATE NOT NULL, -- 作業開始日
    end_dt DATE NOT NULL, -- 作業終了日
    manager_code CHAR(4) NOT NULL, -- マネジャーコード
    leader_code CHAR(4) NOT NULL, -- リーダコード
    month_number INTEGER NOT NULL, -- 月
    internal_man_hours NUMERIC(5, 2) DEFAULT 0.00, -- 自社工数
    partner_man_hours NUMERIC(5, 2) DEFAULT 0.00, -- 協力会社工数
    bulk_man_hours NUMERIC(5, 2) DEFAULT 0.00, -- 一括契約工数
    order_amount INTEGER DEFAULT 0, -- 受注額
    recognized_sales INTEGER DEFAULT 0, -- 売上計上額
    recognized_profit INTEGER DEFAULT 0, -- 利益計上額
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 作成日時
    UNIQUE (order_code, month_number)
);

-- 実績損益テーブル
CREATE TABLE IF NOT EXISTS actual_profit_and_loss (
    id SERIAL PRIMARY KEY,
    order_code CHAR(10) NOT NULL, -- オーダーコード
    order_name VARCHAR(1000) NOT NULL, -- オーダー名
    deal_status CHAR(1) NOT NULL, -- 商談区分
    customer_code CHAR(5) NOT NULL, -- 取引先コード
    start_dt DATE NOT NULL, -- 作業開始日
    end_dt DATE NOT NULL, -- 作業終了日
    manager_code CHAR(4) NOT NULL, -- マネジャーコード
    leader_code CHAR(4) NOT NULL, -- リーダコード
    month_number INTEGER NOT NULL, -- 月
    internal_man_hours NUMERIC(5, 2) DEFAULT 0.00, -- 自社工数
    partner_man_hours NUMERIC(5, 2) DEFAULT 0.00, -- 協力会社工数
    bulk_man_hours NUMERIC(5, 2) DEFAULT 0.00, -- 一括契約工数
    order_amount INTEGER DEFAULT 0, -- 受注額
    recognized_sales INTEGER DEFAULT 0, -- 売上計上額
    recognized_profit INTEGER DEFAULT 0, -- 利益計上額
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 作成日時
    UNIQUE (order_code, month_number)
);

-- 集計設定テーブル
CREATE TABLE IF NOT EXISTS aggregation_config (
    id SERIAL PRIMARY KEY,
    parent_group_key CHAR(1) NOT NULL, -- 集計軸（親）
    group_by_key VARCHAR(20) NOT NULL, -- 集計軸
    customer_code CHAR(5) NOT NULL, -- 取引先コード
    manager_code CHAR(4) NOT NULL, -- マネジャーコード
    leader_code CHAR(4) NOT NULL, -- リーダコード
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 作成日時
    UNIQUE (customer_code, manager_code, leader_code)
);

INSERT INTO aggregation_config (parent_group_key, group_by_key, customer_code, manager_code, leader_code) VALUES 
('1','ニフティ','62886','7285','7675'),
('1','ニフティ','62886','7546','7675'),
('1','富士通【三井／JGG】','10005','7285','6954'),
('1','富士通【三井／JGG】','10005','7285','7546'),
('1','富士通【三井／JGG】','10005','7546','6954'),
('1','富士通【三井／JGG】','10005','7546','7546'),
('1','富士通【三井／JGG】','10005','7546','7761'),
('1','富士通【三井／JGG】','10005','7818','7847'),
('1','SIE','62511','7527','7202'),
('1','SIE','62511','7527','7527'),
('1','SIE','62511','7527','7593'),
('1','富士通【FFG】','10005','7188','2466'),
('1','富士通【FFG】','10005','7188','7188'),
('1','富士通【FFG】','10005','7188','7348'),
('1','富士通【FFG】','10005','7188','7646'),
('1','富士通【FFG】','10005','7188','7659'),
('1','富士通【FFG】','10005','7285','7348'),
('1','富士通【FFG】','10005','7285','7646'),
('2','GSH','21148','6264','7056'),
('2','GSH','21148','7572','7056'),
('2','GSH','21148','7704','7056'),
('2','GSH','60610','6264','6264'),
('2','日立SIS','62553','7572','7704'),
('2','日立SIS','62553','7704','7704'),
('2','日立SIS','62743','7704','7572'),
('2','MSE','62361','7572','7572'),
('2','MSE','62361','7704','6264'),
('2','MSE','62361','7704','7484'),
('2','MSE','62361','7704','7572'),
('2','東洋新薬','63288','7572','7572'),
('2','東洋新薬','63288','7704','7734'),
('3','臼杵','62079','7203','5959'),
('3','SNC','30025','7203','5959'),
('3','SNC','30025','7203','7093'),
('3','SNC','30025','7203','7640'),
('3','SNC','30025','7203','7724');

-- 集計損益テーブル
CREATE TABLE IF NOT EXISTS aggregated_profit_and_loss (
    id SERIAL PRIMARY KEY,
    source_type CHAR(1) NOT NULL, -- 0:budget 1:actual
    parent_group_key CHAR(1) NOT NULL, -- 集計軸（親）
    group_by_key VARCHAR(20) NOT NULL, -- 集計軸
    month_number INTEGER NOT NULL,     -- 月
    total_order_amount INTEGER DEFAULT 0,
    total_sales INTEGER DEFAULT 0,
    total_profit INTEGER DEFAULT 0,
    total_internal_man_hours NUMERIC(5,2) DEFAULT 0.00,
    total_partner_man_hours NUMERIC(5,2) DEFAULT 0.00,
    total_bulk_man_hours NUMERIC(5,2) DEFAULT 0.00,
    aggregated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (source_type, parent_group_key, group_by_key, month_number)
);

-- 差分損益テーブル
CREATE TABLE IF NOT EXISTS difference_profit_and_loss (
    id SERIAL PRIMARY KEY,
    parent_group_key CHAR(1) NOT NULL, -- 集計軸（親）
    group_by_key VARCHAR(20) NOT NULL, -- 集計軸
    month_number INTEGER NOT NULL,     -- 月
    diff_order_amount INTEGER DEFAULT 0,
    diff_sales INTEGER DEFAULT 0,
    diff_profit INTEGER DEFAULT 0,
    diff_internal_man_hours NUMERIC(5,2) DEFAULT 0.00,
    diff_partner_man_hours NUMERIC(5,2) DEFAULT 0.00,
    diff_bulk_man_hours NUMERIC(5,2) DEFAULT 0.00,
    difference_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (parent_group_key, group_by_key, month_number)
);