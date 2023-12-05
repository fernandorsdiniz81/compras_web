import mysql.connector
import os


class DataBase: #CRUD
	def __init__(self):
		pass
	

	def open_connection(self):
		self.connection = mysql.connector.connect(
		host = os.environ["host"],
		user = os.environ["user"],
		password = os.environ["password"],
		database = os.environ["database"],
  		connection_timeout=60)
		self.cursor = self.connection.cursor()
	

	def close_connection(self):
		self.cursor.close()
		self.connection.close()


	def create(self, shopping_list):
		self.open_connection()
		for product in shopping_list:
			query = f"INSERT INTO compras VALUES {product}"
			self.cursor.execute(query)
			self.connection.commit()
		self.close_connection()
		

	def read(self, query):
			self.open_connection()
			self.cursor.execute(query)
			resultado = self.cursor.fetchall()
			self.close_connection()
			return  resultado
		
		
	#def update(self):
	#	query = f"UPDATE compras SET item = 'Fernando R S Diniz' WHERE id = '62'" # ex.
	#	self.open_connection()
	#	self.cursor.execute(query)
	#	self.connection.commit()
	#	self.close_connection()

		
	#def delete(self):
	#	query = f"DELETE FROM compras WHERE id = '62'" # ex.
	#	self.open_connection()
	#	self.cursor.execute(query)
	#	self.connection.commit()
	#	self.close_connection()