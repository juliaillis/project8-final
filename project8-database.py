import psycopg2

conn = psycopg2.connect(database = "project8-db", user = "postgres", host= 'localhost', password = "8600", port = 5432)

# Open a cursor
cur = conn.cursor()

# Julia - Create menu table
cur.execute("""CREATE TABLE menu (
		product_name TEXT,
		price INTEGER
		)""")

# Commit all changes to the database
conn.commit()
		
# Julia - Create orders table
cur.execute("""CREATE TABLE orders (
		order_id SERIAL PRIMARY KEY,
		branch_details TEXT,
		order_date DATE,
		order_time TIME,
		total_price INTEGER
		)""")

# Commit all changes to the database
conn.commit()

# Julia - create order_details table
cur.execute("""CREATE TABLE order_details (
		order_id INTEGER,
		product_name TEXT,
		product_quantity INTEGER,
		price INTEGER
		)""")

# Commit all changes to the database
conn.commit()

# Julia -  create customers table
cur.execute("""CREATE TABLE customers (
		order_id SERIAL PRIMARY KEY,
		customer_name TEXT,
        customer_no TEXT,
		customer_address TEXT,
		payment_method TEXT
		)""")

# Commit all changes to the database
conn.commit()

# Julia - INSERT Menu items into Menu table
cur.execute("INSERT INTO menu(product_name, price) VALUES('Edamame',150)")

cur.execute("INSERT INTO menu(product_name, price) VALUES('Gyoza',200)")

cur.execute("INSERT INTO menu(product_name, price) VALUES('Chicken Yakitori',220)")

cur.execute("INSERT INTO menu(product_name, price) VALUES('Miso Soup',120)")

cur.execute("INSERT INTO menu(product_name, price) VALUES('Kani Salad',180)")

cur.execute("INSERT INTO menu(product_name, price) VALUES('Spicy Tuna Salad',365)")

cur.execute("INSERT INTO menu(product_name, price) VALUES('Shoyu Ramen',330)")

cur.execute("INSERT INTO menu(product_name, price) VALUES('Chirashi',450)")

cur.execute("INSERT INTO menu(product_name, price) VALUES('Ebi Tempura',550)")

cur.execute("INSERT INTO menu(product_name, price) VALUES('Gyudon',230)")

conn.commit()

#Chrystan - Stored Procedure for inserting in order: 
create_procedure = """
CREATE OR REPLACE FUNCTION insert_order(
	IN branch_details_param TEXT,
	IN order_date_param DATE,
	IN order_time_param TIME,
	IN total_price_param INTEGER
)
RETURNS INTEGER
AS $$
DECLARE new_order_id INTEGER;
BEGIN
	INSERT INTO orders (branch_details, order_date, order_time, total_price)
	VALUES (branch_details_param, order_date_param, order_time_param, total_price_param)
	RETURNING order_id INTO new_order_id;

	RETURN new_order_id;
END;
$$
LANGUAGE plpgsql;
"""

# Execute the CREATE PROCEDURE statement
cur.execute(create_procedure)
conn.commit()

#Chrystan - stored procedure for inserting in order_details: 
create_procedure = """
CREATE OR REPLACE PROCEDURE insert_order_details(
	IN order_id_param INTEGER,
	IN product_name_param TEXT,
	IN product_quantity_param INTEGER,
	IN price_param INTEGER
) LANGUAGE plpgsql
AS $$
BEGIN
	INSERT INTO order_details (order_id,product_name, product_quantity, price)
	VALUES (order_id_param,product_name_param, product_quantity_param, price_param);
END;
$$;
"""

# Execute the CREATE PROCEDURE statement
cur.execute(create_procedure)

conn.commit()


# Close cursor and communication with the database
cur.close()
conn.close()

print("Data tables created")
