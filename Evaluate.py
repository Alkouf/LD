from collections import Counter


class Evaluate:
    @staticmethod
    def validBid(previousBid, newBid):
        """
        Checks if the new bid is valid, according to the rules.
        I.e. if the new bid is larger than the previous, or challenge.

        :param previousBid:
        :param newBid:
        :return:
        """

        if newBid[1] == -1:
            if previousBid[1] == -1 or previousBid[1] == 0:  # if it is the first bid of the round cannot challenge
                return False
            return True
        prevSymbol = previousBid[1] % 10
        prevNumber = previousBid[1] / 10

        newSymbol = newBid[1] % 10
        newNumber = newBid[1] / 10

        if newSymbol == 0:
            # what about stars. Number -> star. Star->number
            newNumber = newNumber * 2 - .5

        if prevSymbol == 0:
            prevNumber = prevNumber * 2 - .5

        if newNumber > prevNumber:
            # more in number
            return True

        if newNumber == prevNumber and newSymbol > prevSymbol:
            # same number but greater symbol
            return True

        return False

    @staticmethod
    def challenge(players, moves):
        """
        When somebody challenges, what happens, who loses dice.

        :param players:
        :param moves:
        :return: None if not enough entries in move list OR last move is not challenge.
                 Otherwise, the difference between the actual dice and the bid number.
                 Negative integer means that person who bid last has to lose abs(X) dice.
                 Positive: the person who challenged has to lose X dice.
                 Zero: all but the last bidder must lose one dice.
        """
        if len(moves) <= 1:
            print "Not enough moves, :/"
            return None

        if moves[-1][1] != -1:
            print "Not a challenge, :/"
            return None

        lastBid = moves[-2][1]
        lastSymbol = lastBid % 10
        lastNumber = lastBid / 10

        # TODO: this prerequisites that the players that lost have no dice!!
        dice = [x.dice for x in players]
        dice = [item for sublist in dice for item in sublist]
        # ^ hope this works

        countDict = Counter(dice)

        count = countDict[0]  # Stars always count
        if lastSymbol != 0:
            count += countDict[lastSymbol]  # if not star, add the particular symbol count

#        print "EVAL: symbol:",lastSymbol," bidded number:",lastNumber,"actual number:",count

        return count - lastNumber
