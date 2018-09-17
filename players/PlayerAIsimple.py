from players import Player
from probabilities import calcProbabilityGE


class PlayerAIsimple(Player):
    """
    A simple AI agent that selects the bid based on a greedy tactic.
    Selects the bid that is the least possible to lose.
    """
    def __init__(self, nof_dice, player_id):
        Player.__init__(self, nof_dice=nof_dice, player_id=player_id)
        # super(Player.Player, self).__init__() ??
        self.newVar = "dummy"

    def play(self, total_dice, round_moves):

        new_bid = -1  # default is to challenge

        number_bid = round_moves[-1][1] / 10
        symbol_bid = round_moves[-1][1] % 10

        # 1. Calculate the probability the chance to be true
        pn_dice = len([x for x in self.dice if x == 0 or x == symbol_bid])
        # print "pn_dice", pn_dice
        prob = calcProbabilityGE(target_dice=number_bid - pn_dice, out_of_dice=total_dice - self.nDice,
                                      symbol=symbol_bid)
        prob = 1 - prob
        # print "probability to win if challenges: ", prob

        for i in range(6):
            temp_bid = self.nextSlot(bid=round_moves[-1], symbol=i)
            temp_number = temp_bid / 10
            # print "i:", i, " temp_number", temp_number
            # print "temp_bid", temp_bid
            temp_number -= len([x for x in self.dice if x == 0 or x == i])

            new_prob = calcProbabilityGE(temp_number, total_dice - self.nDice, i)
            # print "new prob ", new_prob
            if new_prob > prob:
                prob = new_prob
                new_bid = temp_bid

        # print self.__str__(), " dice:", self.dice, " bids ", new_bid, " with calculated chance to not lose: ", prob
        return new_bid
