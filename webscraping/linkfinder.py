import requests
from bs4 import BeautifulSoup

def links_finder(url):
    ''' return a list of all product link

    argument :
        -url : url of the catalogue
    '''
    links = []
    link_left = True
    page = 1
    while link_left == True:
        print(page)
        url_page = url + 'page-' + str(page) + '.html'
        response = requests.get(url_page)
        if response.ok:
            soupIndex = BeautifulSoup(response.text, "html.parser")
            divA = soupIndex.find_all('div', {'class': 'image_container'})
            for i in divA:
                a = i.find('a')
                link = a['href']
                links.append(url + link)
            page += 1
        else:
            link_left = False
            print('end')
    return links
