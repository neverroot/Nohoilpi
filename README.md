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

Example Usage in Interpreter
```
In [1]: from nohoilpi import *                                                                                                                                                                             

In [2]: n = Nohoilpi(always_update=True)                                                                                                                                                                   

In [3]: n.initialize()                                                                                                                                                                                     
[WDM] - 

[WDM] - ====== WebDriver manager ======
[WDM] - Current google-chrome version is 95.0.4638
[WDM] - Get LATEST driver version for 95.0.4638
[WDM] - Driver [/home/neveroot/.wdm/drivers/chromedriver/linux64/95.0.4638.54/chromedriver] found in cache

In [4]: n.get_schedule()                                                                                                                                                                                   
[-] File not cached. Fetching
[-] Cached to cached_pages/schedule_cache

In [5]: teams = ['Tampa Bay Buccaneers', 'Dallas Cowboys', 'Philadelphia Eagles']                                                                                                                          

In [6]: teamdatas = n.get_teams(teams)                                                                                                                                                                     
[-] Going to https://www.pro-football-reference.com/teams/tam/2021.htm
[-] Scraping the entire team's page for team info
[-] Data for Tampa Bay Buccaneers was collected and stored
[-] Going to https://www.pro-football-reference.com/teams/dal/2021.htm
[-] Scraping the entire team's page for team info
[-] Data for Dallas Cowboys was collected and stored
[-] Going to https://www.pro-football-reference.com/teams/phi/2021.htm
[-] Scraping the entire team's page for team info
[-] Data for Philadelphia Eagles was collected and stored

In [7]: teamdatas                                                                                                                                                                                          
Out[7]: 
{'Tampa Bay Buccaneers': Tampa Bay Buccaneers,
 'Dallas Cowboys': Dallas Cowboys,
 'Philadelphia Eagles': Philadelphia Eagles}

In [8]: n.week_1                                                                                                                                                                                           
Out[8]: 
[Tampa Bay Buccaneers @ Dallas Cowboys,
 Philadelphia Eagles @ Atlanta Falcons,
 Carolina Panthers @ New York Jets,
 Arizona Cardinals @ Tennessee Titans,
 San Francisco 49ers @ Detroit Lions,
 Houston Texans @ Jacksonville Jaguars,
 Pittsburgh Steelers @ Buffalo Bills,
 Los Angeles Chargers @ Washington Football Team,
 Cincinnati Bengals @ Minnesota Vikings,
 Seattle Seahawks @ Indianapolis Colts,
 Kansas City Chiefs @ Cleveland Browns,
 New Orleans Saints @ Green Bay Packers,
 Miami Dolphins @ New England Patriots,
 Denver Broncos @ New York Giants,
 Los Angeles Rams @ Chicago Bears,
 Las Vegas Raiders @ Baltimore Ravens]


In [9]: current_week = n.get_games_of_week(CURRENT_WEEK)                                                                                                                                                  
[-] Today's date: 2021-11-07 11:48AM

In [10]: current_week                                                                                                                                                                                      
Out[10]: 
[Indianapolis Colts @ New York Jets,
 Atlanta Falcons @ New Orleans Saints,
 New England Patriots @ Carolina Panthers,
 Cleveland Browns @ Cincinnati Bengals,
 Houston Texans @ Miami Dolphins,
 Minnesota Vikings @ Baltimore Ravens,
 Buffalo Bills @ Jacksonville Jaguars,
 Las Vegas Raiders @ New York Giants,
 Denver Broncos @ Dallas Cowboys,
 Los Angeles Chargers @ Philadelphia Eagles,
 Arizona Cardinals @ San Francisco 49ers,
 Green Bay Packers @ Kansas City Chiefs,
 Tennessee Titans @ Los Angeles Rams,
 Chicago Bears @ Pittsburgh Steelers]
```