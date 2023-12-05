from time import sleep
from flask import Flask, render_template, request, redirect
import time
import database_access
import scraping_script
# from dotenv import load_dotenv
# load_dotenv()

class Application:
	def __init__(self) -> None:
		pass
	
 	
	def insert_products_from_invoice(self, urls):
		initial_time = time.time()
		query = "SELECT count(*) FROM compras"
		initial_count = database.read(query)
		for url in urls:
			invoice.create_shopping_list(url)
			database.create(invoice.shopping_list)
		final_count = database.read(query)
		final_time = time.time()
		self.amount_of_inserts = f"Foram incluídos {final_count[0][0] - initial_count[0][0]} itens em {round(final_time - initial_time)} segundos."


	def display_registred_products(self, condition):
		query = f"SELECT * FROM compras WHERE produto LIKE '{condition[0]}' OR produto LIKE '{condition[1]}' ORDER BY dia DESC"
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


invoice = scraping_script.BeatifulSoupScraping()
database = database_access.DataBase()
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

@app.route('/create', methods=['POST'])
def create_products():
	urls = request.form['url']
	urls = urls.split(",")
	application.insert_products_from_invoice(urls)
	return f"{application.amount_of_inserts}" # o problema estava no redirect!?





if __name__ == "__main__":
	app.run(host='0.0.0.0', port=1024, debug=True)
