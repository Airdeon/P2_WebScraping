import os
import re
import requests
import csv
import urllib.request
from bs4 import BeautifulSoup
from time import time

# url
URL_SITE = "http://books.toscrape.com/"
URL_CATALOGUE = "http://books.toscrape.com/catalogue/"

# Page to scan
NUMBER_OF_PAGE = 50

# header for csv file
EN_TETE = [
    "product_page_url",
    "universal_ product_code (upc)",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url"
]

# Link of folder
CSV_FOLDER = 'CSV/'
IMAGES_FOLDER = 'Images/'
if not os.path.exists(CSV_FOLDER):
    os.mkdir(CSV_FOLDER)
if not os.path.exists(IMAGES_FOLDER):
    os.mkdir(IMAGES_FOLDER)

# start time counter
start = time()

# make a list of all product page link
links = []
for i in range(NUMBER_OF_PAGE):
    # url of catalogue page
    url_C = URL_CATALOGUE + 'page-' + str(i+1) + '.html'
    # Find all url of product per page
    response = requests.get(url_C)
    if response.ok:
        soupIndex = BeautifulSoup(response.text, "html.parser")
        divA = soupIndex.find_all('div', {'class': 'image_container'})
        for i in divA:
            a = i.find('a')
            link = a['href']
            links.append(URL_CATALOGUE + link)

# start reading all page and save data
for i in range(len(links)):
    print(str(i+1) + '/' + str(len(links)))
    resultRequest = requests.get(links[i])
    if resultRequest.ok:
        soup = BeautifulSoup(resultRequest.text, "html.parser")

        # product_page_url
        productPageUrl = links[i]

        # title
        title = soup.find('h1').text

        product_Info = soup.find_all('tr')
        upc = ""
        PriceTax = ""
        PriceNoTax = ""
        numberAvailable = ""

        for i in product_Info:
            # universal_ product_code (upc)
            if i.find('th', string='UPC'):
                ucp = i.find('td').text

            # price_including_tax
            if i.find('th', string='Price (incl. tax)'):
                PriceTax = i.find('td').text[1:]

            # price_excluding_tax
            if i.find('th', string='Price (excl. tax)'):
                PriceNoTax = i.find('td').text[1:]

            # availability
            if i.find('th', string='Availability'):
                numberAvailableText = i.find('td').text
                numberAvailable = int(''.join(filter(str.isdigit, numberAvailableText)))

        # description
        try:
            description = soup.find("div", {"id": "product_description"}).find_next('p').text
        except:
            description = ''

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

        # image_URL
        try:
            i_url = soup.find("img", {'alt': title})
            image_url = URL_SITE + i_url['src'][5:]
        except:
            image_url = ''

        # category
        cat_style = soup.find('li', {'class': 'active'}).find_previous('a').text

        # create line for CSV file
        ligne_Csv = [
            productPageUrl,
            ucp,
            title,
            PriceTax,
            PriceNoTax,
            numberAvailable,
            description,
            cat_style,
            real_review_rating,
            image_url
        ]

        # create link of CSV file and image folder
        csvlink = CSV_FOLDER + cat_style + '.csv'
        images_folder_link = IMAGES_FOLDER + cat_style + '/'
        # if title is too long, make it shorter
        title_for_link = re.sub(r"[^a-zA-Z0-9 ]", "", title) # remove all special character 
        if len(title) > 20:
            short_title = title_for_link[0:20]
        else:
            short_title = title_for_link
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
        if image_url != '':
            if not os.path.exists(images_folder_link):
                os.mkdir(images_folder_link)
            urllib.request.urlretrieve(image_url, imageslink)

# show statistic
end = time()
temps = int(end - start)
print(str(len(links)) + ' livre récupéré en ' + str(temps) + 's')
