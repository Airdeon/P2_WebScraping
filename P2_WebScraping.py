import requests
import csv
import os
import urllib.request
from bs4 import BeautifulSoup

urlSite = "http://books.toscrape.com/"
urlCatalogue = "http://books.toscrape.com/catalogue/"

# Link of folder
CSV_FOLDER = 'output CSV/'
IMAGES_FOLDER = 'Images/'
if not os.path.exists(CSV_FOLDER):
    os.mkdir(CSV_FOLDER)
if not os.path.exists(IMAGES_FOLDER):
    os.mkdir(IMAGES_FOLDER)

EN_TETE = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]

# make a list of all product page link
links = []
for i in range(4):
    # url of catalogue page
    url_C = urlCatalogue + 'page-' + str(i+1) + '.html'
    # Find all url of product per page 
    response = requests.get(url_C)
    if response.ok:
        soupIndex = BeautifulSoup(response.text, "html.parser")
        divA = soupIndex.find_all('div', {'class': 'image_container'})
        for l in divA:
            a = l.find('a')
            link = a['href']
            print(link)
            links.append(urlCatalogue + link)

print(len(links))


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
        review_rating = rR['class']
        match review_rating[1]:
            case 'One':
                real_review_rating = '1/5'
            case 'Two':
                real_review_rating = '2/5'
            case 'Three':
                real_review_rating = '3/5'
            case 'Four':
                real_review_rating = '4/5'
            case 'Five':
                real_review_rating = '5/5'
            case _:
                real_review_rating = '1/5'
        print(real_review_rating)

        # image_URL
        i_url = soup.find("img", {'alt': title})
        image_url = urlSite + i_url['src'][5:]
        print(image_url)

        # category
        cat_style = soup.find('li', {'class': 'active'}).find_previous('a').text
        print(cat_style)
        
        ligne_Csv = [productPageUrl, ucp, title, PriceTax, PriceNoTax, numberAvailable, description, cat_style, real_review_rating, image_url]

        csvlink = CSV_FOLDER + cat_style + '.csv'
        images_folder_link = IMAGES_FOLDER + cat_style + '/'
        if len(title) > 21:
            short_title = title[0:20].replace(':', ' ')
        else:
            short_title = title.replace(':', ' ')
        imageslink = IMAGES_FOLDER + cat_style + '/' + short_title + '.jpg'

        # write on csv file if exist or make it and write header before data
        if not os.path.exists(csvlink):
            with open(csvlink, 'w', newline='', encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(EN_TETE)
                writer.writerow(ligne_Csv)
        else:
            with open(csvlink, 'a', newline='', encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(ligne_Csv)
        
        # save image.jpg
        if not os.path.exists(images_folder_link):
            os.mkdir(images_folder_link)
        urllib.request.urlretrieve(image_url, imageslink)
