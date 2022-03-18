
import boto3
from collections import OrderedDict
import sys

from loguru import logger

from db_connector import DBInstance



# sql queries dict for each table 
# (key: csv file path in the s3 bucket, value: object of diff queries(DROP,CREate,INSERT))
# each csv file is a table in the database
# each object is a dict with keys: DROP, CREATE, INSERT
SQL_Queries = OrderedDict({
    "departments.csv": {
        "DROP": ("DROP TABLE IF EXISTS departments"),
        "CREATE": (
            """CREATE TABLE departments (
            department_id INT NOT NULL,
            department VARCHAR (256) NOT NULL,
            PRIMARY KEY (department_id))"""
        ),
        "INSERT": ("""INSERT INTO departments ( department_id, department )
            VALUES ( %s, %s )""")
    },
    "aisles_norm.csv": {
        "DROP": ("DROP TABLE IF EXISTS aisles"),
        "CREATE": ("""CREATE TABLE aisles (
            aisle_id INT NOT NULL, aisle VARCHAR(256) NOT NULL,department_id INT NOT NULL,
            PRIMARY KEY (aisle_id),CONSTRAINT pd_didfk_1 FOREIGN KEY (department_id) REFERENCES departments(department_id))"""),
        "INSERT": ("""INSERT INTO aisles ( aisle_id, aisle, department_id)
            VALUES ( %s, %s, %s )""")
    },
  "orders.csv": {
        "DROP": ("DROP TABLE IF EXISTS orders"),
        "CREATE": (
            """CREATE TABLE orders (
            order_id INT NOT NULL,
            user_id INT NOT NULL,
            order_number INT NOT NULL,
            order_dow INT NOT NULL,
            order_hour_of_day INT NOT NULL,
            days_since_prior_order INT NOT NULL,
            PRIMARY KEY (order_id))"""
        ),
        "INSERT": ("""INSERT INTO orders (
                order_id, user_id, order_number, order_dow,
                order_hour_of_day, days_since_prior_order
            )
            VALUES ( %s, %s, %s, %s, %s, %s )"""
        )
    },
  
    "products_norm.csv": {
        "DROP": ("DROP TABLE IF EXISTS products"),
        "CREATE": (
            """CREATE TABLE products (
                product_id INT NOT NULL,
                product VARCHAR (256) NOT NULL,
                aisle_id INT NOT NULL,
                PRIMARY KEY (product_id),
                CONSTRAINT pd_aidfk_1 FOREIGN KEY (aisle_id) REFERENCES aisles(aisle_id),
            )"""
        ),
        "INSERT": ("""INSERT INTO products ( product_id, product_name, aisle_id, department_id )
            VALUES ( %s, %s, %s, %s )""")
    },
    "order_products.csv": {
        "DROP": ("DROP TABLE IF EXISTS order_products"),
        "CREATE": (
            """CREATE TABLE order_products (
                order_id INT NOT NULL,
                product_id INT NOT NULL,
                add_to_cart_order INT NOT NULL,
                reordered INT NOT NULL,
                PRIMARY KEY ( product_id, order_id ),
                CONSTRAINT opd_pidfk_1 FOREIGN KEY (product_id) REFERENCES products(product_id),
                CONSTRAINT opd_oidfk_1 FOREIGN KEY (order_id) REFERENCES orders(order_id)
            )"""
        ),
        "INSERT": (
            """INSERT INTO order_products (
            order_id, product_id, add_to_cart_order, reordered
            ) VALUES (
                %s, %s, %s, %s
            )"""
        )
    }

})

# aws s3 connection
s3 = boto3.resource('s3')
# get bucket
bucket = s3.Bucket('insta-cart-data')

# read all objects in the bucket
obj_dict = {obj.key: obj for obj in bucket.objects.all()}


# for each sql query dict, execute the query
for key, value in SQL_Queries.items():
    logger.info("key on s3: {}".format(key))

    # read data from s3 obj
    data_obj = obj_dict[key]
    body_data = data_obj.get()['Body'].read()
    content = str(body_data, encoding="utf-8")   # bytes to str
    lines = content.split("\r\n") # split lines by \r\n
    logger.info("Read {0} lines of data {1}".format(
        len(lines) - 2, str(key).split(".")[0]))

    # create DbInstance connection
    dataBase = DBInstance()

    # drop table if exists
    dataBase.cursor.execute(value["DROP"])
    # create table
    dataBase.cursor.execute(value["CREATE"])

    # insert data
    logger.info("Completed {0} records of data into table {1}".format(
        str(len(lines) - 2), str(key).split(".")[0]))
    for i in range(len(lines) - 1):
        columns = tuple(lines[i].split(","))
        dataBase.cursor.execute(value["INSERT"], columns)
        if i % 2000 == 0:
            logger.info("Write {0} lines.".format(i))
            dataBase.conn.commit()

    dataBase.conn.commit()
    logger.info("Write successfully!")

    dataBase.cursor.close()
    dataBase.conn.close()
