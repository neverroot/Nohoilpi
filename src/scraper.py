from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle
import util

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

NUM_OF_WEEKS = 18


class Schedule():
    def __init__(self, games):
        self.time_fetched = util.get_dt_string(util.get_today())
        self.games = games
        # makes each week an attribute ex. schedule.week_1
        self.__dict__.update(self.get_weeks())
        self.__dict__ = util.remove_empty_kvs(self.__dict__)

    def __str__(self):
        res = ""
        for k,v in self.__dict__.items():
            if k == 'games':
                continue
            else:
                res += f"{k} : {v}\n"
        return res

    def get_weeks(self):
        weeks = {f'week_{i+1}':[] for i in range(NUM_OF_WEEKS)}
        for game in self.games:
            weeks[f'week_{game.week_num}'].append(game)
        return weeks

    def print_list_of_games(self, lgames):
        print(f"[-] Games for Week {lgames[0].week_num}")
        print(f"[-] {'='*75}")
        for i,game in enumerate(lgames):
            print(f"[-] Game {i+1} - {game} | {util.get_dt_string(game.gt_dt)}")
        print(f"[-] {'='*75}")

    def week(self, n):
        return getattr(self,f"week_{n}")

    def get_curr_week_num(self):
        curr = util.get_curr_dt()
        for i in range(NUM_OF_WEEKS):
            last_game_of_week = getattr(self,f"week_{i+1}")[-1]
            if last_game_of_week.gt_dt > curr:
                return int(last_game_of_week.week_num)


class TeamData():
    def __init__(self, data):
        self.__dict__.update(data)
        self.__dict__ = util.remove_empty_kvs(self.__dict__)

    def __repr__(self):
        return self.name

    def __str__(self):
        res = ""
        for k,v in self.__dict__.items():
            res += f"{k} : {v}\n"
        return res


class GameData():
    def __init__(self, data):
        self.__dict__.update(data)

    def __repr__(self):
        return f"{self.winner} @ {self.loser}"
    
    def __str__(self):
        res = ""
        for k,v in self.__dict__.items():
            res += f"{k} : {v}\n"
        return res


GET_FULL_NAME  = 0
GET_TEAM_URL   = 1
GET_SHORT_NAME = 2

NUM_OF_TEAMS = 32

class Scraper():
    def __init__(self, always_update=False):
        self.always_update = always_update
        self.cached_dir = "cached_pages"
        self.teams = ['Tampa Bay Buccaneers', 'Dallas Cowboys', 'Philadelphia Eagles', 'Atlanta Falcons', 'Carolina Panthers', 'New York Jets', 'Los Angeles Chargers', 'Washington Football Team', 'Pittsburgh Steelers', 'Buffalo Bills', 'Cincinnati Bengals', 'Minnesota Vikings', 'Seattle Seahawks', 'Indianapolis Colts', 'Arizona Cardinals', 'Tennessee Titans', 'San Francisco 49ers', 'Detroit Lions', 'Houston Texans', 'Jacksonville Jaguars', 'Kansas City Chiefs', 'Cleveland Browns', 'Denver Broncos', 'New York Giants', 'New Orleans Saints', 'Green Bay Packers', 'Miami Dolphins', 'New England Patriots', 'Los Angeles Rams', 'Chicago Bears', 'Las Vegas Raiders', 'Baltimore Ravens']
        self.teams_tri = [('Tampa Bay Buccaneers', '/teams/tam/2021.htm', 'tam'), ('Dallas Cowboys', '/teams/dal/2021.htm', 'dal'), ('Philadelphia Eagles', '/teams/phi/2021.htm', 'phi'), ('Atlanta Falcons', '/teams/atl/2021.htm', 'atl'), ('Carolina Panthers', '/teams/car/2021.htm', 'car'), ('New York Jets', '/teams/nyj/2021.htm', 'nyj'), ('Los Angeles Chargers', '/teams/sdg/2021.htm', 'sdg'), ('Washington Football Team', '/teams/was/2021.htm', 'was'), ('Pittsburgh Steelers', '/teams/pit/2021.htm', 'pit'), ('Buffalo Bills', '/teams/buf/2021.htm', 'buf'), ('Cincinnati Bengals', '/teams/cin/2021.htm', 'cin'), ('Minnesota Vikings', '/teams/min/2021.htm', 'min'), ('Seattle Seahawks', '/teams/sea/2021.htm', 'sea'), ('Indianapolis Colts', '/teams/clt/2021.htm', 'clt'), ('Arizona Cardinals', '/teams/crd/2021.htm', 'crd'), ('Tennessee Titans', '/teams/oti/2021.htm', 'oti'), ('San Francisco 49ers', '/teams/sfo/2021.htm', 'sfo'), ('Detroit Lions', '/teams/det/2021.htm', 'det'), ('Houston Texans', '/teams/htx/2021.htm', 'htx'), ('Jacksonville Jaguars', '/teams/jax/2021.htm', 'jax'), ('Kansas City Chiefs', '/teams/kan/2021.htm', 'kan'), ('Cleveland Browns', '/teams/cle/2021.htm', 'cle'), ('Denver Broncos', '/teams/den/2021.htm', 'den'), ('New York Giants', '/teams/nyg/2021.htm', 'nyg'), ('New Orleans Saints', '/teams/nor/2021.htm', 'nor'), ('Green Bay Packers', '/teams/gnb/2021.htm', 'gnb'), ('Miami Dolphins', '/teams/mia/2021.htm', 'mia'), ('New England Patriots', '/teams/nwe/2021.htm', 'nwe'), ('Los Angeles Rams', '/teams/ram/2021.htm', 'ram'), ('Chicago Bears', '/teams/chi/2021.htm', 'chi'), ('Las Vegas Raiders', '/teams/rai/2021.htm', 'rai'), ('Baltimore Ravens', '/teams/rav/2021.htm', 'rav')]        

    def initialize(self):
        self.options = Options()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def name_translate(self, full_name):
        for t in self.teams_tri:
            if full_name == t[GET_FULL_NAME]:
                return t[GET_SHORT_NAME]

    def parse_team_info(self, team_soup):
        def disgusting_parsing(d):
            # split record into more key-value pairs
            record = d['record']
            d['record'] = record.split(',')[0]
            d['division_pos'] = record[len(d['record'])+1:].split("in")[0].strip()
            d['division'] = record.split("\n")[1].strip()
            # leave d['coach'] alone
            # split points_for into more key-value pairs
            pts_for = d['points_for']
            d['points_for'] = pts_for.split(' ')[0]
            d['points_for_pg'] = pts_for.split(' ')[1] # parse more for just the for ppg
            d['points_for_rank'] = pts_for.split(' ')[2]
            # split points_against into more key-value pairs
            pts_agnst = d['points_against']
            d['points_against'] = pts_agnst.split(' ')[0]
            d['points_against_pg'] = pts_agnst.split(' ')[1] # parse more for just the for ppg
            d['points_against_rank'] = pts_agnst.split(' ')[2]
            # split expected_w-l into more key-value pairs
            ewl = d.pop('expected_w-l')
            d['expected_w'] = ewl.split('-')[0]
            d['expected_l'] = ewl.split('-')[1]
            return d

        # Get general team info 
        info_dict = {}
        div = team_soup.find("div", attrs={"data-template":"Partials/Teams/Summary"})
        for p in div.find_all("p"):
            rec = p.find("strong")
            # we don't care about anything past this field unless we want
            # coords/coaches/org information
            if rec.text.strip() == "SRS":
                break
            # make all the keys lowercase and replace spaces with underscores
            # in order to assign them as class attributes
            title = rec.text.replace(":","").strip().lower().replace(" ","_")
            info = p.text.replace(rec.text,"").strip()

            info_dict[title] = info

        info_dict = disgusting_parsing(info_dict)

        return info_dict

    def parse_team_injury_info(self, team_soup, short_name):
        # Get the team's latest weekly injury report
        injured_players = []
        div = team_soup.find("div", attrs={"id":f"div_{short_name}_injury_report"})
        tbody = div.find("tbody")
        trs = tbody.find_all("tr")
        for tr in trs:
            # if it doesn't have the "injured_reserve hidden" class then it's a valid row
            if not tr.has_attr('class'):
                player = {}
                th_td_rows = tr.find_all(["th","td"], attrs={"data-stat":True})
                for row in th_td_rows:
                    player[row['data-stat']] = row.text
                injured_players.append(player)
        return injured_players

    def parse_team_stats_rankings(self, team_soup):
        team_stats = {}
        div = team_soup.find("div", attrs={"id":"div_team_stats"})
        tbody = div.find("tbody")
        trs = tbody.find_all("tr")
        for tr in trs:
            th_tr_rows = tr.find_all(["th","td"], attrs={"data-stat":True})
            key = ''
            for row in th_tr_rows:
                if row.name == "th":
                    key = row.text
                    team_stats[row.text] = {}
                else:
                    team_stats[key][row['data-stat']] = row.text
        return team_stats

    # literally the same exact function as parse_team_stats_rankings above
    # just starting with a different div
    def parse_team_conversions(self, team_soup):
        team_stats = {}
        div = team_soup.find("div", attrs={"id":"div_team_conversions"})
        tbody = div.find("tbody")
        trs = tbody.find_all("tr")
        for tr in trs:
            th_tr_rows = tr.find_all(["th","td"], attrs={"data-stat":True})
            key = ''
            for row in th_tr_rows:
                if row.name == "th":
                    key = row.text
                    team_stats[row.text] = {}
                else:
                    team_stats[key][row['data-stat']] = row.text
        return team_stats

    # use the same format as the 2 above functions to get individual
    # players that contribute to the team's passing stats
    def parse_team_stats(self, team_soup, div):
        stats = {}
        d = team_soup.find("div", attrs={"id":div})
        tbody = d.find("tfoot")
        trs = tbody.find_all("tr")
        for tr in trs:
            th_tr_rows = tr.find_all(["th","td"], attrs={"data-stat":True})
            key = ''
            for i, row in enumerate(th_tr_rows):
                if i == 0: # skip the first col, it's blank
                    continue
                elif i == 1: # 2nd col is the key
                    key = row.text
                    stats[row.text] = {}
                else:
                    stats[key][row['data-stat']] = row.text
        return stats

    # lteams = list of short_names
    def scrape_teams(self, lteams):
        DIVS = {'rushing_recving':'div_rushing_and_receiving', 'passing':'div_passing', 'returns':'div_returns',\
            'kicks_punts':'div_kicking', 'defense':'div_defense', 'scoring':'div_scoring'}

        if lteams == ['all']:
            target_teams = self.teams_tri
        # TODO: must be a better way to do this
        # should we just always work with short_names
        else:
            target_teams = []
            for lt in lteams:
                for stt in self.teams_tri:
                    if stt[GET_FULL_NAME] == lt:
                        target_teams.append(stt)

        base_url = "https://www.pro-football-reference.com"
        teams = {}
        for team, url, short in target_teams:
            print(f"[-] Going to {base_url+url}")
            self.driver.get(base_url+url)
            short_name = url.split('/')[2]

            soup = BeautifulSoup(self.driver.page_source, features="lxml")
            print(f"[-] Scraping the entire team's page for team info")
            all_team_info = {}
            all_team_info['short_name'] = short
            all_team_info['url'] = url
            all_team_info['name'] = team
            all_team_info['team_info'] = self.parse_team_info(soup)
            all_team_info['injured_players'] = self.parse_team_injury_info(soup, short_name)

            for k,v in DIVS.items():
                all_team_info[k] = self.parse_team_stats(soup, v)

            t = TeamData(all_team_info)
            teams[team] = t
            print(f"[-] Data for {team} was collected and stored")
        return teams

    def scrape_schedule(self):
        url = "https://www.pro-football-reference.com/years/2021/games.htm"
        file = os.path.join(self.cached_dir, "schedule_cache")
        soup = self.get_soup(file, url)

        # Get table and body with games data in it
        table = soup.find("table", attrs={"id":"games"})
        tbody = table.find("tbody")

        schedule = []
        # for every row in the body of the table
        found = False
        for row in tbody.find_all("tr"):
            row_data = {}
            # for every column in the row
            for col in row.find_all("th", {"class":"right", "data-stat":"week_num"}):
                row_data[col['data-stat']] = col.text
            for col in row.find_all("td"):
                row_data[col['data-stat']] = col.text
                # combine date and time to get the game's dt
                if 'game_date' in row_data and 'gametime' in row_data:
                    gt = f"{row_data['game_date']} {row_data['gametime']}"
                    gt_dt = util.get_dt(gt)
                    row_data["gt_dt"] = gt_dt
                # see if there is an aref
                try:
                    a = col.find_all("a")
                    assert(len(a) == 1)
                    link = a[0]['href']
                    row_data[col['data-stat']+'_link'] = link
                except Exception as e:
                    continue
            if row_data:
                # if game not played, save the time
                if not row_data['pts_win'] and not found:
                    self.next_week_num = row_data['week_num']
                    self.next_gametime = row_data['game_date']
                    found = True
                if self.always_update:
                    # get a list of teams and their respective url while you're at
                    if row_data['winner'] not in self.teams and row_data['winner_link']:
                        self.teams.append(row_data['winner'])
                        short_name = row_data['winner_link'].split("/")[2]
                        self.teams_tri.append((row_data['winner'],row_data['winner_link'],short_name))
                    if row_data['loser'] not in self.teams and row_data['loser_link']:
                        self.teams.append(row_data['loser'])
                        short_name = row_data['loser_link'].split("/")[2]
                        self.teams_tri.append((row_data['loser'],row_data['loser_link'],short_name))
                gd = GameData(row_data)
                schedule.append(gd)

        return Schedule(schedule)

    # return the BeautifulSoup depending on if page source was cached or needs to be fetched
    def get_soup(self, file, url):
        # check if the file was cached, if not go get the page
        if util.page_cached(file) and not self.always_update:
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
