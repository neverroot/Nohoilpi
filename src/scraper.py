from bs4 import BeautifulSoup
import requests
from os.path import join
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle

from util import *


try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

class Schedule():
    def __init__(self, games):
        self.games_played = games
    
    def week(self, n):
        return [g for g in self.games_played if int(g.week_num) == n]
    

class GameData():
    def __init__(self, data):        
        self.__dict__.update(data)
    
    def __repr__(self):
        return f"{self.winner} @ {self.loser}"

class Scraper():
    def __init__(self):
        self.cached_dir = "cached_pages"
        self.options = Options()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def scrape_schedule(self):
        url = "https://www.pro-football-reference.com/years/2021/games.htm"
        file = os.path.join(self.cached_dir, "schedule_cache")
        soup = self.get_soup(file, url)

        # Get table and body with games data in it
        table = soup.find("table", attrs={"id":"games"})
        tbody = table.find("tbody")

        schedule = []
        # for every row in the body of the table
        for row in tbody.find_all("tr"):
            row_data = {}
            # for every column in the row
            for col in row.find_all("th", {"class":"right", "data-stat":"week_num"}):
                row_data[col['data-stat']] = col.text
            for col in row.find_all("td"):
                row_data[col['data-stat']] = col.text
                # see if there is an aref
                try:
                    a = col.find_all("a")
                    assert(len(a) == 1)
                    link = a[0]['href']
                    row_data[col['data-stat']+'_link'] = link
                except Exception as e:
                    continue
            if row_data:
                gd = GameData(row_data)
                schedule.append(gd)

        return Schedule(schedule)

    # return the BeautifulSoup depending on if page source was cached or needs to be fetched
    def get_soup(self, file, url):
        # check if the file was cached, if not go get the page
        if page_cached(file):
            print(f"[-] Getting cached file from {file}")
            with open(file, 'rb') as f:
                page = f.read().decode("utf-8")
            return BeautifulSoup(page, 'html.parser')
        else:
            print(f"[-] File not cached. Fetching")
            self.driver.get(url)
            with open(file, 'w+') as f:
                f.write(self.driver.page_source)
            print(f"[-] Cached to {file}")
            return BeautifulSoup(self.driver.page_source, 'html.parser')


s = Scraper()
schedule = s.scrape_schedule()
print(schedule.week(1))

