from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

origin_db_data = {
    'host'     : '127.0.0.1',
    'port'     : '5432',
    'user'     : 'stefan',
    'password' : 'postgres',
    'db'       : 'cookblog_db'
}

origin_db_uri = "postgresql://{}:{}@{}:{}/{}".format(
    origin_db_data['user'], origin_db_data['password'], 
    origin_db_data['host'], origin_db_data['port'], 
    origin_db_data['db'])

test_db_data = {
    'host'     : '127.0.0.1',
    'port'     : '5432',
    'user'     : 'stefan',
    'password' : 'postgres',
    'db'       : 'cookblog_db_test'
}

test_db_uri = "postgresql://{}:{}@{}:{}/{}".format(
    test_db_data['user'], test_db_data['password'], 
    test_db_data['host'], test_db_data['port'], 
    test_db_data['db'])