import os
import re
import urllib.request


def get_product_info(soup_object):
    ''' return a list from soup object with in order : upc, Price include tax, price exclude tax, Availability

    argument :
        -soup_object : BeautifulSoup object of the page
    '''
    product_soup = soup_object.find_all('tr')
    product_info = []
    for i in product_soup:
        # universal_ product_code (upc)
        if i.find('th', string='UPC'):
            product_info.append(i.find('td').text)
        else:
            product_info.append('')

        # price_including_tax
        if i.find('th', string='Price (incl. tax)'):
            product_info.append(i.find('td').text[1:])
        else :
            product_info.append('')

        # price_excluding_tax
        if i.find('th', string='Price (excl. tax)'):
            product_info.append(i.find('td').text[1:])
        else :
            product_info.append('')

        # availability
        if i.find('th', string='Availability'):
            numberAvailableText = i.find('td').text
            product_info.append(int(''.join(filter(str.isdigit, numberAvailableText))))
        else :
            product_info.append('')

    return product_info

def get_rating(soup_object):
    ''' return rating of book in string with format "x/5"
    argument :
        -soup_object : BeautifulSoup object of the page
    '''
    rating = soup_object.find("p", {"class": "star-rating"})
    review_rating = rating['class']
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
            real_review_rating = ''
    return real_review_rating

def get_image_and_url(soup_object, style, title, images_folder, url_site):
    ''' return image url and save this image on folder with name of book category
    argument :
        -soup_object : BeautifulSoup object of the page
        -style : book category
        -title : book title
        -image_folder : link of image folder
        -url_site : url of the main website
    '''
    if soup_object.find("img", {'alt': title}):
        i_url = soup_object.find("img", {'alt': title})
        image_url = url_site + i_url['src'][5:]
        images_folder_link = images_folder + style + '/'
        if not os.path.exists(images_folder_link):
            os.mkdir(images_folder_link)
        # make title good for a link
        title_for_link = re.sub(r"[^a-zA-Z0-9 ]", "", title) # remove all special character
        if len(title) > 20:
            short_title = title_for_link[0:20] # cut after 20 character if it's too long
        else:
            short_title = title_for_link
        imageslink = images_folder_link + '/' + short_title + '.jpg'
        # save image.jpg
        urllib.request.urlretrieve(image_url, imageslink)
    else:
        image_url = ''
    return image_url
