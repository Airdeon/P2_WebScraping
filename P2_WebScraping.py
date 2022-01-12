import requests
from bs4 import BeautifulSoup

urlSite = "http://books.toscrape.com"
urlPage = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

response = requests.get(urlPage)

if response.ok:
    soup = BeautifulSoup(response.text, "html.parser")
    
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