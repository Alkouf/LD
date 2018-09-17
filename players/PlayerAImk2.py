from players import Player
import math
import numpy as np
from probabilities import calcProbabilityGE


class PlayerAImk2(Player):
    """
    An improved and versatile version of AI player

    The agent (AI player) has a memory option where it holds the previous bids by the opponents.
    The memory is used as indication of what dice might the opponents have.
    E.g. if human plays 2 of star(*) then the AI will think that the human has at least one star
    and will incorporate it to the decision making process.

    The agent has three options for decision making (for selecting the next bid):
    1. Random: from the available bids selects randomly
    2. Greedy: selects the bid that minimizes the probability to lose.
        Isn't very effective against humans because gives out a lot of information.
    3. Softmax: from the probabilities to not lose for every possible bid option,
        calculates a vector of softmax weights. Using the weights selects one of the possible bids.
        That way the AI acts more randomly, and confusing for the human.
        At the same time does not disregard the probabilities but uses them as adapted weights.
    4. Combination of the above: given a number e (\in (0,1)) selects between two of the above options.

    Default option combines greedy with softmax (60% of the time greedy, 40% softmax)
    """
    def __init__(self, nof_dice, player_id, memory=True):
        Player.__init__(self, nof_dice=nof_dice, player_id=player_id)
        self.m = memory

    def play(self, total_dice, round_moves):
        """
        The AI selects one of the possible moves (bids).

        For the decision incorporates the memory option.

        :param total_dice: int, the total number of dice in the game
        :param round_moves: list of tuples, the moves that have been played during the round
        :return: int, the bid
        """

        temp_total = total_dice
        temp_dice = self.dice

        if self.m:
            m = self.memory(round_moves)
            # temp_total = total_dice - len(m)
            temp_dice = self.dice + m

        p = []

        number_bid = round_moves[-1][1] / 10
        symbol_bid = round_moves[-1][1] % 10

        # Calculate the probability the chance to be true
        pn_dice = len([x for x in temp_dice if x == 0 or x == symbol_bid])

        prob = calcProbabilityGE(target_dice=number_bid - pn_dice, out_of_dice=temp_total - len(temp_dice),
                                 symbol=symbol_bid)
        prob = 1 - prob
        # print "probability to win if challenges: ", prob

        p.append((-1, prob))

        for i in range(6):
            temp_bid = self.nextSlot(bid=round_moves[-1], symbol=i)
            temp_number = temp_bid / 10
            # print "i:", i, " temp_number", temp_number
            # print "temp_bid", temp_bid
            temp_number -= len([x for x in temp_dice if x == 0 or x == i])

            new_prob = calcProbabilityGE(temp_number, temp_total - len(temp_dice), i)
            # print "new prob ", new_prob

            p.append((temp_bid, new_prob))

        # return self.choice_greedy(p)
        # return self.choice_softmax(p)
        # return self.choice_greedy(p, e=.05)
        return self.choice_combo(choice1=self.choice_greedy, choice2=self.choice_softmax, p=p, e=.6)

    def choice_random(self, p):
        return self.random.choice(p)[0]

    def choice_softmax(self, p):
        softy = self.softmax(p)
        return softy[self.sample([s[1] for s in softy])][0]

    def choice_greedy(self, p):
        return p[np.argmax([a[1] for a in p])][0]

    def choice_combo(self, choice1, choice2, p, e=.5):
        """
        Combines two of the above selection policies

        :param choice1: first choice function. One of {choice_softmax, choice_greedy, choice_random}
        :param choice2: second choice function. One of {choice_softmax, choice_greedy, choice_random}
        :param p:
        :param e: chance to use the first choice function. Otherwise the second.
        :return:
        """
        assert choice1 == self.choice_greedy or choice1 == self.choice_random or choice1 == self.choice_softmax, \
            "choice1 must be a choice function"
        assert choice2 == self.choice_greedy or choice2 == self.choice_random or choice2 == self.choice_softmax, \
            "choice2 must be a choice function"

        if self.random.random() < e:
            return choice1(p)
        return choice2(p)

    def softmax(self, p):
        """
        Produces the softmax weights from the probabilities p

        :param p: list of float, the probabilities for the bids
        :return: list of float, the softmax weights for the bids
        """
        emphasis = 5
        z_exp = [math.exp(i * emphasis) for i in [a[1] for a in p]]
        # print z_exp
        sum_z_exp = sum(z_exp)

        softmax = [round(i / sum_z_exp, 4) for i in z_exp]

        softmax = zip([a[0] for a in p], softmax)
        return softmax

    def memory(self, round_moves):
        """
        Exports the memory list, that is the probable dice of the opponents.

        :param round_moves:
        :return: list of int, assumes the AI knows one dice of each player
        """
        m = dict()
        for b in round_moves:
            if b[1] != 0:
                symb = b[1] % 10
                if b[0] in m.keys():
                    m[b[0]].append(symb)
                else:
                    m[b[0]] = [symb]

        a = []
        for k in m.keys():
            if k != self.id:
                a.append(m[k][-1])
        return a

    def sample(self, seq):
        """
        Randomly select from sequence according to weights of the sequence.

        :param seq:
        :return:
        """
        v = self.random.random()
        i = 0
        sum = 0
        for a in seq:
            sum += a
            if sum >= v:
                return i
            i += 1
        return 6
