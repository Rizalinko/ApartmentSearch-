import urllib
from bs4 import BeautifulSoup
import requests
import requests
from requests import get
import pandas as pd
from os import path
import time
import selenium_test
import selenium
import datetime


from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select


import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='comparis.log',level=logging.DEBUG)

comparis = 'https://en.comparis.ch/immobilien/result/list?requestobject=%7B%22DealType%22%3A10%2C%22SiteId%22%3A-1%2C%22RootPropertyTypes%22%3A%5B%5D%2C%22PropertyTypes%22%3A%5B%5D%2C%22RoomsFrom%22%3A%223%22%2C%22RoomsTo%22%3Anull%2C%22FloorSearchType%22%3A0%2C%22LivingSpaceFrom%22%3Anull%2C%22LivingSpaceTo%22%3Anull%2C%22PriceFrom%22%3A%221000%22%2C%22PriceTo%22%3A%221800%22%2C%22ComparisPointsMin%22%3A-1%2C%22AdAgeMax%22%3A-1%2C%22AdAgeInHoursMax%22%3Anull%2C%22Keyword%22%3A%22%22%2C%22WithImagesOnly%22%3Anull%2C%22WithPointsOnly%22%3Anull%2C%22Radius%22%3Anull%2C%22MinAvailableDate%22%3A%221753-01-01T00%3A00%3A00%22%2C%22MinChangeDate%22%3A%221753-01-01T00%3A00%3A00%22%2C%22LocationSearchString%22%3A%22dubendorf%2C%20dietlikon%2C%208051%2C%208005%2C%208008%22%2C%22Sort%22%3A3%2C%22HasBalcony%22%3Afalse%2C%22HasTerrace%22%3Afalse%2C%22HasFireplace%22%3Afalse%2C%22HasDishwasher%22%3Afalse%2C%22HasWashingMachine%22%3Afalse%2C%22HasLift%22%3Afalse%2C%22HasParking%22%3Afalse%2C%22PetsAllowed%22%3Afalse%2C%22MinergieCertified%22%3Afalse%2C%22WheelchairAccessible%22%3Afalse%2C%22LowerLeftLatitude%22%3Anull%2C%22LowerLeftLongitude%22%3Anull%2C%22UpperRightLatitude%22%3Anull%2C%22UpperRightLongitude%22%3Anull%7D&page=0'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

message = 'Gruezi, Wir sind eine Paar, die sehr an Ihrer Wohnung interessiert sind und würden uns über einen Besichtigungstermin freuen. \n Grüsse, Ramun and Rizalina'
# '\n\nFür English: 0762751992 \nFür Deutsch: 0765038724 \nGrüsse, Ramun and Rizalina'

user_data_original = {'Firstname': 'Ramun', 'LastName': 'Benedetti', 'Email': 'rizalinko@gmail.com',
                      'Phone': '0762751992',
                      'Message': message}

user_data_comparis = {'ContactFullName': 'Ramun Benedetti', 'ContactEmail': 'rizalinko@gmail.com', 'ContactPhoneNumber': '0762751992',
                 'ContactMessage': message}

opts = Options()
opts.set_headless()
browser = Firefox(options=opts)

debug = False
try:
    f2 = open('comparis_listings', 'r')
    old_links = f2.readlines()
    for idx in range(len(old_links)):
        old_links[idx] = old_links[idx].replace('\n', '')
    f2.close()
except FileNotFoundError:
    old_links = []

def get_last_comparis():

    f = open('comparis_listings', 'a')
    comp_links = []
    a_class_name= 'css-1ogf9b9 excbu0j4'
    response = get(comparis, headers=headers)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    links = html_soup.find_all('a', class_= a_class_name)
    for link in links:
        if len(link.attrs['href']) == 1:
            links.remove(link)
            continue

        url = 'https://en.comparis.ch/' + link.attrs['href']

        if url in old_links:
            continue

        comp_links.append(url)
        old_links.append(url)
        f.write(url+'\n')
    f.close()
    return comp_links


def fillApply(user_data, submit_button_name):
    for key in user_data.keys():
        form = browser.find_elements_by_id(key)
        form[0].clear()
        form[0].send_keys(user_data[key])

    # button = browser.find_elements_by_id(submit_button_name)
    button = browser.find_elements_by_class_name(submit_button_name)
    button[0].click()
    return

def ClickOnOriginalLink(url):
    browser.get(url)

    try:
        submit_button_name = 'btnSendEmail'
        fillApply(user_data_original, submit_button_name)
        logging.info('Clicked ' + url)
    except IndexError:
        logging.warning('Ooops.. Looks like the listing is already gone from original website')
        return
    return

def ClickOnLinkComparis(url):
    browser.get(url)

    # try to filll the form contact adviser directly
    try:
        submit_button_name = 'icon-right.expanded.zero-margin.hf-contact-form-button.button'
        fillApply(user_data_comparis, submit_button_name)
        logging.info('Clicked ' + url)
        return
    except IndexError:
        logging.info('Did not find the form to contact advisor directly. Looking for follow link')

        redirect_link = browser.find_elements_by_class_name('follow-link')
        if redirect_link[0].text.count('homegate'):
            logging.warning('Originally posted on homegate. This is being taken care of in another programm')
            return
        if redirect_link[0].text.count('anibis'):
            logging.warning('Originally posted on anibis. Need to login to apply')
            return

        listnig_id = url.split('/')[-1]
        redirect_link = 'https://www.comparis.ch/immobilien/redirect/tooriginalad?adId={}'.format(listnig_id)
        ClickOnOriginalLink(redirect_link)


if __name__=="__main__":

    if not debug:
        while True:
            try:
                links = get_last_comparis()
            except requests.exceptions.ConnectionError:
                time.sleep(200)
            for link in links:
                logging.info('Trying to apply on ' + link)
                try:
                    ClickOnLinkComparis(link)
                    time.sleep(60)
                except selenium.common.exceptions.WebDriverException:
                    # pperhaps, connection is temporally lost, therefore sleep a bit
                    time.sleep(200)
            if len(links) == 0:
                logging.info('{}: No new apartments'.format(datetime.datetime.now()))
            time.sleep(300)

    else:
        link = 'https://www.comparis.ch/immobilien/marktplatz/details/show/23370397'
        selenium_test.ClickOnLinkComparis(link)
