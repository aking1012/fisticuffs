from .game import Game

#This will come out eventually - it's just a default config to run the game with a simple import
#Accelerates testing, on the interactive console.
num_players = 2
app = Game(num_players)
app.init(num_players)
app.run()
