from players import Player


def is_num(user_input):
    """
    Checks if user_input is int

    :param user_input: str
    :return: Boolean
    """
    try:
        int(user_input)
    except ValueError:
        return False
    else:
        return True


class PlayerHuman(Player):

    def play(self, total_dice, round_moves):
        """
        Implements the human players turn by prompting user input

        :param total_dice: how many dice are left in the game
        :param round_moves: list of the previous bids of the round
        :return:
        """
        if round_moves[-1][1] != 0:
            prev_bid = round_moves[-1][1]
            print "Previous bid:", prev_bid
        else:
            print "You start the new round!"
        print "Your dice: ", self.dice
        player_bid = raw_input("Give the bid bud! ")
        while not is_num(player_bid):
            player_bid = raw_input("The bid must be integer. Give the bid bud!")
        player_bid = int(player_bid)
        return player_bid
