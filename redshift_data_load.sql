
COPY dev.instacart.departments FROM 's3://insta-cart-data/Instacart_Data/departments.csv'
CREDENTIALS 'aws_access_key_id=AKIAVDOU3QDOV73BQQE2;aws_secret_access_key=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'
DELIMITER ','
DATEFORMAT AS 'auto'
TIMEFORMAT AS 'auto'
IGNOREHEADER 1
REMOVEQUOTES;


COPY dev.instacart.aisles FROM 's3://insta-cart-data/Instacart_Data/aisles_norm.csv'
CREDENTIALS 'aws_access_key_id=AKIAVDOU3QDOV73BQQE2;aws_secret_access_key=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'
DELIMITER ','
DATEFORMAT AS 'auto'
TIMEFORMAT AS 'auto'
IGNOREHEADER 1
REMOVEQUOTES;


COPY dev.instacart.orders FROM 's3://insta-cart-data/Instacart_Data/orders.csv'
CREDENTIALS 'aws_access_key_id=AKIAVDOU3QDOV73BQQE2;aws_secret_access_key=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'
DELIMITER ','
DATEFORMAT AS 'auto'
TIMEFORMAT AS 'auto'
IGNOREHEADER 1
REMOVEQUOTES;



COPY dev.instacart.products FROM 's3://insta-cart-data/Instacart_Data/products.csv'
CREDENTIALS 'aws_access_key_id=AKIAVDOU3QDOV73BQQE2;aws_secret_access_key=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'
DELIMITER ','
DATEFORMAT AS 'auto'
TIMEFORMAT AS 'auto'
IGNOREHEADER 1
REMOVEQUOTES;




COPY dev.instacart.products FROM 's3://insta-cart-data/Instacart_Data/products.csv'
CREDENTIALS 'aws_access_key_id=AKIAVDOU3QDOV73BQQE2;aws_secret_access_key=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'
DELIMITER ','
DATEFORMAT AS 'auto'
TIMEFORMAT AS 'auto'
IGNOREHEADER 1;



COPY dev.instacart.order_products FROM 's3://insta-cart-data/Instacart_Data/order_products.csv'
CREDENTIALS 'aws_access_key_id=AKIAVDOU3QDOV73BQQE2;aws_secret_access_key=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'
DELIMITER ','
DATEFORMAT AS 'auto'
TIMEFORMAT AS 'auto'
IGNOREHEADER 1
REMOVEQUOTES;


