from scraper import Scraper, Schedule
from analyzer import Analzyer
import os
import time

CURRENT_WEEK = 0
class Nohoilpi():
    def __init__(self, always_update=False):
        self.always_update = always_update
        self.teams = {}

    def initialize(self):
        self.analyzer = Analzyer()
        self.scraper = Scraper(self.always_update)
        self.scraper.initialize()
        self.NFL_TEAMS = self.scraper.teams

    def print_games(self,lgames):
        self.schedule.print_list_of_games(lgames)

    # get the games of nth week
    # if n=0 get current week
    def get_games_of_week(self,n):
        assert(self.schedule)
        if n==0:
            return self.schedule.week(self.schedule.get_curr_week_num())
        return self.schedule.week(n)

    # get the week number of the given matchup (a vs b)
    def get_week_of_matchup(self, a, b, n=0):
        for game in self.schedule.games:
            if game.winner == a and game.loser == b or game.winner == b and game.loser == a:
                return int(game.week_num)

    # returns team data for each team in the list provided
    # provide it lteams=['all'] to get every team's data
    def get_teams(self, lteams):
        if lteams == ['all']:
            teamdatas = self.scraper.scrape_teams(["all"])
            self.teams.update(teamdatas)
            return teamdatas
        teamdatas = self.scraper.scrape_teams(lteams)
        self.teams.update(teamdatas)
        return teamdatas

    def get_schedule(self):
        self.schedule = self.scraper.scrape_schedule()
        self.__dict__.update(self.schedule.__dict__)
    
    def analyze_week(self, n):
        games_of_week = self.schedule.week(n)
        all_res = []
        for game in games_of_week:
            res = self.analyze_matchup(game.winner, game.loser)
        return all_res

    def analzye_teams_last_game(self, full_name, n):
        assert(self.schedule)
        games_of_last_week = getattr(self,f"week_{n}")
        for game in games_of_last_week:
            if full_name == game.winner or full_name == game.loser:
                self.analyze_game(game.winner, game.loser)

    # analyze the matchup of a vs b on nth week
    def analyze_game(self, a, b):
        last_a_game = self.analzye_teams_last_game(a,n-1)
        last_b_game = self.analzye_teams_last_game(b,n-1)
        matchup_stats = self.analzyer.matchup(a,b,last_a_game,last_b_game)
