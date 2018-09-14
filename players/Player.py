class Player:
    """ Interface of the players (either human or AI) """
    import random

    def __init__(self, nof_dice, player_id):
        self.nDice = nof_dice
        self.id = player_id
        self.dice = []

    def shuffleDice(self, n_dice=None, rand=random):
        """
        Recreates the action of throwing the dice by the player and updates the self.dice var

        :param n_dice: How many dice the player has
        :param rand:
        :return: the list of integers representing the dice
        """
        d = []
        if n_dice is not None:
            self.nDice = n_dice

        for i in range(0, self.nDice):
            d.append(rand.randrange(6))
        self.dice = d
        return d

    def play(self, total_dice, round_moves):
        """Default play method, should be overriden by subclasses"""
        pass

    def subtractDice(self, n):
        """
        Removes the given number of dice from the player (min value is zero)

        :param n:
        :return: the number of remaining dice
        """
        self.nDice -= n
        if self.nDice < 0:
            self.nDice = 0
        return self.nDice

    def __str__(self):
        return "Player " + str(self.id)+ " has " + str(self.nDice) + " dice left."

    def setDice(self, nof_dice):
        self.nDice = nof_dice

    def nextSlot(self, bid, symbol):
        """
        Finds the next valid bid given the current one and the desired symbol of the new bid

        Given the current bid, what is the most conservative bid given the symbol (1,2,3,4,5,*).
        E.g. if bid = 52 (five ones) and the symbol = 4, the result = 54
            if bid = 52 and symbol = 1, result = 61
            if bid = 20 and symbol = 3, result = 43

        :param bid: current bid
        :param symbol: the symbol of the new bid
        :return: the next valid bid
        """

        import math

        number_bid = bid[1] / 10
        symbol_bid = bid[1] % 10
        if symbol == symbol_bid:
            return (number_bid + 1) * 10 + symbol_bid
        if symbol == 0:
            return int(math.ceil((number_bid + 1) / 2.) * 10)
        # if symbol_bid
        if symbol_bid < symbol:
            if symbol_bid == 0:
                number_bid *= 2
            if number_bid == 0:  # when is the first bid
                number_bid += 1
            return number_bid * 10 + symbol  # just rotate the dice, increase the symbol

        return (number_bid + 1) * 10 + symbol  # increase by one the number
