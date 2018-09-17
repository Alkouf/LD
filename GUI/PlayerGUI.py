from Tkinter import *
import tkFont

from players import Player, PlayerHuman


class PlayerGUI:
    def __init__(self, root, width=100, player_gui_font=None, pack_side=None, player=None, human_player=False):
        self._canvas_color = "green3"
        self._human_color = "deep sky blue"
        self._ai_color = "lightgreen"

        self.root = root

        self._font = player_gui_font
        self._human_player = human_player

        self.dice = [1, 2, 3]
        self.name = "Name placeholder"
        self.dice_visible = True
        self.active = True
        self.message = "No message"

        self._spinny_number = None
        self._spinny_symbol = None
        self._bid_button = None

        self._side = width

        self.player_frame = Frame(root, bg=self._canvas_color, height=self._side, bd=5, width=self._side, relief=GROOVE,
                                  padx=0,
                                  pady=0)
        self.player_frame.pack(side=pack_side)

        self.name_canvas = Canvas(self.player_frame, bg=self._ai_color, borderwidth=0, width=self._side * .9,
                                  height=self._side / 5)

        self.dice_canvas = Canvas(self.player_frame, bg=self._canvas_color, borderwidth=0, width=self._side * .9,
                                  height=self._side * 0.15 * 2)

        self.message_canvas = Canvas(self.player_frame, bg=self._canvas_color, borderwidth=0, width=self._side * .9,
                                     height=self._side / 5)

        self.name_text = self.name_canvas.create_text(self._side * .9 / 2, self._side / 5 / 2,
                                                      text="This is a name per se. ", anchor="center",
                                                      width=int(self._side * .9 * .9), font=self._font)
        # if not human_player:
        self.message_label = Label(self.message_canvas, text="",
                                   width=30, height=10, wraplength=200, bg=self._canvas_color)
        self.message_label.pack()
        self.message_canvas.create_window(self._side * .9 / 2, self._side / 5 / 2, window=self.message_label)
        if human_player:  # Isn't used; setup method is used instead
            self.create_bid()
            self.name_canvas.config(bg=self._human_color)

        self.canvas_die = []
        for i in range(5):
            self.canvas_die.append([Canvas(self.dice_canvas, bg='lightblue', borderwidth=3, width=0.15 * self._side,
                                           height=self._side * .15, relief=RAISED)])

            # the '6' is because of the border on canvas_die ^
            self.canvas_die[i].append(
                self.canvas_die[i][0].create_text((6 + 0.15 * self._side) / 2, (6 + 0.15 * self._side) / 2, text="X",
                                                  anchor="center", font=self._font))
            self.dice_canvas.create_window((i * (.15 + .025) + 0.1) * self._side, self._side * 0.15, anchor="center",
                                           window=self.canvas_die[i][0])

        self.set_dice()

        self.setup(player=player)

        self.name_canvas.pack()
        self.dice_canvas.pack()
        self.message_canvas.pack()

    def create_bid(self):
        """
        Creates the necessary GUI widgets for the bid

        :return: None
        """

        self.message_label.destroy()

        self.message_label = Label(self.message_canvas, text="",
                                   width=30, height=2, wraplength=200, bg=self._canvas_color)
        self.message_label.pack()
        self.message_canvas.create_window(self._side * .9 / 2, self._side / 10 / 2., window=self.message_label)

        self.message_canvas.create_text(self._side / 10, self._side / 3.7 / 2., text="Symbol:")

        self._spinny_symbol = Spinbox(master=self.message_canvas, values=(-1, 1, 2, 3, 4, 5, "*"), width=2)
        self.message_canvas.create_window(self._side * 2.5 / 10, self._side / 3.7 / 2., window=self._spinny_symbol)

        self.message_canvas.create_text(self._side * 4.3 / 10, self._side / 3.7 / 2., text="Number:")

        self._spinny_number = Spinbox(master=self.message_canvas, values=range(1, 31, 1), width=2)
        self.message_canvas.create_window(self._side * 6 / 10, self._side / 3.7 / 2., window=self._spinny_number)

        self._bid_button = Button(master=self.message_canvas, text="Bid")
        self.message_canvas.create_window(self._side * 8 / 10, self._side / 3.7 / 2., window=self._bid_button)

    def set_bid_button_state(self, state=NORMAL):
        """
        Sets the state of the bid button (NORMAL = can be pressed, DISABLED = cannot)

        :param state: (str)"NORMAL", "DISABLED"
                   or (TkInter constant) NORMAL, DISABLED
        :return: None
        """

        assert state is "NORMAL" or "DISABLED" or NORMAL or DISABLED

        if isinstance(state, str):
            if state == "NORMAL":
                state = NORMAL
            elif state == "DISABLED":
                state = DISABLED
        # print "state:", state
        self._bid_button.config(state=state)

    def set_bid_button_command(self, command):
        """set the action to be done when bid button is pressed"""

        self._bid_button.config(command=command)

    def get_spinbox_bid(self):
        """translates the user input (via spinboxes) to bid"""

        number = int(self._spinny_number.get())
        symbol = 0 if self._spinny_symbol.get() == "*" else int(self._spinny_symbol.get())
        return number * 10 + symbol if symbol != -1 else -1

    def set_message(self, mess):
        """ if mess is str then update the player's message label  (otherwise do nothing)"""

        if isinstance(mess, str):
            self.message = mess
            self.message_label.config(text=mess)

    def set_name(self, name=None):
        """ if name is str then update the player's name label  (otherwise do nothing)"""

        if isinstance(name, str):
            if name is not None:
                self.name = name
            self.name_canvas.itemconfig(self.name_text, text=name)

    def set_active(self, active):
        """ if player is active (=True) then the bg color is set """

        self.active = active
        if active:
            self.player_frame.config(bg="#333")

    def set_dice(self, dice=None, visible=False):
        """
        Updates the GUI for the dice

        Human player's dice are always visible
        AI's dice only after the end of the round

        :param dice: list with ints representing the dice (1,2,3,4,5,6 (6=star))
        :param visible: make the dice visible onto the GUI
        :return:
        """
        if dice is not None:
            self.dice = dice
        for i in range(5 - len(self.dice)):
            self.canvas_die[4 - i][0].config(relief=SUNKEN)
            self.canvas_die[4 - i][0].config(bg='pink')
            self.canvas_die[4 - i][0].itemconfig(self.canvas_die[4 - i][1], text="X")
        for i in range(len(self.dice)):
            self.canvas_die[i][0].config(relief=RAISED)
            self.canvas_die[i][0].config(bg='lightblue')
            self.canvas_die[i][0].itemconfig(self.canvas_die[i][1], text=str(
                self.dice[i] if self.dice[i] != 0 else '*') if self.dice_visible or visible else "?")

    def lost_dice(self, nof_remaining):
        """
        Gives pink bg to the dice that are lost.

        :param nof_remaining: The number of dice the player still possesses
        :return: Nothing
        """
        for i in range(5):
            if i + 1 > nof_remaining:
                if self.canvas_die[i][0].cget('relief') != SUNKEN:
                    self.canvas_die[i][0].config(relief=SUNKEN)
                    self.canvas_die[i][0].config(bg='red')

    def setup(self, player):
        if isinstance(player, Player):
            # assert the appropriate values
            if isinstance(player, PlayerHuman):
                self._human_player = True
                self.name_canvas.config(bg=self._human_color)
                self.create_bid()
            self.set_dice(player.dice)
            self.name = " Player " + str(player.id)

            self.set_name(self.name)

    def destroy(self):
        self.player_frame.destroy()


if __name__ == "__main__":
    # for testing

    root = Tk()

    font = tkFont.Font(size=12, weight=tkFont.NORMAL)

    pg = PlayerGUI(root, width=300, player_gui_font=None)   # can add _font

    pg.dice_visible = True

    pg.set_dice([0, 3, 5, 0])

    pg2 = PlayerGUI(root, width=300, player_gui_font=None, human_player=True)

    pg2.dice_visible = True

    pg2.set_dice([0, 3, 5, 0])

    root.update()

    pg.set_message("Bid is 100")

    # pg2.set_number_spinbox_state(state="DISABLED")

    root.mainloop()
