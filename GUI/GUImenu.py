from Tkinter import *
import tkMessageBox


class GMenu:
    """ The menu on the game window """
    def __init__(self, root, start_game_command, player_type_command):
        self.default_enemies = 3
        self.start_command = start_game_command
        self.player_type_command = player_type_command
        self.player_type = "mixed"

        self.type_select = StringVar()
        self.type_select.set("mixed")

        self.select = IntVar()
        self.select.set(self.default_enemies)

        menubar = Menu(root)
        menubar.add_command(label="New game!", command=self.start_command)

        menubar.add_command(label="Quit!", command=root.quit)

        players_menu = Menu(menubar, tearoff=0)

        players_menu.add_radiobutton(label="1 Opponent", variable=self.select, value=2,
                                     command=self.gen_command(nof_players=2))
        players_menu.add_radiobutton(label="2 Opponents", variable=self.select, value=3,
                                     command=self.gen_command(nof_players=3))
        players_menu.add_radiobutton(label="3 Opponents", variable=self.select, value=4,
                                     command=self.gen_command(nof_players=4))
        players_menu.add_radiobutton(label="4 Opponents", variable=self.select, value=5,
                                     command=self.gen_command(nof_players=5))
        players_menu.add_radiobutton(label="5 Opponents", variable=self.select, value=6,
                                     command=self.gen_command(nof_players=6))

        menubar.add_cascade(label="Select opponents", menu=players_menu)

        player_type_menu = Menu(menubar, tearoff=0)

        player_type_menu.add_radiobutton(label="Type 1", variable=self.type_select, value="simpleAI",
                                         command=self.gen_command_type(player_type="simpleAI"))
        player_type_menu.add_radiobutton(label="Type 2", variable=self.type_select, value="AImk2",
                                         command=self.gen_command_type(player_type="AImk2"))
        player_type_menu.add_radiobutton(label="Mixed", variable=self.type_select, value="mixed",
                                         command=self.gen_command_type(player_type="mixed"))

        menubar.add_cascade(label="Opponent type", menu=player_type_menu)

        menubar.add_command(label="Help", command=self._callback)

        # display the menu
        root.config(menu=menubar)

        print self.select.get(), self.type_select.get()

    def gen_command(self, nof_players):
        return lambda: {
            self.start_command(nof_players)
        }

    def gen_command_type(self, player_type):
        print("type of opponents:", player_type)
        return lambda: {
            self.player_type_command(t=player_type)
        }

    def _callback(self):
        print "click!"
        tkMessageBox.showinfo(
            title="Guidelines to play the game",
            message="You can select the number of the opponents and their type (type 2 is harder) via the menu.\n\n"
                    "When is your turn select your bid using the spinner boxes by defining the symbol and the number. "
                    "The symbol is the dice number (1-5 or star *). "
                    "The minus one (-1) option on \"symbol\" corresponds "
                    "to the act of challenging the previous player.\n\n"
                    "For more information about the game rules refer to "
                    "https://en.wikipedia.org/wiki/Liar%27s_dice#Common_hand"
        )
