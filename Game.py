import Evaluate as eval
from players import PlayerAIsimple, PlayerHuman, Player, PlayerAImk2
import time
import threading
from Tkinter import TclError

# TODO: if GUI not applicable then proceed with the CLI version


class Game:
    def __init__(self, board=None, pui=None, starting_player_id=None, pauses=True):
        """
        Initialize, if either board or pui is None, then the gui is deactivated.
        PlayerHuman must be played with the gui!!

        :param board: CanvasBoard object that corresponds to the board (default None).
                If None then no gui is used at all.
        :param pui: list of PlayerGUI objects that correspond to the players (default None). If None then no gui at all.
        :param starting_player_id: integer (default None), the id of the player that starts the game.
                If None starts the first player on the list.
        :param pauses: boolean (default True), when gui is applicable, if true the gameplay will pause
                when one round finishes,until the "continue" button is pressed.
                If false no pauses until the start of the new round.
                When there is one or more human players (PlayerHuman) the value must be "True".
        """
        self.moves = []  # list of lists of tuples (p_id, bid)
        self.players = []
        self.totalDice = 0
        self.board = board
        self.pui = pui
        self.starting_player_id = starting_player_id
        if self.board is not None:
            self.board.set_inner_button_text("Play next round")
            self.board.set_inner_button_command(self.play_game)

        self.cycle_moves = []
        self.pauses = pauses  # False does not work when there is human player
        self.delay = 1000  # the delay after some actions in milliseconds
        self.recorded_stats = False
        self.wait_thread = None

    def add_players(self, player_list, all_visible=False):
        """
        Given a list of Player objects, adds them to the player list. Use with caution, preferably use it only once.
        The id must be unique for each player.

        :param all_visible: Boolean, denotes if every player's dice are to be visible.
                If not, only the humans' are visible.
        :param player_list: List of objects, of the class Player or subclass
        :return:
        """
        assert set([isinstance(p, Player) for p in player_list]) == {True}, \
            "Not all players are instances of Player"

        # check that the ids are unique
        ids = []
        for p in self.players + player_list:
            if p.id in ids:
                print "Duplicate ID, exiting"
                exit()
            else:
                ids.append(p.id)

        self.players += player_list
        self.update_total_dice()
        for p in self.players:
            self.pui[p.id].setup(p)
            if isinstance(p, PlayerHuman):
                self.pui[p.id].set_bid_button_command(command=self.continue_cycle)
                self.pui[p.id].set_bid_button_state(state="DISABLED")

                self.pauses = True  # is set to true because there is a human player
                print "\'pauses\' is set to True, as there is a human player"

            elif not all_visible:
                self.pui[p.id].dice_visible = False

    def remove_players(self, player_ids=None):
        """
        Remove players, given a list with player IDs.

        :param player_ids: list with the ids of the players that continue to play
        :return:
        """

        remaining_player = []
        for i in range(0, len(self.players)):
            if self.players[i].id not in player_ids:
                remaining_player += self.players[i]

        self.players = remaining_player
        if player_ids is None:
            self.players = []
        self.update_total_dice()

    def play_game(self, starting_player_id=None):
        """
        If self.pauses: plays one game round (until somebody challenges), and then waits
        for the button (inner canvas) to call this method again for a new game round
        (meaning the human player initiates the new round)

        If not self.pauses: plays game rounds, until only one player is left; the winner
            Note: if self.pauses==False: does not work with human player(s)

        :param starting_player_id: The id of the player that starts the round.
                Is set only on the first game round, it is managed internally for the following rounds.
        :return:
        """
        self.board.set_inner_button_state("DISABLED")

        self.board.place_bid(0)

        assert len(self.players) >= 2, "Not enough players!"

        # find the player the starts the round
        if starting_player_id is None:  # if no new value given
            if self.starting_player_id is None:  # if no default value already exists
                for p in self.players:
                    if p.nDice > 0:  # find the first player that has dice > 0, and set him/her as starting
                        self.starting_player_id = p.id
                        break
        else:
            self.starting_player_id = starting_player_id

        if not self.pauses:
            self.init_cycle()
            self.play_cycle()
            # print "Starting player:", self.starting_player_id
            while len([x for x in self.players if x.nDice > 0]) > 1:
                self.init_cycle()
                self.play_cycle()
        else:
            if len([x for x in self.players if x.nDice > 0]) > 1:
                self.init_cycle()
                self.play_cycle()

        if len([x for x in self.players if x.nDice > 0]) == 1:
            # One player left, game is over!
            self.board.set_message("Player " + str(self.starting_player_id) + " has won!")
            for p in self.players:
                if p.id == self.starting_player_id and isinstance(p, PlayerHuman):
                    # if a human player exists then export the stats
                    self.export_stats()

        self.board.blink(0)

    def continue_cycle(self):
        """
        This method is called only when a human plays, and presses the "bid" button.
        In essence it continues the normal steps that had been interrupted when the human player's turn come up.
        In detail:
            checks if bid is valid; if not return
            else if it is valid: find the player that starts after the human player,
                and call self.play_cycle to continue the cycle

        :return: None
        """
        # take the bid from the form
        print self.starting_player_id

        new_bid = self.pui[self.starting_player_id].get_spinbox_bid()

        # check if valid -> if not-> return (in order to be given a new and valid bid) + message
        print self.cycle_moves[-1], (self.starting_player_id, new_bid)
        if eval.Evaluate.validBid(self.cycle_moves[-1], (self.starting_player_id, new_bid)):
            bid = (self.starting_player_id, new_bid)
            # append human players' bid
            self.cycle_moves.append(bid)
            self.pui[self.starting_player_id].set_message("Player Bid:" + str(new_bid))
            self.board.place_bid(bid=new_bid)
            self.pui[self.starting_player_id].set_bid_button_state(state="DISABLED")
        else:
            self.board.set_message("Invalid bid, please enter a valid bid!")
            return
            # if isinstance(active_players[self.starting_player_id % nof_active], PlayerAIsimple.PlayerAIsimple):
            #     print "Player is AI, no point in playing again, will provide the same bid probably"
            #     exit()

        # increment the playing id (thelei ligi skepsi)

        index = 0
        for i in range(len(self.players)):
            if self.players[i].id == self.starting_player_id:
                index = i
        index += 1
        self.starting_player_id = self.players[index % len(self.players)].id
        while self.players[index].nDice <= 0:
            self.starting_player_id = self.players[(index + 1) % len(self.players)].id
            index += 1

        self.play_cycle()

    def init_cycle(self):
        """
        Initializes the cycle: shuffle + UI display.

        :return: None
        """
        self.board.place_bid(bid=-1)
        self.board.set_message("New round! Player " + str(self.starting_player_id) + " starts!")

        bid = (0, 0)
        self.cycle_moves = [bid]  # ! the place holder starting new round
        for p in self.players:
            self.pui[p.id].set_message("")
            if p.nDice > 0:
                p.shuffleDice()
            else:
                p.dice = []
            self.pui[p.id].set_dice(p.dice)

    def play_cycle(self):
        """
        Plays (or continues) the round.
        Plays the turns, until a challenge happens or it is the human's turn.
        If human's turn just update the self.starting_player and the self.cycle_moves, and waits for the player to bid.
            when the human bids, it updates starting_player and appends the bid and returns to this method.

        If the last bid was a challenge (this could be the human's bid):
            evaluates the situation, removes dice and returns

        :return: None
        """
        active_players = [x for x in self.players if x.nDice > 0]
        # print active_players

        nof_active = len(active_players)
        playing_index = 0  # the index of the player that plays next, (with regard to the active players list)
        for i in range(nof_active):  # find the starting player
            if active_players[i].id == self.starting_player_id:
                playing_index = i
                break

        total_dice = sum([x.nDice for x in self.players])

        actions = []

        # self.board.set_dice_in_game(total_dice)
        actions.append((self.board.set_dice_in_game, [total_dice], None))
        # self.board.set_players_active(len(active_players))
        actions.append((self.board.set_players_active, [len(active_players)], None))

        while self.cycle_moves[-1][1] != -1:
            """
            Paizei o paiktis pou einai i seira tou.
            To neo bid paei sto telos.
            An to bid einai -1, tote vgainei apo to loop.
            """
            # self.board.set_message("Player " + str(active_players[playing_index % nof_active].id) + " plays")
            actions.append((self.board.set_message,
                            ["Player " + str(active_players[playing_index % nof_active].id) + " plays"], self.delay))
            # self.board.blink(self.delay)

            if isinstance(active_players[playing_index % nof_active], PlayerHuman):
                self.starting_player_id = active_players[playing_index % nof_active].id
                # self.pui[self.starting_player_id].set_bid_button_state(state="NORMAL")
                actions.append((self.pui[self.starting_player_id].set_bid_button_state, ["NORMAL"], None))
                # self.delayed_actions(actions)
                self.wait_thread = threading.Thread(target=self.delayed_actions, args=(actions,))
                # threads.append(t)
                self.wait_thread.start()
                return

            new_bid = active_players[playing_index % nof_active].play(total_dice=total_dice,
                                                                      round_moves=self.cycle_moves)
            active_id = active_players[playing_index % nof_active].id
            print new_bid

            if eval.Evaluate.validBid(self.cycle_moves[-1], (active_id, new_bid)):
                bid = (active_id, new_bid)
                self.cycle_moves.append(bid)
                playing_index += 1
                # self.pui[active_id].set_message("Player Bid:" + str(new_bid))
                actions.append((self.pui[active_id].set_message, ["Player Bid:" + str(new_bid)], None))
                # self.board.place_bid(bid=new_bid)
                actions.append((self.board.place_bid, [new_bid], None))
            else:
                self.board.set_message("Invalid bid, please enter a valid bid!")
                if isinstance(active_players[playing_index % nof_active], PlayerAIsimple):
                    print "Player is AI, no point in playing again, will provide the same bid probably"
                    exit()

        actions.append((self.reveal, [], None))
        actions.append((self.eval_carry_out,
                        [eval.Evaluate.challenge(active_players, self.cycle_moves), active_players, playing_index],
                        None))
        t = threading.Thread(target=self.delayed_actions, args=(actions,))
        t.start()
        self.moves += self.cycle_moves
        self.board.blink(0)

    def delayed_actions(self, actions):
        # do stuff until reveal
        # do stuff until player bid
        # if pauses = false is ok? NO, delay only if pauses == False
        # with and without human ...
        """
        actions[i] = (function, args, delay)
        possible actions: (type_of_action, id, extra_args, delay)
        1. (set_bid_active, id, None, ms)
        2. (set_player_message, id, message, ms)
        3. (set_board_bid, None, bid, ms)
        4. (set_board_message, None, message, ms)
        5. (reveal_all, None, None, ms)
        6. (eval_carry_out, None, None, ms)
        """
        for a in actions:
            print a[0], a[1]
            try:
                a[0](*a[1])
            except TclError:
                print "Hey byatch. Don't sweat it."

            if a[2] is not None:
                self.board.update_gui()
                time.sleep(self.delay / 1000)
        return

    def reveal(self):
        """
        Sets the dice visible in the GUI (instead of ?), and prints the dice.
        For all the players.

        :return: None
        """
        for p in self.players:
            self.pui[p.id].set_dice(visible=True)

    def update_total_dice(self):
        """
        Calculates the cumulative number of dice that all the players have, and update the value of self.totalDice

        :return: self.totalDice, with the updated value
        """
        self.totalDice = sum([x.nDice for x in self.players])
        return self.totalDice

    def eval_carry_out(self, ev, active_players, playing_index):
        """
        Receives the value ev of the evaluation, the list of active players,
        and the playingIndex (the index of the active players' list that corresponds to the player that plays next).

        Removes the correct number of dice from the player(s). Also prints some messages that describe who lost how many

        Returns the id of the player that plays next.

        :param ev:
        :param active_players:
        :param playing_index:
        :return:
        """
        nof_active = len(active_players)

        msg = "Player " + str(active_players[(playing_index - 1) % nof_active].id) + " challenged, "
        if ev < 0:
            msg += "and player " + str(active_players[(playing_index - 2) % nof_active].id) + " loses " + str(
                abs(ev)) + " dice"
            active_players[(playing_index - 2) % nof_active].subtractDice(abs(ev))
            starting_player_id = active_players[(playing_index - 1) % nof_active].id
        elif ev == 0:
            msg += "and all players but " + str(active_players[(playing_index - 2) % nof_active].id) + " lose one die"
            for p in active_players:
                if p != active_players[(playing_index - 2) % nof_active]:
                    p.subtractDice(1)
            starting_player_id = active_players[(playing_index - 2) % nof_active].id
        else:
            msg += "and player" + str(active_players[(playing_index - 1) % nof_active].id) + " loses " + str(
                ev) + " dice"
            active_players[(playing_index - 1) % nof_active].subtractDice(abs(ev))
            starting_player_id = active_players[(playing_index - 2) % nof_active].id

        for p in self.players:
            self.pui[p.id].lost_dice(p.nDice)
            if isinstance(p, PlayerHuman):
                if p.nDice == 0 and not self.recorded_stats:
                    # export the stats right after the player loses, because they are likely to initiate new game
                    self.export_stats()
                    self.recorded_stats = True

            # if p.nDice == 0:
            #     p.dice = []
            #     self.pui[p.id].set_active(False)
            # self.pui[p.id].set_dice(dice=p.dice)

        if self.pauses:
            self.board.set_inner_button_state("NORMAL")
        self.board.set_message(msg)
        self.board.set_players_active(len([x for x in self.players if x.nDice > 0]))
        self.starting_player_id = starting_player_id
        return self.starting_player_id

    def find_player_by_id(self, player_id):
        """
        Finds the player with the given id, and returns the player object.
        If not found, returns None

        :param player_id:
        :return:
        """
        for p in self.players:
            if p.id == player_id:
                return p
        return None

    def export_stats(self):
        t1_w = 0
        t2_w = 0
        t1 = 0
        t2 = 0
        w_L = "win"
        for p in self.players:
            if isinstance(p, PlayerHuman):
                if p.nDice == 0:
                    w_L = "loss"
            elif isinstance(p, PlayerAImk2):
                t2 += 1
                if p.nDice > 0:
                    t2_w += 1
            elif isinstance(p, PlayerAIsimple):
                t1 += 1
                if p.nDice > 0:
                    t1_w += 1
        self.append_stats(nof_opponents=t1 + t2, w_L=w_L, count_t1=t1, count_t2=t2, lost_to_t1=t1_w, lost_to_t2=t2_w)
        # write the stats to the .cvs file

    def append_stats(self, nof_opponents, w_L, count_t1, count_t2, lost_to_t1, lost_to_t2):
        # time, nof_opponents, w_L, count_t1, count_t2, lost_to_t1, lost_to_t2
        f_name = "stats.csv"
        with open(f_name, "a+") as f:
            f.write(
                time.ctime() + "," + str(nof_opponents) + "," + str(w_L) + "," + str(count_t1) + "," + str(
                    count_t2) + "," + str(lost_to_t1) + "," + str(lost_to_t2) + "\n")


if __name__ == '__main__':
    g = Game()
    from players import PlayerAImk2

    print g.add_players(player_list=[Player(nof_dice=5, player_id=1),
                                     PlayerHuman(nof_dice=5, player_id=2),
                                     PlayerAIsimple(nof_dice=5, player_id=3),
                                     PlayerAImk2(nof_dice=5, player_id=4)
                                     ])
