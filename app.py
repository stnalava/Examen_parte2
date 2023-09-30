from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient
import json
from flask import Flask, jsonify
from bson.json_util import dumps


driver = webdriver.Chrome()


driver.get('https://masmusika.com/categoria/instrumentos-musicales')


data = {'products': []}


guitar = driver.find_elements(By.CLASS_NAME, "product-inner")

data = []
for product in guitar:
    descr = product.find_element(by=By.CLASS_NAME, value="product-loop-title").text
    price = product.find_element(by=By.CLASS_NAME, value="price").text
    button = product.find_element(by=By.CLASS_NAME, value="add-links-wrap").text

    data.append({
        "descr": descr,
        "price": price,
        "button": button,
    })

with open('products.json', 'w') as f:
    json.dump(data, f)

driver.quit()


url = "mongodb+srv://stnalava9396:oPZgszTgMvBBRKhB@cluster0.hivc9iv.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
client = MongoClient(url)
db = client["MasMusika1"]
collection = db["guitar1"]

# Carga los datos del archivo .json
with open('products.json', 'r') as f:
    data = json.load(f)

collection.insert_many(data)

app = Flask(__name__)



@app.route('/')
def home():
    # Conexión a la base de datos
    url = "mongodb+srv://stnalava9396:oPZgszTgMvBBRKhB@cluster0.hivc9iv.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
    client = MongoClient(url)
    db = client["MasMusika1"]
    collection = db["guitar1"]

    data = list(collection.find())

    return dumps(data)

if __name__ == '__main__':
    app.run(debug=True)