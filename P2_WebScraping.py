import requests
import csv
from bs4 import BeautifulSoup

urlSite = "http://books.toscrape.com/"
urlPage = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

en_tete = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]

# Find all url of product page 
response = requests.get(urlSite)
if response.ok:
    links = []
    soupIndex = BeautifulSoup(response.text, "html.parser")
    divA = soupIndex.find_all('div', {'class': 'image_container'})
    for l in divA:
        a = l.find('a')
        link = a['href']
        links.append(urlSite + link)

# open csv file in write mode
with open('Book.csv', 'w', encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(en_tete)

    # start reading all page and save data
    for i in range(len(links)):
        print(links[i])
        resultRequest = requests.get(links[i])
        if resultRequest.ok:
            soup = BeautifulSoup(resultRequest.text, "html.parser")

            # product_page_url
            productPageUrl = links[i]

            # title
            title = soup.find('h1').text
            print(title)

            product_Info = soup.find_all('tr')
            upc = ""
            PriceTax = ""
            PriceNoTax = ""
            numberAvailable = ""

            for i in product_Info:
                # universal_ product_code (upc)
                if i.find('th', string='UPC'):
                    ucp = i.find('td').text
                    print(ucp)

                # price_including_tax
                if i.find('th', string='Price (incl. tax)'):
                    PriceTax = i.find('td').text
                    print(PriceTax)

                # price_excluding_tax
                if i.find('th', string='Price (excl. tax)'):
                    PriceNoTax = i.find('td').text
                    print(PriceNoTax)

                # availability
                if i.find('th', string='Availability'):
                    numberAvailableText = i.find('td').text
                    numberAvailable = int(''.join(filter(str.isdigit, numberAvailableText)))
                    print(numberAvailable)

            # description
            description = soup.find("div", {"id": "product_description"}).find_next('p').text
            print(description)

            # review rating
            rR = soup.find("p", {"class": "star-rating"})
            reviewRating = rR['class']
            match reviewRating[1]:
                case 'One':
                    realReviewRating = '1/5'
                case 'Two':
                    realReviewRating = '2/5'
                case 'Three':
                    realReviewRating = '3/5'
                case 'Four':
                    realReviewRating = '4/5'
                case 'Five':
                    realReviewRating = '5/5'
                case _:
                    realReviewRating = '1/5'
            print(realReviewRating)

            # image_URL
            i_url = soup.find("img", {'alt': title})
            image_url = urlSite + i_url['src'][5:]
            print(image_url)

            # category
            cat_Style = soup.find('li', {'class': 'active'}).find_previous('a').text
            print(cat_Style)

            ligne_Csv = [productPageUrl, ucp, title, PriceTax, PriceNoTax, numberAvailable, description, cat_Style, realReviewRating, image_url]
            writer.writerow(ligne_Csv)

