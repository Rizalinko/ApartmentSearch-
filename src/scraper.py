import urllib
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
from os import path


class ListingsScraper:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}


    arxiveDf = pd.DataFrame()

    def __init__(self, **kwargs):
        if 'debug' in kwargs:
            self.debug = kwargs['debug']
        elif 'release' in kwargs:
            self.debug = not kwargs['release']
        self.nrooms = kwargs['nrooms']
        if kwargs['balcony']:
            self.filter = 400
        self.prices = kwargs['rprice']

        self.arxiveListings = 'archiveListings_{}rooms_pricerange_{}_{}.pkl'.format(self.nrooms, self.prices[0], self.prices[1])
        if path.exists(self.arxiveListings):
            self.arxiveDf = pd.read_pickle(self.arxiveListings)

    def getArxiveDf(self):
        return self.arxiveDf

    def create_listing(self):
        # ToDo: add check by publication time

        aprts = {'address': [], 'price': [], 'links': []}

        page_num = 0
        while True:
            page_num += 1  # the result is the same whether page_num =0 or page_num = 1, therefore incrementing here for convinience

            homegate = 'https://www.homegate.ch/rent/real-estate/canton-zurich/matching-list?ep={}&ac={}&an={}&o=dateCreated-desc&&loc=geo-city-dietlikon%2Cgeo-city-dubendorf%2Cgeo-zipcode-8005%2Cgeo-zipcode-8008%2Cgeo-zipcode-8051&&ag={}&ah={}'.format(page_num, self.nrooms, self.filter,self.prices[0], self.prices[1])
            #homegate = 'https://www.homegate.ch/rent/real-estate/matching-list?ep={}&ac={}&loc=geo-city-dubendorf%2Cgeo-city-dietlikon%2Cgeo-zipcode-8005%2Cgeo-zipcode-8008%2Cgeo-zipcode-8051&ag={}&ah={}'.format(page_num, self.nrooms, self.filter,self.prices[0], self.prices[1])
            # comparis = 'https://en.comparis.ch/immobilien/result/list?requestobject=%7B%22DealType%22%3A10%2C%22SiteId%22%3A-1%2C%22RootPropertyTypes%22%3A%5B%5D%2C%22PropertyTypes%22%3A%5B%5D%2C%22RoomsFrom%22%3A%223%22%2C%22RoomsTo%22%3Anull%2C%22FloorSearchType%22%3A0%2C%22LivingSpaceFrom%22%3Anull%2C%22LivingSpaceTo%22%3Anull%2C%22PriceFrom%22%3A%221000%22%2C%22PriceTo%22%3A%221700%22%2C%22ComparisPointsMin%22%3A-1%2C%22AdAgeMax%22%3A-1%2C%22AdAgeInHoursMax%22%3Anull%2C%22Keyword%22%3A%22%22%2C%22WithImagesOnly%22%3Anull%2C%22WithPointsOnly%22%3Anull%2C%22Radius%22%3Anull%2C%22MinAvailableDate%22%3A%221753-01-01T00%3A00%3A00%22%2C%22MinChangeDate%22%3A%221753-01-01T00%3A00%3A00%22%2C%22LocationSearchString%22%3A%22dubendorf%2C%20dietlikon%2C%208051%22%2C%22Sort%22%3A%223%22%2C%22HasBalcony%22%3Afalse%2C%22HasTerrace%22%3Afalse%2C%22HasFireplace%22%3Afalse%2C%22HasDishwasher%22%3Afalse%2C%22HasWashingMachine%22%3Afalse%2C%22HasLift%22%3Afalse%2C%22HasParking%22%3Afalse%2C%22PetsAllowed%22%3Afalse%2C%22MinergieCertified%22%3Afalse%2C%22WheelchairAccessible%22%3Afalse%2C%22LowerLeftLatitude%22%3Anull%2C%22LowerLeftLongitude%22%3Anull%2C%22UpperRightLatitude%22%3Anull%2C%22UpperRightLongitude%22%3Anull%7D&page=0'
            print(homegate)
            response = get(homegate, headers=self.headers)
            print('Response from the website', response)

            html_soup = BeautifulSoup(response.text, 'html.parser')

            div_class_name = 'ListItem_item_1GcIZ ListItem_isFavouriteEnabled_1GRUr'
            house_containers = html_soup.find_all('div', class_=div_class_name)

            if len(house_containers) == 0:
                print('reached the empty page, number', page_num)
                break

            links = html_soup.find_all('a', class_='ListItem_itemLink_30Did ResultListPage_ListItem_n8HMf')
            for house, link in zip(house_containers, links):
                aprt_url = r'https://www.homegate.ch' + link.attrs['href']

                span_tmp = house.find_all('span')

                address = bytearray(span_tmp[-1].text, 'iso-8859-1').decode('utf8')
                if len(self.arxiveDf) and address in self.arxiveDf.values and aprt_url in self.arxiveDf.values:
                    break
                # if address.count('Ueberlandstr'):
                #     continue
                aprts['address'].append(address)
                aprts['price'].append(span_tmp[3].text.replace('â', '').replace(',', ''))

                aprts['links'].append(aprt_url)


            if page_num > 0 and self.debug:
                break
        return aprts

    def ListingsDf(self):
        # listings = self.ListingsScraper(release=False)
        apartments = self.create_listing()

        apartments['T_total_dectris'] = [0.] * len(apartments['address'])
        apartments['T_total_mellingen'] = [0.] * len(apartments['address'])
        apartments['T_mellingen'] = [0.] * len(apartments['address'])
        apartments['T_dectris'] = [0.] * len(apartments['address'])
        apartments['T_ks'] = [0.] * len(apartments['address'])
        apartments['T_bms'] = [0.] * len(apartments['address'])

        apartments['option'] = [False] * len(apartments['address']) # Values are true or false, depending on the commutes to ks/bms/dectris
        df = pd.DataFrame(apartments)
        return df

    def UpdateArchiveListings(self, apartments):

        # merge aprtments with arxiveListings
        if len(self.arxiveDf):
            pd.concat([apartments, self.arxiveDf]).to_pickle(self.arxiveListings)
        else:
            apartments.to_pickle(self.arxiveListings)
