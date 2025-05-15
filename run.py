from app import create_app, db
from app.models import AggregationConfig, User
from werkzeug.security import generate_password_hash

app = create_app()

# 初回起動時にデータベースの初期化（テーブル作成）
with app.app_context():
    db.create_all()

    new_records = []

    # 初期データの挿入
    if not AggregationConfig.query.first():
        new_records = [
            AggregationConfig(parent_group_key='1', group_by_key='ニフティ', customer_code='62886', manager_code='7285', leader_code='7675'),
            AggregationConfig(parent_group_key='1', group_by_key='ニフティ', customer_code='62886', manager_code='7546', leader_code='7675'),
            AggregationConfig(parent_group_key='1', group_by_key='富士通【三井／JGG】', customer_code='10005', manager_code='7285', leader_code='6954'),
            AggregationConfig(parent_group_key='1', group_by_key='富士通【三井／JGG】', customer_code='10005', manager_code='7285', leader_code='7546'),
            AggregationConfig(parent_group_key='1', group_by_key='富士通【三井／JGG】', customer_code='10005', manager_code='7546', leader_code='6954'),
            AggregationConfig(parent_group_key='1', group_by_key='富士通【三井／JGG】', customer_code='10005', manager_code='7546', leader_code='7546'),
            AggregationConfig(parent_group_key='1', group_by_key='富士通【三井／JGG】', customer_code='10005', manager_code='7546', leader_code='7761'),
            AggregationConfig(parent_group_key='1', group_by_key='富士通【三井／JGG】', customer_code='10005', manager_code='7818', leader_code='7847'),
            AggregationConfig(parent_group_key='1', group_by_key='SIE', customer_code='62511', manager_code='7527', leader_code='7202'),
            AggregationConfig(parent_group_key='1', group_by_key='SIE', customer_code='62511', manager_code='7527', leader_code='7527'),
            AggregationConfig(parent_group_key='1', group_by_key='SIE', customer_code='62511', manager_code='7527', leader_code='7593'),
            AggregationConfig(parent_group_key='1', group_by_key='富士通【FFG】', customer_code='10005', manager_code='7188', leader_code='2466'),
            AggregationConfig(parent_group_key='1', group_by_key='富士通【FFG】', customer_code='10005', manager_code='7188', leader_code='7188'),
            AggregationConfig(parent_group_key='1', group_by_key='富士通【FFG】', customer_code='10005', manager_code='7188', leader_code='7348'),
            AggregationConfig(parent_group_key='1', group_by_key='富士通【FFG】', customer_code='10005', manager_code='7188', leader_code='7646'),
            AggregationConfig(parent_group_key='1', group_by_key='富士通【FFG】', customer_code='10005', manager_code='7188', leader_code='7659'),
            AggregationConfig(parent_group_key='1', group_by_key='富士通【FFG】', customer_code='10005', manager_code='7285', leader_code='7348'),
            AggregationConfig(parent_group_key='1', group_by_key='富士通【FFG】', customer_code='10005', manager_code='7285', leader_code='7646'),
            AggregationConfig(parent_group_key='2', group_by_key='GSH', customer_code='21148', manager_code='6264', leader_code='7056'),
            AggregationConfig(parent_group_key='2', group_by_key='GSH', customer_code='21148', manager_code='7572', leader_code='7056'),
            AggregationConfig(parent_group_key='2', group_by_key='GSH', customer_code='21148', manager_code='7704', leader_code='7056'),
            AggregationConfig(parent_group_key='2', group_by_key='GSH', customer_code='60610', manager_code='6264', leader_code='6264'),
            AggregationConfig(parent_group_key='2', group_by_key='日立SIS', customer_code='62553', manager_code='7572', leader_code='7704'),
            AggregationConfig(parent_group_key='2', group_by_key='日立SIS', customer_code='62553', manager_code='7704', leader_code='7704'),
            AggregationConfig(parent_group_key='2', group_by_key='日立SIS', customer_code='62743', manager_code='7704', leader_code='7572'),
            AggregationConfig(parent_group_key='2', group_by_key='MSE', customer_code='62361', manager_code='7572', leader_code='7572'),
            AggregationConfig(parent_group_key='2', group_by_key='MSE', customer_code='62361', manager_code='7704', leader_code='6264'),
            AggregationConfig(parent_group_key='2', group_by_key='MSE', customer_code='62361', manager_code='7704', leader_code='7484'),
            AggregationConfig(parent_group_key='2', group_by_key='MSE', customer_code='62361', manager_code='7704', leader_code='7572'),
            AggregationConfig(parent_group_key='2', group_by_key='東洋新薬', customer_code='63288', manager_code='7572', leader_code='7572'),
            AggregationConfig(parent_group_key='2', group_by_key='東洋新薬', customer_code='63288', manager_code='7704', leader_code='7734'),
            AggregationConfig(parent_group_key='3', group_by_key='臼杵', customer_code='62079', manager_code='7203', leader_code='5959'),
            AggregationConfig(parent_group_key='3', group_by_key='SNC', customer_code='30025', manager_code='7203', leader_code='5959'),
            AggregationConfig(parent_group_key='3', group_by_key='SNC', customer_code='30025', manager_code='7203', leader_code='7093'),
            AggregationConfig(parent_group_key='3', group_by_key='SNC', customer_code='30025', manager_code='7203', leader_code='7640'),
            AggregationConfig(parent_group_key='3', group_by_key='SNC', customer_code='30025', manager_code='7203', leader_code='7724')
        ]

    if not User.query.first():  # すでにユーザーがいなければ
        hashed_password = generate_password_hash('n,_Z,ist2YZm')
        new_records.append(User(username='admin', email='test@test.co.jp', password=hashed_password))

    if new_records:
        try :
            db.session.add_all(new_records)
            db.session.commit()
            print("Database initialized successfully!")
        except Exception as e:
            print(f"Error initializing database: {e}")
    else:
        print("No new data to initialize.")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    #app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))