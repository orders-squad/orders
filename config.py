import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')
HOST = os.getenv('HOST', '0.0.0.0')

db_user = os.getenv('DB_USER', 'flaskrest02')
db_pass = os.getenv('DB_PASS', 'flaskrest02')
db_name = os.getenv('DB_NAME', 'flaskrest02')
db_addr = os.getenv('DB_ADDR', '127.0.0.1:5432')


SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = \
    "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=db_user,
                                                                  DB_PASS=db_pass,
                                                                  DB_ADDR=db_addr,
                                                                  DB_NAME=db_name)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
