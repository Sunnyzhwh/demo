import pymysql
from lib.db import patch_model

pymysql.install_as_MySQLdb()
patch_model()
