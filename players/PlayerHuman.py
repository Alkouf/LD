from players import Player


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
        player_bid = int(player_bid)
        return player_bid
