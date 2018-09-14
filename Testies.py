from players.PlayerAIsimple import PlayerAIsimple
import GameCLI
from players.PlayerAImk2 import PlayerAImk2
import time
from threading import Timer


# def hello():
#     print "Hello world in "
#
# def append_stats():
#     name = "stats.csv"
#     with open(name, "ab") as f:
#         f.write("one,line \n")
#         print "line wrote"
#
# append_stats()
# t = Timer(1.0, hello)
# t.start()
# print "hello outside"

from Tkinter import *

master = Tk()

def callback():
    print "click!"

b = Button(master, text="OK", command=callback)

b.pack()

mainloop()

exit()


starting_time = time.time()

nof_players = 2
# players list: list of doubles, players[i][0] is of type Player, and players[i][1] is of type PlayerGUI
players = list()
# players.append((PlayerHuman(5, 1), None))
# players.append((PlayerAIsimple(5, 1), None))
players.append((PlayerAImk2(5,1),None))
for i in range(2, nof_players+1, 1):
    players.append((PlayerAIsimple(5, i), None))


winners = []
r=10000
for i in range(r):
    for p in players:
        p[0].shuffleDice(n_dice=5)
    game = GameCLI.Game()
    game.add_players([x[0] for x in players])
    winners.append(game.playGame())


print "Duration:", (time.time()-starting_time)
print "Player 1 won:", (winners.count(1)), " out of ", r
# 5040 / 10000 simple vs simple
# 7581 / 10000 mk2 vs simple (greedy(e=0), memory=True)
# 4820 / 10000 mk2 vs simple (softmax, memory=True)
# 550 / 1000 mk2 vs 3 simple (greedy(e=0), memory=True)
# 6873/ 10000 mk2 vs simple (greedy(e=0.05), memory=True)

exit()
# moves = [(1, 100), (2, 200)]
#
# ph.shuffleDice(rand=random)
# ph2.shuffleDice()
# pai.shuffleDice()
#
# game = Game.Game()
# game.addPlayers([ph, ph2, pai])
# # game.playCycle(startingPlayerId=ph.id)
#
# # ph.play(20,moves)
# # print ph.dice
#
#
# pai.shuffleDice()

# print pai.shitOperation(N=4,x=2)
# pr = pai.calcProbabilityGE(targetDice=5,outofDice=10,symbol=2)
# print "probability",pr
