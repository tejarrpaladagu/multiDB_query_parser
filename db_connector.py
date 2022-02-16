import mysql.connector
import config


class DBInstance(object):
    # global variables
    conn = None
    cursor = None
    
    # class initializer
    def __init__(self):
        self.connect_to_db()
        return

    # connect to database
    def connect_to_db(self):
        self.conn = mysql.connector.connect(
            host=config._DB_CONF['host'],
            port=config._DB_CONF['port'],
            user=config._DB_CONF['user'],
            passwd=config._DB_CONF['passwd'],
            db=config._DB_CONF['db']
        )
        self.cursor = self.conn.cursor(dictionary=True)
        return
