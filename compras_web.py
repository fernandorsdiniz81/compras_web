from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from time import sleep
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

class NotaFiscal:
    def __init__(self):
        self.options = Options()
        self.options.page_load_strategy = 'normal'
        self.options.add_argument("--blink-settings=imagesEnabled=false") # no images loaded
        self.options.add_argument("--headless") # browser is invisible
        self.lista_de_compras = []
            
    def gerar_lista_de_compras(self, url):
        driver = webdriver.Edge(options=self.options)
        driver.get(url)
        sleep(2)
        
        item_xpath = '//tbody[@id="myTable"]/tr/td[1]/h7'
        quantidade_xpath = '//tbody[@id="myTable"]/tr/td[2]'
        valor_xpath = '//tbody[@id="myTable"]/tr/td[4]'
        data_da_compra_xpath = '//div[@id="collapse4"]/table[3]/tbody/tr/td[4]'
        supermercado_xpath = '//div[@id="formPrincipal:content-template-consulta"]/div[1]/table[1]/thead/tr[2]/th/h4/b'
        
        itens = driver.find_elements(By.XPATH, item_xpath)
        quantidades = driver.find_elements(By.XPATH, quantidade_xpath)
        valores = driver.find_elements(By.XPATH, valor_xpath)
        supermercado = driver.find_element(By.XPATH, supermercado_xpath)
        
        driver.find_element(By.XPATH, '//div[@id="heading3"]/h4').click()
        sleep(0.5)
        data_da_compra = driver.find_element(By.XPATH, data_da_compra_xpath)
        data_da_compra = data_da_compra.text[:10].split("/")
        data_da_compra = ("/").join(reversed(data_da_compra))
        
        for item, quantidade, valor in zip(itens, quantidades, valores):
            registro = (0, item.text.strip(), quantidade.text[20:].strip(), valor.text[18:].strip().replace(',','.'), supermercado.text.strip(), data_da_compra)
            self.lista_de_compras.append(registro)
            # como id é autoincrement, não é necessário se preocupar com o valor e preencher 'default' não foi aceito
        

class BancoDeDados:
    def __init__(self):
        self.conexao = mysql.connector.connect(
        host = os.getenv("host"),
        user = os.getenv("user"),
        password = os.getenv("password"),
        database = os.getenv("database"))
        self.cursor = self.conexao.cursor()
       

    def creat(self, lista_de_compras):
        for produto in lista_de_compras:
            comando = f"INSERT INTO compras VALUES {produto}"
            self.cursor.execute(comando)
            self.conexao.commit()
        self.cursor.close()
        self.conexao.close()

    def read(self):
        comando = "SELECT * FROM compras"
        self.cursor.execute(comando)
        resultado = self.cursor.fetchall()
        self.cursor.close()
        self.conexao.close()
        print(resultado)
        
    def update(self):
        comando = "UPDATE compras SET item = 'Fernando R S Diniz' WHERE id = '62'"
        self.cursor.execute(comando)
        self.conexao.commit()
        self.cursor.close()
        self.conexao.close()
        
    def delete(self):
        comando = "DELETE FROM compras WHERE id = '62'"
        self.cursor.execute(comando)
        self.conexao.commit()
        self.cursor.close()
        self.conexao.close()




### App #########################################

nota_fiscal = NotaFiscal()
salvar_BD = BancoDeDados()

# Preencher URLs aqui:
urls = [""]

for url in urls:
    nota_fiscal.gerar_lista_de_compras(url)
    
print(nota_fiscal.lista_de_compras)
salvar_BD.creat(nota_fiscal.lista_de_compras)

