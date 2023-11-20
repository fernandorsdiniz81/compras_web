from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from time import sleep
from mysql import connector
import os
from flask import Flask, render_template, request, redirect

# from dotenv import load_dotenv
# load_dotenv()

class Invoice:
	def __init__(self):
		self.options = Options()
		self.options.page_load_strategy = 'normal'
		self.options.add_argument("--blink-settings=imagesEnabled=false") # no images loaded
		self.options.add_argument("--headless") # browser is invisible
		self.shopping_list = []
			
	def create_shopping_list(self, url):
		driver = webdriver.Edge(options=self.options)
		driver.get(url)
		sleep(2)
		
		item_xpath = '//tbody[@id="myTable"]/tr/td[1]/h7'
		amount_xpath = '//tbody[@id="myTable"]/tr/td[2]'
		price_xpath = '//tbody[@id="myTable"]/tr/td[4]'
		shopping_date_xpath = '//div[@id="collapse4"]/table[3]/tbody/tr/td[4]'
		supermarket_xpath = '//div[@id="formPrincipal:content-template-consulta"]/div[1]/table[1]/thead/tr[2]/th/h4/b'
		
		itens = driver.find_elements(By.XPATH, item_xpath)
		amounts = driver.find_elements(By.XPATH, amount_xpath)
		prices = driver.find_elements(By.XPATH, price_xpath)
		supermarket = driver.find_element(By.XPATH, supermarket_xpath)
		
		driver.find_element(By.XPATH, '//div[@id="heading3"]/h4').click()
		sleep(0.5)
		shopping_date = driver.find_element(By.XPATH, shopping_date_xpath)
		shopping_date = shopping_date.text[:10].split("/")
		shopping_date = ("/").join(reversed(shopping_date))
		
		for item, amount, price in zip(itens, amounts, prices):
			registro = (0, item.text.strip(), amount.text[20:].strip(), price.text[18:].strip().replace(',','.'), supermarket.text.strip(), shopping_date)
			self.shopping_list.append(registro)
			# como id é autoincrement, não é necessário se preocupar com o valor, mas preencher 'default' não foi aceito
		

class DataBase: #CRUD
	def __init__(self):
		self.connection = connector.connect(
		host = os.environ["host"],
		user = os.environ["user"],
		password = os.environ["password"],
		database = os.environ["database"])
		self.cursor = self.connection.cursor()
   
	
	def close_connection(self):
		self.cursor.close()
		self.connection.close()  


	def create(self, shopping_list):
		for product in shopping_list:
			query = f"INSERT INTO compras VALUES {product}"
			self.cursor.execute(query)
			self.connection.commit()
		

	def read(self, query):
		self.cursor.execute(query)
		resultado = self.cursor.fetchall()
		self.close_connection()
		return  resultado
		
		
	def update(self):
		query = f"UPDATE compras SET item = 'Fernando R S Diniz' WHERE id = '62'"
		self.cursor.execute(query)
		self.connection.commit()
		self.close_connection()

		
	def delete(self):
		query = f"DELETE FROM compras WHERE id = '62'"
		self.cursor.execute(query)
		self.connection.commit()
		self.close_connection()


class Application:
	def __init__(self) -> None:
		pass
	
 	
	def insert_products_from_invoice(self, urls):
		for url in urls:
			invoice.create_shopping_list(url)
		query = f"SELECT count(*) FROM compras"
		initial_count = database.read(query)
		database.create(invoice.shopping_list)
		final_count = database.read(query)
		print(f"Foram incluídos {initial_count[0][0] - final_count[0][0]} itens.")


	def display_registred_products(self, query):
		products = database.read(query)
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


invoice = Invoice()
database = DataBase()
application = Application()


app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/read', methods=['POST'])
def read_products():
	# query = request.form['query']
	query = f"SELECT * FROM compras"
	page = application.display_registred_products(query)
	return page 

@app.route('/create', methods=['POST']) # https://portalsped.fazenda.mg.gov.br/portalnfce/sistema/qrcode.xhtml?p=31231171385637000434650120001654541120169211|2|1|1|818BF8A3F93CD1F95A46398B52B9CBE0FA1159F1
def create_products():
	urls = [request.form['url']]
	application.insert_products_from_invoice(urls)
	return "ok" # o problema estava no redirect!?





if __name__ == "__main__":
	app.run(host='0.0.0.0', port=1024, debug=True)
