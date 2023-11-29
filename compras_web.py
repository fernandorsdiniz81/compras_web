# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.edge.options import Options
from time import sleep
import mysql.connector
import os
from flask import Flask, render_template, request, redirect
from bs4 import BeautifulSoup as bs
import requests

# from dotenv import load_dotenv
# load_dotenv()

# class SeleniumScraping:
# 	def __init__(self):
# 		self.options = Options()
# 		self.options.page_load_strategy = 'normal'
# 		self.options.add_argument("--blink-settings=imagesEnabled=false") # no images loaded
# 		self.options.add_argument("--headless") # browser is invisible
# 		self.shopping_list = []
			
# 	def create_shopping_list(self, url):
# 		try:
# 			driver = webdriver.Edge(options=self.options)
# 		except:
# 			driver = webdriver.Chrome(options=self.options)
# 		driver.get(url)
# 		sleep(2)
		
# 		item_xpath = '//tbody[@id="myTable"]/tr/td[1]/h7'
# 		amount_xpath = '//tbody[@id="myTable"]/tr/td[2]'
# 		price_xpath = '//tbody[@id="myTable"]/tr/td[4]'
# 		shopping_date_xpath = '//div[@id="collapse4"]/table[3]/tbody/tr/td[4]'
# 		supermarket_xpath = '//div[@id="formPrincipal:content-template-consulta"]/div[1]/table[1]/thead/tr[2]/th/h4/b'
		
# 		items = driver.find_elements(By.XPATH, item_xpath)
# 		amounts = driver.find_elements(By.XPATH, amount_xpath)
# 		prices = driver.find_elements(By.XPATH, price_xpath)
# 		supermarket = driver.find_element(By.XPATH, supermarket_xpath)
		
# 		driver.find_element(By.XPATH, '//div[@id="heading3"]/h4').click()
# 		sleep(0.5)
# 		shopping_date = driver.find_element(By.XPATH, shopping_date_xpath)
# 		shopping_date = shopping_date.text[:10].split("/")
# 		shopping_date = ("/").join(reversed(shopping_date))
		
# 		for item, amount, price in zip(items, amounts, prices):
# 			registry = (0, item.text.strip(), amount.text[20:].strip(), price.text[18:].strip().replace(',','.'), supermarket.text.strip(), shopping_date)
# 			self.shopping_list.append(registry)
# 			# como id é autoincrement, não é necessário se preocupar com o valor, mas preencher 'default' não foi aceito
		

class BeatifulSoupScraping:
	def __init__(self) -> None:
		self.shopping_list = []
	def create_shopping_list(self, url):
		try:
			response = requests.get(url)
			page = response.text
			self.soup = bs(page, "html.parser")
		except:
			return response.status_code	
		self.shopping_list = []
		table = self.soup.find_all("td")
		for td in table:
			h7 = td.find("h7") # O nome do item fica em um h7 dentro de um td, demais info em um td
			if h7 != None:
				h7 =str(h7)
				h7 = h7[4:-5].strip()
				self.shopping_list.append(h7)
			else:
				self.shopping_list.append(td.text.strip())
		# Neste ponto, as tags td ainda estão sequenciais, sem separação por item, quantidade e preço.
  		# O primeiro produto está na td2, o primeiro quantidade na td3 e o primeiro preço na td5.
		# O ciclo se repete a cada 4 tags td.
		# O último td referente ao preço do último produto está a 19 tags td do final para o início.
		
		items = []
		for i, td in zip(range(2, len(self.shopping_list)-19, 4), self.shopping_list):
			items.append(self.shopping_list[i])

		amounts = []
		for i, td in zip(range(3, len(self.shopping_list)-19, 4), self.shopping_list):
			amount = (self.shopping_list[i])[20:]
			amounts.append(amount)

		prices = []
		for i, td in zip(range(5, len(self.shopping_list)-19, 4), self.shopping_list):
			price = (self.shopping_list[i])[18:].strip().replace(',','.')
			prices.append(price)

		supermarket = self.shopping_list[-15]

		shopping_date = self.shopping_list[-5]
		shopping_date = shopping_date[:10].split("/")
		shopping_date = ("/").join(reversed(shopping_date))

		self.shopping_list = []
		for item, amount, price in zip(items, amounts, prices):
			registry = (0, item, amount, price, supermarket, shopping_date)
			self.shopping_list.append(registry)
			# como id é autoincrement, não é necessário se preocupar com o valor, mas preencher 'default' não foi aceito

		return self.shopping_list
	

class DataBase: #CRUD
	def __init__(self):
		self.connection = mysql.connector.connect(
		host = os.environ["host"],
		user = os.environ["user"],
		password = os.environ["password"],
		database = os.environ["database"])
		self.cursor = self.connection.cursor()
   
	
	def close_connection(self):
		pass
		# self.cursor.close()
		# self.connection.close()  


	def create(self, shopping_list):
		for product in shopping_list:
			query = f"INSERT INTO compras VALUES {product}"
			self.cursor.execute(query)
			self.connection.commit()
		

	def read(self, query):
		self.cursor.execute(query)
		resultado = self.cursor.fetchall()
		# self.close_connection()
		return  resultado
		
		
	def update(self):
		query = f"UPDATE compras SET item = 'Fernando R S Diniz' WHERE id = '62'"
		self.cursor.execute(query)
		self.connection.commit()
		# self.close_connection()

		
	def delete(self):
		query = f"DELETE FROM compras WHERE id = '62'"
		self.cursor.execute(query)
		self.connection.commit()
		# self.close_connection()


class Application:
	def __init__(self) -> None:
		pass
	
 	
	def insert_products_from_invoice(self, urls):
		for url in urls:
			invoice.create_shopping_list(url)
		query = "SELECT count(*) FROM compras"
		initial_count = database.read(query)
		database.create(invoice.shopping_list)
		final_count = database.read(query)
		print(f"Foram incluídos {initial_count[0][0] - final_count[0][0]} items.")
		# database.close_connection()	


	def display_registred_products(self, condition):
		query = f"SELECT * FROM compras WHERE produto LIKE '{condition[0]}' OR produto LIKE '{condition[1]}'"
		print(condition) ########### teste ############
		print(query)
		products = database.read(query)
		# database.close_connection()
		f = open('templates/registred_products.html')
		page = f.read()
		for product in products:
			page += f"""
				<tr>
					<td>{product[0]}</td>
					<td>{product[1]}</td>
					<td>{product[2]}</td>
					<td>{product[3]}</td>
					<td>{product[4]}</td>
					<td>{product[5]}</td>
				</tr>
			"""
		page += """
				</tbody>
				</table>
				</body>
				</html>
    			"""
		return page

	
	def format_condition(self, condition):
		vowels = ["a", "e", "i", "o", "u"]
		condition_without_vowel = ""
		
		for letter in condition:
			if letter not in vowels:
				condition_without_vowel += letter    
		
		if condition == "":
			condition = "%"
			condition_without_vowel = "%"
		elif len(condition) > 3:
			condition = f"%{condition[0:3]}%"
			condition_without_vowel = f"%{condition_without_vowel[0:3]}%"
		else:
			condition = f"%{condition}%"
			condition_without_vowel = f"%{condition_without_vowel}%"
		
		return condition, condition_without_vowel		



# invoice = SeleniumScraping()
invoice = BeatifulSoupScraping()
database = DataBase()
application = Application()


app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/read', methods=['POST'])
def read_products():
	condition = request.form['condition']
	condition = application.format_condition(condition)

	page = application.display_registred_products(condition)
	return page 

@app.route('/create', methods=['POST']) # https://portalsped.fazenda.mg.gov.br/portalnfce/sistema/qrcode.xhtml?p=31231171385637001082650130001610761133193289|2|1|1|B97922C625E7F691F49DEB150665888398C3B6C3
def create_products():
	urls = [request.form['url']]
	application.insert_products_from_invoice(urls)
	return "ok" # o problema estava no redirect!?





if __name__ == "__main__":
	app.run(host='0.0.0.0', port=1024, debug=True)
