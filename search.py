# -*- coding: utf-8 -*-
import pandas as pd
import datetime
import time
import scraper
import route_planner
import analyse_search

import selenium_test

performsearch = True
ifCheckCommute = False
ifapply = True


if __name__ == '__main__':
    scraper = scraper.ListingsScraper(release=False, nrooms=3, rprice=(1200,1750), balcony=True)

    if performsearch:

        while True:
            apartments = scraper.ListingsDf()
            if ifCheckCommute:
                apartments = route_planner.EstimateCommuteTime(apartments)
                apartments = route_planner.evaluateCommutes(apartments)
            scraper.UpdateArchiveListings(apartments)

            if ifapply:
                if len(apartments)==0:
                    print('{}: No new apartments'.format(datetime.datetime.now()))
                for link in apartments['links']:
                    selenium_test.clickOnlinkHomegate(link)
                    time.sleep(60)
            else:
                break
            time.sleep(300)

    else:
        apartments = scraper.getArxiveDf()
        apartments = route_planner.evaluateCommutes(apartments)

    if not ifapply:
        analyse_search.PrintOptions(apartments, noptions = 'all')

