from Tkinter import *


class GMenu:
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
