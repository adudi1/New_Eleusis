import new_eleusis
from random import *


class State:
    def __init__(self, state):
        self.state = state

    def setRule(self, rule):
        self.rule = rule

    def rule(self):
        return self.rule

    def boardState(self):
        return self.state

    def play(self, card):
        # to do
        pass

    def scientist(self):
        pass

    def score(self):
        pass


class HTree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.value = None
        self.attribute = None


def nextcard(prevcards):
    # hyp = traverse_hypothesisSpace(prevcards)
    # card = test_hyp(hyp)
    # return card
    pass


def guessrule():
    # return best hypothesis so far, in rule format
    pass


def random_card(value=None, suit=None):
    i = randint(1, 13)
    s = choice('CDHS')
    if value is not None:
        i = choice(value)
    if suit is not None:
        s = choice(suit)

    v = new_eleusis.number_to_value(i)
    card = v + s
    return card


# print random_card()

# select a random odd red card
# print random_card([1,3,5,7,9,11,13],['D','H'])



def hypothesis():
    # cards = ['3S', 'JH']
    #
    # currentcard_list = {'color(current)': 'R','value(current)': 'odd', 'value(current)': 'is_royal'}
    # operators = ["equal", "not"]
    #
    # root = HTree()
    # for j in operators:
    #     for i in currentcard_list.keys():
    #         p = new_eleusis.parse(i)
    #         root.value = j
    #         root.left = HTree()
    #         root.left.value = i
    #         root.right = HTree()
    #         root.right.value = currentcard_list.value(i)

    # red card should be followed by a black card
    # return "andf(equal(color(previous)R),equal(color(current),B))"
    # return hypothesis to be tested
    pass


    # def card(prev=None, prev2=None):
    # return card to be played to test hypothesis
    # h = hypothesis()
    # if h is based on only current, play a card to fail the hypothesis

    # if h is based on current and prev
    # if prev is none, play a card that fits prev
    # prev  is already there, play a card that fails the hypothesis
    # if h is based on current, prev and prev2
    # if prev and prev2 are none play prev2, prev then fail hypothesis with current
    # if prev is none, play prev then fail hypothesis with current
    # else play  current to fail hypothesis
    # pass
