class Player:
    import random

    def __init__(self, nof_dice, player_id):
        self.nDice = nof_dice
        self.id = player_id
        self.dice = []

    def shuffleDice(self, n_dice=None, rand=random):
        d = []
        if n_dice is not None:
            self.nDice = n_dice

        for i in range(0, self.nDice):
            d.append(rand.randrange(6))
        self.dice = d
        return d

    def play(self, total_dice, round_moves):
        print "Default play method, should be overriden by subclasses"

    def subtractDice(self, n):
        self.nDice -= n
        if self.nDice < 0:
            self.nDice = 0
        return self.nDice

    def __str__(self):
        return "Player " + str(self.id)+ " has " + str(self.nDice)+ " dice left."

    def setDice(self, nof_dice):
        self.nDice = nof_dice

    def nextSlot(self, bid, symbol):
        # TODO: improve the inheritance

        import math
        # TODO: na to valw to math san dependencies

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
