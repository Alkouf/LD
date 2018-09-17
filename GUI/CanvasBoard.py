from Tkinter import *
import tkFont
import tkMessageBox


class CanvasBoard:
    """" implements the board GUI """
    def __init__(self, root, width, height=None, pack_side=None):
        """
        Setup the board within the root

        Creates the cells on the circumference of the board and the message panel in the interior

        :param root:
        :param width:
        :param height:
        :param pack_side:
        """
        self.bid_die_rect = None
        self.bid_die_text = None

        self.root = root
        self.width = width
        if height is None:
            height = 0.7 * self.width
        self.height = height
        self.canvas = Canvas(self.root, bg='grey', borderwidth=5, width=self.width, height=self.height)
        self.canvas.pack(side=pack_side)

        self.cell_dims = self.width / 10.0

        self.c_font = tkFont.Font(size=str(int(-0.5 * self.cell_dims)), weight=tkFont.NORMAL)

        self.cells = [[] for i in range(30)]

        for i in range(30):
            if i < 10:
                self.cells[i] = (self.canvas.create_rectangle(i * self.cell_dims, 0, (i + 1) * self.cell_dims,
                                                              self.cell_dims, fill="yellow"), i * self.cell_dims, 0)
            elif i < 16:
                self.cells[i] = (self.canvas.create_rectangle(9 * self.cell_dims, (i - 9) * self.cell_dims,
                                                              10 * self.cell_dims, (i + 1 - 9) * self.cell_dims,
                                                              fill="yellow"), 9 * self.cell_dims,
                                 (i - 9) * self.cell_dims)
            elif i < 24:
                self.cells[i] = (self.canvas.create_rectangle((25 - i) * self.cell_dims, 6 * self.cell_dims,
                                                              (24 - i) * self.cell_dims, 7 * self.cell_dims,
                                                              fill="yellow"), (24 - i) * self.cell_dims,
                                 6 * self.cell_dims)
            else:
                self.cells[i] = (self.canvas.create_rectangle(0 * self.cell_dims, (31 - i) * self.cell_dims,
                                                              1 * self.cell_dims, (30 - i) * self.cell_dims,
                                                              fill="yellow"), 0 * self.cell_dims,
                                 (30 - i) * self.cell_dims)

        i = 1
        s = 2
        for c in self.cells:
            if s == 3:
                s = 0
                self.canvas.create_text(c[1] + int(self.cell_dims / 2), c[2] + int(self.cell_dims / 2),
                                        text=str((i + 1) / 2) + "*")
                self.canvas.itemconfig(c[0], fill="red")
            else:
                self.canvas.create_text(c[1] + int(self.cell_dims / 2), c[2] + int(self.cell_dims / 2), text=i)
                i += 1
            s += 1

        for i in range(len(self.cells)):  # not used
            self.canvas.tag_bind(self.cells[i][0], '<Button-1>', self.lambda_gen(cc=i))

        self.innie = InnerBoard(self.canvas)

    def place_bid(self, bid):
        """
        Visualizes the bid onto the board.

        Deletes the rectangle and text from the canvas.
        Places the new ones according to the arguments.
        Greys out the cells that are behind the bid.

        if bid is None or bid == 0: clears the previous placements and restores the board to the original state

        if bid ==-1: changes the color of the placement

        else: removes the previous placement and places the bid onto the board

        :param bid: the newest bid
        :return: None
        """
        color = "lime green"

        if bid is None:
            bid = 0

        if bid == -1:
            self.canvas.itemconfig(self.bid_die_rect, fill="dark goldenrod")
            return

        self.canvas.delete(self.bid_die_rect)
        self.canvas.delete(self.bid_die_text)

        if bid == 0:
            self.grey_out_cells()
            return

        symbol = str(bid % 10)
        if symbol == "0": symbol = "*"
        index = self._bid_to_location(bid)

        c = self.cells[index]

        # create the rectangle
        self.bid_die_rect = self.canvas.create_rectangle(c[1],
                                                         c[2] + 3. / 5. * self.cell_dims,
                                                         c[1] + 2. / 5. * self.cell_dims,
                                                         c[2] + self.cell_dims,
                                                         fill=color)

        # create the text with the corresponding symbol
        self.bid_die_text = self.canvas.create_text(c[1] + 1. / 5. * self.cell_dims,
                                                    c[2] + 4. / 5. * self.cell_dims,
                                                    anchor="center", text=symbol)

        self.grey_out_cells(index=index)

    def _bid_to_location(self, bid):
        """
        Given the bid, finds the index or the position of the bid (aka the cell index).

        :param bid:
        :return:
        """
        symbol = bid % 10
        number = bid / 10
        if symbol == 0:
            index = number * 3 - 1
        else:
            index = number + number / 2
        return index - 1

    def _event_cell(self, event, cell_number):
        """For future use"""
        # print "hey this is an eventful event"
        # print "cell No", cell_number
        # print event.x, event.y
        # print event.x_root, event.y_root
        pass

    def lambda_gen(self, cc):
        return lambda event: {
            self._event_cell(event, cc)
        }

    def grey_out_cells(self, index=None, bid=None):
        """
        Changes the color of the first cells to grey.
        if index is given, then greys out the first "index" cells (no matter the bid).
        if index is None and bid is given, then finds the index that corresponds to bid.
        if both index and bid are None ((index is None) and (bid is None)) then resets the color of the cells.
            The same if index is negative number.

        :param index: indicates how many cells are to be greyed out
        :param bid: is the latest bid, and greys out all the non valid cells
        :return: None
        """
        if index is None:
            if bid is None:
                index = -1
            else:
                index = self._bid_to_location(bid)
        for i in range(30):
            self.canvas.itemconfig(self.cells[i][0], fill="yellow")
        i = 1
        s = 2
        for c in self.cells:
            if s == 3:
                s = 0
                self.canvas.itemconfig(c[0], fill="red")
            else:
                i += 1
            s += 1
        for c in self.cells:
            if c[0] <= index:
                self.canvas.itemconfig(c[0], fill="#555")

    def set_dice_in_game(self, nofdice):
        """
        Updates the message in the interior of the board regarding the dice number

        :param nofdice: int, the number of dice in game
        :return: None
        """
        self.innie.set_dice_in_game(nofdice)
        self.root.update()

    def set_players_active(self, nofactive):
        """
        Updates the relevant message at the itnerior of the board about the number of players still playing

        :param nofactive: int, the number of active players, players that still have dice
        :return: None
        """
        self.innie.set_players_active(nofactive)

    def set_message(self, message):
        """
        Updates the message at the interior of the board with the given message

        :param message: str, the message to write
        :return: None
        """
        self.innie.set_message(message)

    def blink(self, ms=500):
        """
        Updates the queued actions referring to the board and waits some ms.
        (Deprecated?)

        :param ms: int, millliseconds to wait
        :return: None
        """
        self.root.update_idletasks()
        self.root.after(ms)

    def update_gui(self):
        """
        Updates the pending GUI actions

        :return: None
        """
        self.root.update_idletasks()

    def set_inner_button_text(self, text):
        self.innie.set_button_text(text=text)

    def set_inner_button_command(self, command):
        self.innie.set_button_command(command=command)

    def set_inner_button_state(self, state=NORMAL):
        """ state= (str) NORMAL / DISABLED """
        self.innie.set_button_state(state=state)


class InnerBoard:
    """
    Class that implements the interior of the board.
    It contains some messages (player count, dice count, info)
    and the button that initiates the new round.
    """
    def __init__(self, parent_canvas, font=None):
        self.font = tkFont.Font(size=12, weight=tkFont.NORMAL)  # default only value

        self.width = float(parent_canvas.cget('width')) / 2
        self.height = float(parent_canvas.cget('height')) / 2
        self.inner_board = Canvas(parent_canvas, bg=parent_canvas.cget('bg'), borderwidth=5, width=self.width,
                                  height=self.height, relief=RAISED)
        self.inner_board.pack()

        parent_canvas.create_window(float(parent_canvas.cget('width')) / 2, float(parent_canvas.cget('height')) / 2,
                                    window=self.inner_board, anchor="center")

        self.dice_in_game = self.inner_board.create_text(self.width / 2, self.height / 5, width=int(0.9 * self.width),
                                                         anchor="center", text="Dice in game: 10", font=self.font,
                                                         justify="center")
        self.players_active = self.inner_board.create_text(self.width / 2, self.height * 2 / 5,
                                                           width=int(0.9 * self.width), anchor="center",
                                                           text="Players that still play: 0", font=self.font,
                                                           justify="center")
        self.message = self.inner_board.create_text(self.width / 2, self.height * 3 / 5, width=int(0.9 * self.width),
                                                    anchor="center",
                                                    text="Press new game to start",
                                                    font=self.font, justify="center")

        self.button = Button(self.inner_board, text="continue", state=DISABLED)
        self.button.pack()
        self.inner_board.create_window(self.width / 2, self.height * 4 / 5, window=self.button)

    def set_dice_in_game(self, nofdice):
        self.inner_board.itemconfig(self.dice_in_game, text="Dice in game: " + str(nofdice))

    def set_players_active(self, nofactive):
        self.inner_board.itemconfig(self.players_active, text="Players that still play: " + str(nofactive))

    def set_message(self, message):
        self.inner_board.itemconfig(self.message, text=message)

    def set_button_command(self, command):
        self.button.config(command=command)

    def set_button_text(self, text):
        self.button.config(text=text)

    def set_button_state(self, state=NORMAL):
        if isinstance(state, str):
            if state == "NORMAL":
                state = NORMAL
            else:
                state = DISABLED
        self.button.config(state=state)


if __name__ == "__main__":
    # For testing

    root = Tk()
    # w = 1000
    w = 600
    cb = CanvasBoard(root, width=w)

    # cb.grey_out_cells(index=1)
    # cb.set_inner_button_text(text="Neo text gia tot button mou")
    # cb.set_inner_button_command(command=lambda: cb.set_inner_button_text("Molis patises to koumpi"))
    # cb.set_inner_button_state(DISABLED)

    # cb.place_bid(index=10, symbol="2")

    bid = 20
    cb.place_bid(bid=bid)
    cb.place_bid(bid=-1)

    # cb.place_bid(0)

    # print cb._bid_to_location(10)

    # cb.grey_out_cells(1)

    # cb.place_bid(index=29, symbol="100")
    root.mainloop()
