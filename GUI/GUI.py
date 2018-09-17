from Tkinter import *

import CanvasBoard
import PlayerGUI
from players import PlayerHuman, PlayerAIsimple, PlayerAImk2
from Game import Game
from GUImenu import GMenu
import random


class App:
    """ Handles the GUI and initiates the game procedure """

    def __init__(self):
        self.nof_players = 3
        self.player_type = "mixed"
        self.root = Tk()
        self.root.title("Liar's Dice Board Game")
        self.root.iconbitmap("..\media\\transparenticon.ico")

        self.g_menu = GMenu(root=self.root, start_game_command=self.start_game,
                            player_type_command=self.set_player_type)

        self.frame = Frame()
        self.frame.pack()

        self.frameLeft = Frame(self.frame)
        self.frameLeft.pack(side=LEFT)
        self.cb = CanvasBoard.CanvasBoard(self.frame, width=700, pack_side=LEFT)
        self.frameRight = Frame(self.frame)
        self.frameRight.pack(side=RIGHT)

        self.p = dict()
        self.game = None

        self.root.mainloop()

    def set_player_type(self, t):
        self.player_type = t

    def start_game(self, number_players=None, player_type=None):
        """
        0. destroy the players (if anyone exists)
        1. create the list with the players objects (PlayerHuman, PlayerAI ...)
        2. create the dictionary with the players and lay them onto the left/right frames
        4. starts game (via Game class)

        :param number_players:
        :param player_type: the type of the opponent players; "simpleAI", "AImk2", "mixed" (50% chance each)
        :return:
        """
        # print number_players
        if number_players is not None:
            self.nof_players = number_players

        self.destroy_pui()

        players = list()
        players.append(PlayerHuman(5, 1))
        # players.append(PlayerAIsimple(5, 1))
        if player_type is not None:
            self.player_type = player_type
        if self.player_type == "simpleAI":
            e = 1
        elif self.player_type == "AImk2":
            e = 0
        elif self.player_type == "mixed":
            e = .5
        for i in range(2, self.nof_players + 1, 1):
            # print "AI", i, "chance AI simple:", e
            if random.random() < e:
                players.append(PlayerAIsimple(5, i))
            else:
                players.append(PlayerAImk2(5, i))

        for i in range(self.nof_players):
            # arrange the players' GUI in the correct location
            if i == 0 or i > self.nof_players / 2:
                if i == self.nof_players - 2 and self.nof_players > 4:
                    # make sure the players are laid out clockwise
                    self.p[players[i + 1].id] = PlayerGUI.PlayerGUI(self.frameLeft, width=300, pack_side=TOP,
                                                                    player=players[i + 1])
                    self.p[players[i].id] = PlayerGUI.PlayerGUI(self.frameLeft, width=300, pack_side=TOP,
                                                                player=players[i])
                    break

                self.p[players[i].id] = PlayerGUI.PlayerGUI(self.frameLeft, width=300, pack_side=TOP, player=players[i])
            else:
                self.p[players[i].id] = PlayerGUI.PlayerGUI(self.frameRight, width=300, pack_side=TOP,
                                                            player=players[i])

        game = Game(board=self.cb, pui=self.p)
        game.add_players(players, all_visible=False)
        game.play_game()
        self.game = game

    def destroy_pui(self):
        """
        Destroys the players GUIs that might exist onto the frames, in order to put the new ones.
        Essentially is used when the number of players is changed.
        :return:
        """
        for i in self.p.keys():
            self.p[i].destroy()


if __name__ == "__main__":
    App()
