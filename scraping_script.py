from bs4 import BeautifulSoup as bs
import requests


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