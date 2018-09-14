from players import Player


# TODO: make PlayerAI class, and PlayerAIsimple should be subclass (is instance tho? think yes)
# TODO: add the option for the player to do something random
class PlayerAIsimple(Player):
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
        prob = self.calcProbabilityGE(target_dice=number_bid - pn_dice, out_of_dice=total_dice - self.nDice,
                                      symbol=symbol_bid)
        prob = 1 - prob
        # print "probability to win if challenges: ", prob

        for i in range(6):
            temp_bid = self.nextSlot(bid=round_moves[-1], symbol=i)
            temp_number = temp_bid / 10
            # print "i:", i, " temp_number", temp_number
            # print "temp_bid", temp_bid
            temp_number -= len([x for x in self.dice if x == 0 or x == i])

            new_prob = self.calcProbabilityGE(temp_number, total_dice - self.nDice, i)
            # print "new prob ", new_prob
            if new_prob > prob:
                prob = new_prob
                new_bid = temp_bid

        #        print self.__str__(), " dice:", self.dice, " bids ", new_bid, " with calculated chance to not lose: ", prob
        return new_bid

    def calcProbabilityGE(self, target_dice, out_of_dice, symbol):
        prob = 0
        if target_dice <= 0:
            return 1
        for i in range(target_dice, out_of_dice + 1):
            prob += self.calcProbabilityE(i, out_of_dice, symbol)

        return prob

    def calcProbabilityE(self, target_dice, out_of_dice, symbol):
        """
        Return the probability that exactly "targetDice" exist
        within the total number of dice ("outofDice").
        Parameter "symbol", refers to the desired number (or if is sta!)

        :param target_dice:
        :param out_of_dice:
        :param symbol:
        :return:
        """
        # TODO: it's not the best way to do the calculations (factorial does not scale well)
        if target_dice < 0:
            return 0

        if symbol == 0:
            return float(self.shitOperation(out_of_dice, target_dice) * pow(1, target_dice) * pow(5, (
                    out_of_dice - target_dice))) / pow(6, out_of_dice)

        return float(
            self.shitOperation(out_of_dice, target_dice) * pow(2, target_dice) * pow(4, (
                        out_of_dice - target_dice))) / pow(6, out_of_dice)

    def shitOperation(self, N, x):
        """
        :param N:
        :param x:
        :return:
        """
        a = max([x, N - x])
        b = min([x, N - x])

        factorial = 1

        for i in range(a + 1, N + 1):
            factorial *= i

        for i in range(1 + 1, b + 1):
            factorial /= i

        return factorial
