import logging

from flask import Flask, request
import datetime
import decimal
import pymysql
import json
import config
from flask_cors import CORS

app = Flask(__name__)

"""
CORS function is to avoid No 'Access-Control-Allow-Origin' error
"""
CORS(app)

def type_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    if isinstance(x, decimal.Decimal):
        return '$%.2f'%(x)
    raise TypeError("Unknown type")

def rows_to_json(cols,rows):

    result = []
    for row in rows:
        data = dict(zip(cols, row))
        result.append(data)
    return json.dumps(result, default=type_handler)


@app.route('/')
def hello():
    # test api 
    return 'Welcome Api setup sucessful'

@app.route('/test')
def test_get():
 
    # create mysql connection
    conn = pymysql.connect(host=config._DB_CONF['host'], 
                           port=config._DB_CONF['port'], 
                           user=config._DB_CONF['user'], 
                           passwd=config._DB_CONF['passwd'], 
                           db=config._DB_CONF['db'])
    cur = conn.cursor()
    sql="SELECT * FROM mytable LIMIT 3;"
    cur.execute(sql)
    
    # get all column names
    columns = [desc[0] for desc in cur.description]
    # get all data
    rows=cur.fetchall()
    
    # build json 
    result = rows_to_json(columns,rows)
    #print(result)
    
    cur.close()
    conn.close()

    return result



@app.route('/runsqlquery', methods=['POST'])
def run_mysql_query():
    # read post request data
    request_data = request.get_json()

    print(request_data)
     
    # create a new connection
    conn = pymysql.connect(host=config._DB_CONF['host'], 
                           port=config._DB_CONF['port'], 
                           user=config._DB_CONF['user'], 
                           passwd=config._DB_CONF['passwd'], 
                           db=config._DB_CONF['db'])
    cur = conn.cursor()
    # read the query to run from request 
    sql = request_data['sql']
    # excure the query
    cur.execute(sql)
    
    # get all column names
    columns = [desc[0] for desc in cur.description]

    # get all data
    rows=cur.fetchall()
    
    # build json 
    result = rows_to_json(columns,rows)
    
    # close connection
    cur.close()
    conn.close()

    return result
  	
@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    app.run(threaded=True,debug=True)

## [END app]

