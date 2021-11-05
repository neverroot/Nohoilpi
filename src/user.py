from nohoilpi import Nohoilpi


gambler = Nohoilpi(always_update=True)
gambler.initialize()

teams = ['Tampa Bay Buccaneers', 'Dallas Cowboys', 'Philadelphia Eagles']

gambler.get_schedule()
