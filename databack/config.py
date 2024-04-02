SECRET_KEY = "jdsfiuyyjhT*^(^%^%%^0976"


ENV = 'development'  # 开发环境配置
DEBUG = True  # 调试模式为True
username='root'
password='9981wto9981'
port=3306
db='big'
host='127.0.0.1'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(username, password, host, port, db)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True