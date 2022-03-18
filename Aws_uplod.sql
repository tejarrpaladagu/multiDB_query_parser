Use instacart1;

# 

CREATE TABLE departments (
             department_id INT NOT NULL,
            department VARCHAR (256) NOT NULL,
             PRIMARY KEY (department_id)
             );
             
             
CREATE TABLE aisles (
             aisle_id INT NOT NULL, 
             aisle VARCHAR(256) NOT NULL,
             department_id INT NOT NULL,
             PRIMARY KEY (aisle_id),
             CONSTRAINT pd_didfk_1 FOREIGN KEY (department_id) REFERENCES departments(department_id));             

CREATE TABLE orders (
            order_id INT NOT NULL,
            user_id INT NOT NULL,
            order_number INT NOT NULL,
            order_dow INT NOT NULL,
            order_hour_of_day INT NOT NULL,
            days_since_prior_order INT NOT NULL,
            PRIMARY KEY (order_id)
            ); 
            
CREATE TABLE products (
                product_id INT NOT NULL,
                product VARCHAR (256) NOT NULL,
                aisle_id INT NOT NULL,
                PRIMARY KEY (product_id),
                CONSTRAINT pd_aidfk_1 FOREIGN KEY (aisle_id) REFERENCES aisles(aisle_id)
            );           
            
CREATE TABLE order_products (
                order_id INT NOT NULL,
                product_id INT NOT NULL,
                add_to_cart_order INT NOT NULL,
                reordered INT NOT NULL,
                PRIMARY KEY ( product_id, order_id ),
                CONSTRAINT opd_pidfk_1 FOREIGN KEY (product_id) REFERENCES products(product_id),
                CONSTRAINT opd_oidfk_1 FOREIGN KEY (order_id) REFERENCES orders(order_id)
            );            
# aisles
LOAD DATA local INFILE '/Users/vamshisaggurthi/Downloads/Db_assignment2/Data/aisles_norm.csv' INTO TABLE aisles FIELDS TERMINATED BY ',' IGNORE 1 ROWS;   


#departments
LOAD DATA local INFILE '/Users/vamshisaggurthi/Downloads/Db_assignment2/Data/departments.csv' INTO TABLE departments FIELDS TERMINATED BY ',' IGNORE 1 ROWS;   


# orders            
LOAD DATA local INFILE '/Users/vamshisaggurthi/Downloads/Db_assignment2/Data/orders.csv' INTO TABLE orders FIELDS TERMINATED BY ',' IGNORE 1 ROWS;   

# products
LOAD DATA local INFILE '/Users/vamshisaggurthi/Downloads/Db_assignment2/Data/products_norm.csv' INTO TABLE products FIELDS TERMINATED BY ',' IGNORE 1 ROWS;   

# order_products         
LOAD DATA local INFILE '/Users/vamshisaggurthi/Downloads/Db_assignment2/Data/order_products.csv' INTO TABLE order_products FIELDS TERMINATED BY ',' IGNORE 1 ROWS;   


