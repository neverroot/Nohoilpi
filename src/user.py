from nohoilpi import *

gambler = Nohoilpi(always_update=True)
gambler.initialize()

teams = ['Tampa Bay Buccaneers', 'Dallas Cowboys', 'Philadelphia Eagles']

gambler.get_schedule()

gambler.get_teams(teams)

this_weeks_games = gambler.get_games_of_week(CURRENT_WEEK)
gambler.print_games(this_weeks_games)

game = this_weeks_games[1]
gambler.analyze_game(game)