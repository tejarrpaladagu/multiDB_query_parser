CREATE TABLE instacart.departments (
             department_id INT NOT NULL,
            department VARCHAR (256) NOT NULL,
             PRIMARY KEY (department_id)
             );
             
             
CREATE TABLE instacart.aisles (
             aisle_id INT NOT NULL, 
             aisle VARCHAR(256) NOT NULL,
             department_id INT NOT NULL,
             PRIMARY KEY (aisle_id),
             CONSTRAINT pd_didfk_1 FOREIGN KEY (department_id) REFERENCES instacart.departments(department_id));             

CREATE TABLE instacart. orders (
            order_id INT NOT NULL,
            user_id INT NOT NULL,
            order_number INT NOT NULL,
            order_dow INT NOT NULL,
            order_hour_of_day INT NOT NULL,
            days_since_prior_order INT NOT NULL,
            PRIMARY KEY (order_id)
            ); 
            
CREATE TABLE instacart.products (
                product_id INT NOT NULL,
                product VARCHAR (256) NOT NULL,
                aisle_id INT NOT NULL,
                PRIMARY KEY (product_id),
                CONSTRAINT pd_aidfk_1 FOREIGN KEY (aisle_id) REFERENCES instacart.aisles(aisle_id)
            );           
            
CREATE TABLE instacart.order_products (
                order_id INT NOT NULL,
                product_id INT NOT NULL,
                add_to_cart_order INT NOT NULL,
                reordered INT NOT NULL,
                PRIMARY KEY ( product_id, order_id ),
                CONSTRAINT opd_pidfk_1 FOREIGN KEY (product_id) REFERENCES instacart.products(product_id),
                CONSTRAINT opd_oidfk_1 FOREIGN KEY (order_id) REFERENCES instacart.orders(order_id)
            );
