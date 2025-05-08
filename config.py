DB_HOST = 'sql12.freemysqlhosting.net'  
DB_NAME = 'sql12777483'  #constructiondb
DB_USER = 'sql12777483'  
DB_PASSWORD = 'vrtHKCGYqT' 

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Your generated JWT secret key
JWT_SECRET_KEY = 'dbd5d4d1d80019e592d4a578af5b511e3aa2fa0323751e58d66f9c29fa3711d2'
