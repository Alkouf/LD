from players import Player


class PlayerHuman(Player):

    def play(self, total_dice, round_moves):
        if round_moves[-1][1] != 0:
            prev_bid = round_moves[-1][1]
            print "previous bid:", prev_bid
        else:
            print "you start the new round!"
        print "your dice: ", self.dice
        player_bid = raw_input("Give the bid bud! ")
        # TODO: check that input is valid
        player_bid = int(player_bid)
        return player_bid
