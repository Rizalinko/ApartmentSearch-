import urllib
from bs4 import BeautifulSoup
from requests import get

class ListingsScraper:

    # @property
    def create_listing(self):
        # ToDo: add check by publication time

        aprts = {'address': [], 'price': [], 'links': []}

        page_num = 0
        while True:
            page_num += 1  # the result is the same whether page_num =0 or page_num = 1, therefore incrementing here for convinience

            homegate = 'https://www.homegate.ch/rent/real-estate/canton-zurich/matching-list?ep={}&ac=3&o=dateCreated-desc&ah=1700'.format(
                page_num)
            # homegate = 'https://www.homegate.ch/rent/real-estate/zip-8051/matching-list?ac=2&ah=2000'
            response = get(homegate, headers=headers)
            print('Response from the website', response)

            html_soup = BeautifulSoup(response.text, 'html.parser')

            div_class_name = 'ListItem_item_1GcIZ ListItem_isFavouriteEnabled_1GRUr'
            house_containers = html_soup.find_all('div', class_=div_class_name)

            if len(house_containers) == 0:
                print('reached the empty page, number', page_num)
                break

            for house in house_containers:
                span_tmp = house.find_all('span')

                aprts['address'].append(bytearray(span_tmp[-1].text, 'iso-8859-1').decode('utf8'))
                aprts['price'].append(span_tmp[3].text.replace('â', '').replace(',', ''))

            links = html_soup.find_all('a', class_='ListItem_itemLink_30Did ResultListPage_ListItem_n8HMf')
            for link in links:
                aprts['links'].append(r'https://www.homegate.ch' + link.attrs['href'])

            if page_num>0:
                break

        print(aprts['links'][5], aprts['address'][5])

        return aprts
