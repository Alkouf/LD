from players import Player
import math
import numpy as np
from probabilities import calcProbabilityGE


class PlayerAImk2(Player):

    def __init__(self, nof_dice, player_id, memory=True):
        Player.__init__(self, nof_dice=nof_dice, player_id=player_id)
        # super(Player.Player, self).__init__() ??
        self.m = memory

    def play(self, total_dice, round_moves):

        print "round moves:", round_moves

        temp_total = total_dice
        temp_dice = self.dice

        if self.m:
            m = self.memory(round_moves)
            print "MEMORY:", m
            print "total original", total_dice
            # temp_total = total_dice - len(m)
            temp_dice = self.dice + m
            print "temp total and dice", temp_total, temp_dice

        p = []

        newBid = -1  # default is to challenge

        number_bid = round_moves[-1][1] / 10
        symbol_bid = round_moves[-1][1] % 10

        # 1. Calculate the probability the chance to be true
        pn_dice = len([x for x in temp_dice if x == 0 or x == symbol_bid])
        # print "pn_dice", pn_dice
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
        emphasis = 5
        z_exp = [math.exp(i * emphasis) for i in [a[1] for a in p]]
        # print z_exp
        sum_z_exp = sum(z_exp)

        softmax = [round(i / sum_z_exp, 4) for i in z_exp]

        softmax = zip([a[0] for a in p], softmax)
        return softmax

    def memory(self, round_moves):
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
        v = self.random.random()
        i = 0
        sum = 0
        for a in seq:
            sum += a
            if sum >= v:
                return i
            i += 1
        return 6
