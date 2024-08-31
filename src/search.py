# -*- coding: utf-8 -*-
# import pandas as pd
import datetime
import time
import scraper
import route_planner
from apt_search import analyse_search

import seleniumClicker as scliker

performsearch = True
loadDB = True
ifCheckCommute = False
apply = True


if __name__ == '__main__':
    scraper = scraper.ListingsScraper(release=False, nrooms=3, rprice=(1200, 1750), balcony=True)

    if performsearch:

        while True:
            apartments = scraper.ListingsDf()
            if ifCheckCommute:
                apartments = route_planner.EstimateCommuteTime(apartments)
                apartments = route_planner.evaluateCommutes(apartments)
            scraper.UpdateArchiveListings(apartments)

            if apply:
                if len(apartments)==0:
                    print('{}: No new apartments'.format(datetime.datetime.now()))
                for link in apartments['links']:
                    scliker.clickOnlinkHomegate(link)
                    time.sleep(60)
            else:
                break
            time.sleep(300)

    elif loadDB:
        apartments = scraper.getArxiveDf()
        apartments = route_planner.evaluateCommutes(apartments)

    if not apply:
        analyse_search.PrintOptions(apartments, noptions ='all')

