import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find('h1')
    print(title.text)
    product_Info = soup.find_all('tr')
    upc = ""
    PriceTax = ""
    PriceNoTax = ""
    numberAvailable = ""

    for i in product_Info:
        if i.find('th', string='UPC'):
            ucp = i.find('td').text
            print(ucp)
        if i.find('th', string='Price (incl. tax)'):
            PriceTax = i.find('td').text
            print(PriceTax)
        if i.find('th', string='Price (excl. tax)'):
            PriceNoTax = i.find('td').text
            print(PriceNoTax)
        if i.find('th', string='Availability'):
            numberAvailableText = i.find('td').text
            numberAvailable = int
            print(numberAvailable)
