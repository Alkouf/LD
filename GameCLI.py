import Evaluate as eval
from players import PlayerAIsimple, PlayerHuman, Player, PlayerAImk2

"""
Play the game via the terminal.

No stats.  
"""


class Game:
    def __init__(self):
        # self.eval = Evaluate.Evaluate()
        self.moves = []  # tuple (pid, bid)
        self.players = []
        self.totalDice = 0

    def add_players(self, player_list):
        """

        :param player_list: List of objects, of the class Player or subclass
        :return:
        """
        assert set([isinstance(p, Player) for p in player_list]) == {True}, \
            "Not all players are instances of Player"

        self.players += player_list
        self.totalDice = sum([x.nDice for x in self.players])

    def remove_players(self, playerIDs):
        """
        Remove players, given a list with player IDs.

        :param playerIDs:
        :return:
        """

        remainingPlayer = []
        for i in range(0, len(self.players)):
            if self.players[i].id not in playerIDs:
                remainingPlayer += self.players[i]
        self.players = remainingPlayer
        self.totalDice = sum([x.nDice for x in self.players])

    def playGame(self, starting_player_id=None):
        """
        The game sequence

        :return:
        """

        print "* * * * * * * * * * * * * * * * \n* NEW ROUND STARTS! *"
        if len(self.players) < 2:
            print "Not enough players! Exit"
            exit()
        if starting_player_id is None:
            starting_player_id = self.players[0].id

        while len([x for x in self.players if x.nDice > 0]) > 1:
            starting_player_id = self.play_cycle(starting_player_id)

        print "* THE GAME IS OVER! *"
        for p in self.players:
            print p
        print "* Player", starting_player_id, " is the winner! *"
        return starting_player_id

    def play_cycle(self, starting_player_id):
        """

        :param starting_player_id:
        :return: The id of next starting player.
                 None if game over.
        """
        bid = (0, 0)
        cycleMoves = [bid]  # ! the place holder starting new round

        activePLayers = [x for x in self.players if x.nDice > 0]

        for p in activePLayers:
            p.shuffleDice()

        nofActive = len(activePLayers)
        playingIndex = 0  # the index of the player that plays next, (in regards to the active players list)

        for i in range(nofActive):  # find the starting player
            if activePLayers[i].id == starting_player_id:
                playingIndex = i
                break

        totalDice = sum([x.nDice for x in self.players])

        while bid[1] != -1:
            """
            Paizei o paiktis pou einai i seira tou.
            To neo bid paei sto telos.
            An to bid einai -1, tote vgainei apo to loop.
            """

            activeID = activePLayers[playingIndex % nofActive].id
            print "Player ", activeID, " plays"
            newBid = activePLayers[playingIndex % nofActive].play(total_dice=totalDice, round_moves=cycleMoves)
            if eval.Evaluate.validBid(cycleMoves[-1], (activeID, newBid)):
                bid = (activeID, newBid)
                cycleMoves.append(bid)
                playingIndex += 1
                print "Player", activeID, " bade: ", newBid
            else:
                print "Invalid new bid, the player plays again!"
                if not isinstance(activePLayers[playingIndex % nofActive], PlayerHuman):
                    print "Player is AI, no point in playing again, will provide the same bid probably"
                    exit()
            print "- - - - - - - - - - - - - "

        print "* CHALLENGE! *"
        self.reveal()

        ev = eval.Evaluate.challenge(activePLayers, cycleMoves)

        print "Player id=", activePLayers[(playingIndex - 1) % nofActive].id, " challenged!"
        print "And there the difference on the dice is: ", ev
        if ev < 0:
            print "player", activePLayers[(playingIndex - 2) % nofActive].id, "loses", abs(ev), "dice"
            activePLayers[(playingIndex - 2) % nofActive].subtractDice(abs(ev))
            starting_player_id = activePLayers[(playingIndex - 1) % nofActive].id
        elif ev == 0:
            print "all players but player", activePLayers[(playingIndex - 2) % nofActive].id, "lose one die"
            for p in activePLayers:
                if p != activePLayers[(playingIndex - 2) % nofActive]:
                    p.subtractDice(1)
            starting_player_id = activePLayers[(playingIndex - 2) % nofActive].id
        else:
            print "player", activePLayers[(playingIndex - 1) % nofActive].id, "loses", ev, "dice"
            activePLayers[(playingIndex - 1) % nofActive].subtractDice(abs(ev))
            starting_player_id = activePLayers[(playingIndex - 2) % nofActive].id

        print "Situation after removing dice:"

        for p in self.players:
            if p.nDice == 0:
                p.dice = []
            print "Player", p.id, " has ", p.nDice, "dice left"

        print "* The round ended! *"
        print "* * * * * * * * * * * * * * * *"
        self.moves += cycleMoves

        return starting_player_id

    def reveal(self):
        for p in self.players:
            # if p.nDice == 0:
            #     p.dice = []
            print p.id, " player ", p.dice

    def update_total_dice(self):
        self.totalDice = sum([x.nDice for x in self.players])
        return self.totalDice


if __name__ == '__main__':
    g = Game()

    g.add_players(player_list=[PlayerHuman(nof_dice=5, player_id=1),
                               PlayerAImk2(nof_dice=5, player_id=2)
                               ])
    g.playGame()
