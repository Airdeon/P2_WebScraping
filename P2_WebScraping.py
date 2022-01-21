import os
import requests
import csv
from bs4 import BeautifulSoup
from time import time
from webscraping.getdata import get_image_and_url, get_rating, get_product_info
from webscraping.linkfinder import links_finder

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
links = links_finder(URL_CATALOGUE)

# start reading all page and save data
for i in range(len(links)):
    print(str(i+1) + '/' + str(len(links)))
    resultRequest = requests.get(links[i])
    if resultRequest.ok:
        soup = BeautifulSoup(resultRequest.text, "html.parser")

        # get product_page_url
        productPageUrl = links[i]

        # get title
        title = soup.find('h1').text

        # get product_info in a list
        product_Info = get_product_info(soup)

        # get description
        if soup.find("div", {"id": "product_description"}):
            description = soup.find("div", {"id": "product_description"}).find_next('p').text
        else:
            description = ''

        # get review rating
        review_rating = get_rating(soup)

        # get category
        cat_style = soup.find('li', {'class': 'active'}).find_previous('a').text

        # get image url and save it
        image_url = get_image_and_url(soup, cat_style, title, IMAGES_FOLDER, URL_SITE)

        # create line for CSV file
        ligne_Csv = [
            productPageUrl,
            product_Info[0],
            title,
            product_Info[1],
            product_Info[2],
            product_Info[3],
            description,
            cat_style,
            review_rating,
            image_url
        ]

        # create link of CSV file
        csvlink = CSV_FOLDER + cat_style + '.csv'

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

# show statistic
end = time()
temps = int(end - start)
print(str(len(links)) + ' livre récupéré en ' + str(temps) + 's')
