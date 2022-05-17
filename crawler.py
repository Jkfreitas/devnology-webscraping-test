from flask import Flask
from playwright.sync_api import sync_playwright
from operator import itemgetter
import json

app = Flask(__name__)

def busca():
    with sync_playwright() as p:

        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops")

        #Capturando modelo, link e estrelas.
        all_data = []
        num = page.locator('.title').count() 
        n = 0

        for i in range(0, num, 1):
            model = page.get_attribute('.title >> nth=' + str(n), 'title')
            link = page.get_attribute('.title >> nth=' + str(n), 'href')
            stars = page.get_attribute('p[data-rating] >> nth=' + str(n), 'data-rating')
            
            n = n+1
            
            all_data.append({   "model":model,
                                "link":"https://webscraper.io" + link,
                                "classification": stars + " star(s)"})

        #Capturando preço, descrição e reviews
        price = page.locator('h4[class="pull-right price"]').all_text_contents()
        description = page.locator('p[class="description"]').all_text_contents()
        reviews = page.locator('p[class="pull-right"]').all_text_contents() 

        for i in range(0, len(price), 1):
            
            all_data[i]["reviews"] = reviews[i]
            all_data[i]["description"] = description[i]
            all_data[i]["price"] = price[i]
            
        lenovo_data = []

        for i in range(0, len(all_data), 1):
            if ("Lenovo" in all_data[i]["model"]) or ("ThinkPad" in all_data[i]["model"]):
                lenovo_data.append(all_data[i])

        lenovo_data.insert(0, {"occurrences": str(len(lenovo_data)) + " results" }) 

        data = json.dumps(lenovo_data, indent="\t")
        browser.close()

    return data

@app.route("/")
def get_lenovo():
    dados = busca()
    return dados

app.run(debug=True)