import psycopg2
from datetime import date, datetime, time
conn = psycopg2.connect(database = "project8-db", user = "postgres", host= 'localhost', password = "8600", port = 5432)

#Items to Order
# 2 - Miso Soup
# 1 - Kani Salad
# 2 - Gyudon
# 1 - Shoyu Ramen

# Open a cursor to perform database operations
cur = conn.cursor()

# Fetch all rows from the menu table
cur.execute("SELECT * FROM menu")
rows = cur.fetchall()

# Julia - Create a dictionary from the rows
menu = {}
for row in rows:
		menu[row[0]] = row[1]
	
# Make the changes to the database persistent
conn.commit()

# Julia - Storing customer details
customer_name = []
customer_no = []
customer_address = []
payment_method = []

#Storing Branch details
branch = {"Ortigas","Shangri-La","Katipunan"}

# Julia - Menu Display
def display_menu():
	print("Menu:")
	for i, (item, price) in enumerate(menu.items()):
		print(f"{item} - ₱{price:.2f}")
		

print("Welcome to Irasshaimase! Which Branch will you be delivering from today?")
branch_detail = input("Branch Name: Ortigas, Shangri-La, or Katipunan ")
while True:
	if branch_detail not in branch:
		print('ITM Kitchen does not delivery to your area. Kindly contact any branch for further assistance.')
		print("Welcome to Irasshaimase! Which Branch will you be delivering from today?")
		branch_detail = input("Branch Name: Ortigas, Shangri-La, or Katipunan ")
	else: 
		display_menu()
		break
	
#conn.commit()

# Julia - Initialize orders and receipt dictionary
orders = []
receipt = {product_name: 0 for product_name in menu}

while True:
		product_name = input("Please enter product name:")
		if product_name not in menu:
				print('Product not found')
				continue
	
		product_quantity = int(input("Please enter the product quantity:"))
	
		# Remember the order
		orders.append({'product_name': product_name, 'product_quantity': product_quantity})
		receipt[product_name] += product_quantity
	
		order_more = input("Would you like to order more? (Yes/No)")
		if order_more == "Yes":
			continue
		elif order_more == "No":
			#Chrystan - Call to insert order: 
				total_price = sum(menu[p] * receipt[p] for p in menu)
				currentDateOnly = date.today()
				now = datetime.now()
				current_time = now.time()
				cur.callproc('insert_order', [branch_detail, currentDateOnly, current_time, total_price])
				new_order_id = str(cur.fetchone()[0])
				final_order_id = "The new order ID is: " + new_order_id
				conn.commit()
				#Chrystan - Loop for inserting all orders into order_details 
				for order in orders:
					product_name = order['product_name']
					quantity = order['product_quantity']
					price =  menu[product_name]
					sql = "CALL insert_order_details(%s, %s, %s, %s);"
					params = (new_order_id,product_name, quantity, price)
					cur.execute(sql, params)
					conn.commit()
					
				#Julia - Review Orders
				print("Review your Order Here")
				for p in menu:
					if receipt[p] > 0:
						print(f"{p} - {receipt[p]} - {receipt[p] * menu[p]} pesos")
						
				delivery_details = input("Would you like to proceed with your delivery? (Yes/No)")
				if delivery_details == "Yes":
					print(f'''

					To proceed with your delivery, kindly provide the neccesary details 
					so our branch manager may reach out and communicate any updates on your order.

					''')
					customer_name.append(input("Name: "))
					customer_no.append(input("Contact Number: "))
					customer_address.append(input("Address: "))
					payment_method.append(input("Payment Method (Gcash, COD, Bank Transfer): "))
					
					# Insert customer details into customers table
					cur.execute("INSERT INTO customers (order_id, customer_name, customer_no, customer_address, payment_method) VALUES (%s, %s, %s, %s, %s)", (new_order_id, customer_name[-1], customer_no[-1], customer_address[-1], payment_method[-1]))
					
					# Make the changes to the database persistent
					conn.commit()

					print(f'''

					Review your Order Here
					''')
					print("Name: ","".join(customer_name))
					print("Contact Number: ","".join(customer_no))
					print("Address: ","".join(customer_address))
					print("Payment Method: ","".join(payment_method))
					print(f"Total Price: {total_price} pesos")
					
					for p in menu:
						if receipt[p] > 0:
							print(f"{p} - {receipt[p]} - {receipt[p] * menu[p]} pesos")
					print(f'''

					Thank you very much for ordering from IT Kitchen, 
					please expect a call or message from your chosen branch to process the order payment.


					''')
					break
				else:
					break
			
# Close cursor and communication with the database
cur.close()
conn.close()