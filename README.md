Nohoilpi - Navajo Gambling God

Of all the gods of gambling we have talked about, there is no truer god of chance than Nohoilpi. He was born with the purpose of teaching mankind about gambling games and was worshipped for that.
Known as “the Great Gambler,” Nohoilpi is the son of Tsohanoai, the god of the sun in the nation’s lore. When Nohoilpi first descended on Earth, he showed mankind how to play, and introduced them to all sorts of gambling games.

Yet, he was a bit mischievous himself, and he defeated people, indebting them and asking to repay their debt by building a city to pay tribute to him. According to lore, the other gods soon became jealous of Nohoilpi, so they gifted a tribe member with exceptional acumen and prescience and sent him to face off with Nohoilpi and chase him away.

Guided by other deities, the man succeeded and sent Nohoilpi back to the heavens, but his legacy lives to this day all over North America! Nohoilpi used to carry a turquoise talisman, so if you are ever looking for a lucky charm fit for a god, here is a good idea.

Source: https://www.gamblingnews.com/blog/the-god-of-gambling/ by Luke Thompson


This is currently setup for Linux using Chromedriver.

Example usage:
```
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
```