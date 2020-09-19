import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# define
HOST_ADDR = '127.0.0.1'  # localhost address
SERVER_PORT = 8000  # 서버 포트
DEBUG = False  # 디버그모드
MODE = os.environ.get('MODE')

# connect db
USER = 'postgres'  # username
PASSWOLRD = 'root'  # postgresql pw
DB_PORT = '5432'  # postgresql port
NAME = 'capstone2'  # db name
DB_URI = f'postgresql://{USER}:{PASSWOLRD}@{HOST_ADDR}:{DB_PORT}/'  # postgresql uri

# select operation mode
if MODE == 'TEST' or sys.argv[0].endswith('test'):  # use only pytest
    HOST_ADDR = '127.0.0.1'
    DEBUG = False
    NAME += '_test'
elif MODE == 'DEV':  # mode - development
    HOST_ADDR = '127.0.0.1'
    DEBUG = True
    DB_URI += NAME
elif MODE == 'RUN':  # mode - release
    HOST_ADDR = '0.0.0.0'
    DEBUG = False
    DB_URI += NAME
else:  # select not permission mode
    raise KeyError
