import logging

from flask import Flask, request
import datetime
import decimal
import pymysql
import json
import config
from flask_cors import CORS
import time
import psycopg2
import pandas as pd
import numpy as np

app = Flask(__name__)

"""
CORS function is to avoid No 'Access-Control-Allow-Origin' error
"""
CORS(app)



def errors_obj (e):
    return {
    'rows':[[f'Error: {e}']],
    'colums': ['Error'],
    'compute_time': 0
}

# set default function for jsonify
def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


# lamda takes data returns json response
def response(data): return app.response_class(
    response=json.dumps(data, default=set_default),
    status=200,
    mimetype='application/json'
)

def err_response(data): return app.response_class(
    response=json.dumps(data, default=set_default),
    status=400,
    mimetype='application/json'
)

# method to read numbers tuple & conver Decimal('246393')) to float
def read_tuple(tup):
    return [float(i) for i in tup]


# json convert cursor data
def json_cursor(cursor):

    columns = [i[0] for i in cursor.description]

    df = pd.DataFrame(cursor.fetchall(),columns=columns)
    # first 500 rows
    df = df.head(500)

    print(df.count())

    new_data = df.to_json(orient="records")
    json_data = json.loads(new_data)
    # parse json data to list of lists
    data = [list(i.values()) for i in json_data]
    return data,columns
    # data = [dict(zip(columns, row)) for row in cursor]

    # print('new sedata',data)
    # return data



@app.route('/')
def hello():
    # test api
    return 'Welcome Api setup sucessful'


@app.route('/test')
def test_get():
    try:
        # create mysql connection
        conn = pymysql.connect(host=config._DB_CONF['host'],
                               port=config._DB_CONF['port'],
                               user=config._DB_CONF['user'],
                               passwd=config._DB_CONF['passwd'],
                               db=config._DB_CONF['db'])
        cur = conn.cursor()
        # caluclating the time from now
        start_time = time.time()

        sql = "SELECT * FROM aisles LIMIT 3;"
        cur.execute(sql)
        data = json_cursor(cur)


        # get all column names
        columns = [desc[0] for desc in cur.description]
        # get all data
        rows = cur.fetchall()


        # end time
        compute_time = time.time() - start_time
        cur.close()
        conn.close()
        
        # response data
        response_data = {
            'data': data,
            'columns': columns,
            'compute_time': compute_time
        }
        return response(response_data)
    except Exception as e:
        return response(errors_obj(str(e))) 


@app.route('/runsqlquery/instacart', methods=['POST'])
@app.route('/runsqlquery/Abc_retail', methods=['POST'])
def run_mysql_query():
    # read post request data
    url = request.path
    _, db, db_table = url.split('/')
    request_data = request.get_json()
    sql = request_data['sql']
    # print(sql)
    try:
        # create mysql connection
        conn = pymysql.connect(host=config._DB_CONF['host'],
                               port=config._DB_CONF['port'],
                               user=config._DB_CONF['user'],
                               passwd=config._DB_CONF['passwd'],
                               db=db_table)
        cur = conn.cursor()
        # caluclating the time from now
        start_time = time.time()

        cur.execute(sql)
        print('data is being converted')
        data,columns = json_cursor(cur)
       
        # end time
        compute_time = time.time() - start_time
        cur.close()
        conn.close()

        # response data
        response_data = {
            'data': data,
            'columns':columns,
            'compute_time': compute_time
        }
        return response(response_data)
    except Exception as e:
        return err_response(errors_obj(str(e)))


@app.route('/runredshiftquery/instacart', methods=['GET'])
@app.route('/runredshiftquery/instacart', methods=['POST'])
@app.route('/runredshiftquery/Abc_retail', methods=['POST'])
def run_redshift_query():
    url = request.path
    _, db, db_table = url.split('/')

    request_data = request.get_json()
    # sql = request_data['sql']
    sql = "select count(*) from dev.instacart.aisles"
    if request.method == 'GET':
        sql = "select * from aisles LIMIT 10;"
    if request.method == 'POST':
        sql = request_data['sql']  
    try:
        # connect to redshift
        conn = psycopg2.connect(host=config._REDSHIFT_CONF['host'],
                                port=config._REDSHIFT_CONF['port'],
                                user=config._REDSHIFT_CONF['user'],
                                password=config._REDSHIFT_CONF['password'],
                                database=config._REDSHIFT_CONF['database'],
                                options='-c search_path={schema}'.format(schema=db_table)
                                )
        cur = conn.cursor()
        # caluclating the time from now
        start_time = time.time()

        cur.execute(sql)

        # get all column names
        columns = [desc[0] for desc in cur.description]
        print('columnscLLL',columns)
        # get all data
        rows = cur.fetchall()


        # end time
        compute_time = time.time() - start_time
        cur.close()
        conn.close()

        # response data
        response_data = {
            'data': rows[:500],
            'columns':columns,
            'compute_time': compute_time
        }
        return response(response_data)
    except Exception as e:
        return err_response(errors_obj(str(e)))    


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    app.run(threaded=True, debug=True,port=5000)

# [END app]
