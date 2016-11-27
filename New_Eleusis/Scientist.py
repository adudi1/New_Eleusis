import new_eleusis
from random import *


class Score:
    LEGALCARD = 1
    ILLEGALCARD = 2
    WRONGRULE = 15
    BOARDWRONGRULE = 30


class State:
    cardsPlayed = 0
    currentScore = 0
    currentRule = ""
    currentRuleConfidence = 0.0
    totalCardsForRule = {}
    possibleRules = []
    playingLegalCard = True

    def __init__(self, prevCards, godrule):  # prevCards = cards on table so far
        self.prevCards = prevCards
        self.setRule(godrule)
        self.domain = build_domain(True)
        print self.domain
        self.possibleRules = self.forward_checking()
        self.currentRule = self.pickRule()

    def setRule(self, rule):
        self.rule = rule  # gods rule



    def rule(self):
        return self.rule

    def boardState(self):
        return self.state

    def play(self, card):
        print "playedcard: {}".format(card)
        self.cardsPlayed += 1
        n = len(self.prevCards)
        print "god:rule: {}".format(self.rule)
        self.parsedGodRule = new_eleusis.parse(self.rule)
        if n == 0:
            tuple3 = ("", self.random_card(), card)
        elif 0 < n <= 1:
            tuple3 = ("", self.prevCards[n - 1][0], card)
        else:
            tuple3 = (self.prevCards[n - 2][0], self.prevCards[n - 1][0], card)

        legalValue = self.parsedGodRule.evaluate(tuple3)
        print "legalValue {} expected:{}".format(legalValue, self.playingLegalCard)
        self.updateBoardState(card, legalValue)
        print prevcards

    def setCurrentRule(self, rule):
        print "setcurrentrule {}".format(rule)
        self.currentRule = rule
        self.currentRuleConfidence = 0.0

    def scientist(self):
        pass

    def score(self):
        return self.currentScore

    def updateBoardState(self, card, legalValue):
        if self.playingLegalCard:
            if legalValue:
                c = (card, [])
                self.prevCards.append(c)
                self.updateScore(Score.LEGALCARD)
                self.updatecurrentRuleConfidence(Score.LEGALCARD)
                self.play(self.nextcard(False))
            else:
                self.prevCards[len(self.prevCards) - 1][1].append(card)
                self.updateScore(Score.ILLEGALCARD)
                self.updatecurrentRuleConfidence(Score.ILLEGALCARD)
        else: # when playing a card that should be illegal accori=ding to our current rule
            if legalValue:
                c = (card, [])
                self.prevCards.append(c)
                self.updateScore(Score.LEGALCARD)
                self.updatecurrentRuleConfidence(0)
            else:
                self.prevCards[len(self.prevCards) - 1][1].append(card)
                self.updateScore(Score.ILLEGALCARD)
                self.play(self.nextcard(True))




    def updateScore(self, value):
        if self.cardsPlayed > 20:
            self.currentScore += value

    def updateCardsPlayed(self, value=1):
        self.cardsPlayed += value
        if self.cardsPlayed >= 200:
            self.declareRule()

    def updatecurrentRuleConfidence(self, value):
        if value == Score.LEGALCARD:
            fraction = float(1.0 / self.totalCards(self.currentRule))
            self.currentRuleConfidence += fraction
            if self.currentRuleConfidence >= 0.5: #confidence level to declare rule
                self.declareRule()
        else:
            self.currentRuleConfidence = 0
            self.pickRule()
        print "Rule: {} Confidence: {}".format(self.currentRule, self.currentRuleConfidence)

    def pickRule(self):
        print "pickrule"
        if len(self.possibleRules) >0:
            self.setCurrentRule(self.possibleRules.pop())
            return self.currentRule

    def declareRule(self):
        print "Output Rule: {}".format(self.currentRule)
        exit()
        # return self.currentRule

    def nextcard(self, playingLegalCard):
        # return card
        card = self.pickCardToTest(self.currentRule, playingLegalCard)
        return card


    def pickCardToTest(self, rule, playingLegalCard):
        self.playingLegalCard = playingLegalCard
        if playingLegalCard:
            values = satisfying_values(rule)
            suit = satisfying_suits(rule)
            self.totalCardsForRule[rule] = len(values) * len(suit)
        else:
            values = non_satisfying_values(rule)
            suit = non_satisfying_suits(rule)

        return self.random_card(values, suit)

    def totalCards(self, rule):
        if rule not in self.totalCardsForRule.keys():
            values = satisfying_values(rule)
            suit = satisfying_suits(rule)
            self.totalCardsForRule[rule] = len(values) * len(suit)
        return self.totalCardsForRule[rule]

    def forward_checking(self):
        # check the domain with variables(c1,c2,..)
        # to play next card we take a rule from satisfing domain
        # if next card is illegal, that means our constraint (next card is legal) is failed,
        # so remove(prune) it from domain and repeat with another rule

        while len(self.prevCards) < 3:
            self.play(self.random_card())

        print "Cards onTable: {}".format(self.prevCards)

        satisfyingDomain = []
        n = len(prevcards)
        for rule in self.domain:
            p = new_eleusis.parse(rule)
            legalValue = False
            for card in self.prevCards:
                cards = (self.prevCards[n - 3][0], self.prevCards[n - 2][0], card[0])
                legalValue = p.evaluate(cards)
                if not legalValue:
                    break
            if legalValue:
                satisfyingDomain.append(rule)
        return satisfyingDomain

    def random_card(self, value=None, suit=None):
        # random_card()
        # select a random odd red card
        # random_card([1,3,5,7,9,11,13],['D','H'])
        i = randint(1, 13)
        s = choice('CDHS')
        if value is not None:
            i = choice(value)
        else:
            value = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        if suit is not None:
            s = choice(suit)
        else:
            suit = ['C','H','D','S']

        v = new_eleusis.number_to_value(i)
        card = v + s
        print "self.prevCards: {}".format(self.prevCards)
        s = self.prevCards
        while card in str(s).strip('[]') and len(self.prevCards) < len(value)*len(suit):
            #print "card in prevcards: True {} {}".format(card, self.prevCards)
            card = self.random_card(value, suit)

        return card

def satisfying_values(rule=None):
    # improve
    if rule is not None:
        if 'odd' in rule:
            return [1, 3, 5, 7, 9, 11, 13]
        if 'even' in rule:
            return [2, 4, 6, 8, 10, 12]
        if 'royal' in rule:
            return [1, 11, 12, 13]
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


def satisfying_suits(rule=None):
    # improve
    if rule is not None:
        if 'R' in rule:
            return ['H', 'D']
        if 'B' in rule:
            return ['S', 'C']
        if 'C' in rule:
            return ['C']
        if 'D' in rule:
            return ['D']
        if 'H' in rule:
            return ['H']
        if 'S' in rule:
            return ['S']
    return ['C', 'D', 'H', 'S']




def non_satisfying_values(rule):
    l = []
    l = list(set(satisfying_values()) - set(satisfying_values(rule)))
    if len(l) > 0:
        return l
    return None


def non_satisfying_suits(rule):
    l = []
    l = list(set(satisfying_suits()) - set(satisfying_suits(rule)))
    if len(l) > 0:
        return l
    return None




def cardProperties(card):
    # to do : add more properties
    return {'suit': new_eleusis.suit(card), 'value': new_eleusis.value(card), 'color': new_eleusis.color(card)}




def variables():
    # contraints between cards
    pass


def constraints():
    # next card should evaluate to true
    pass


# def domain():
#     return build_domain()

def build_domain(current=True, prev=False, prev2=False):
    if prev2:
        return domain_3card_rules()
    elif prev:
        return domain_2card_rules()
    else:
        return domain_1card_rules()


def domain_1card_rules():
    func = ['and', 'or']
    operators = ['equal']
    attributes = ['color', 'suit']
    cards = ['current']
    values = [['R', 'B'], ['C', 'H', 'D', 'S']]
    list = []
    n = 0
    for i in operators:
        for j in attributes:
            n += 1
            for k in cards:
                for v in values[n - 1]:
                    # for v in l:
                    oper = [i]
                    attr = [j]
                    card = [k]
                    value = [v]
                    list.append(construct_rule(1, None, oper, attr, card, value))

    return list


def domain_2card_rules():
    # for 2 card rules
    pass


def domain_3card_rules():
    # for 3 card rules
    pass


def construct_rule(args, func, operators, attributes, cards, values):
    # args - int - number of arguments in the rule for function
    # func - string - and/or/if/
    # operators - list (length = args), - equal/not/less/greater
    # attributes - list - color/value/suit
    # cards -list - prev2/prev/curr
    # values -list

    list = []
    rule = ''
    for i in range(0, args, 1):
        oper = operators[i]
        attr = attributes[i]
        card = cards[i]
        value = values[i]
        prule = oper + '(' + attr + '(' + card + '), ' + value + ')'
        list.append(prule)
    if len(list) > 1:
        s = ', '.join(list)
        rule = func + '(' + s + ')'
    else:
        rule = list[0]

    return rule


# print construct_rule(2, 'and', ['equal','equal'],['color','color'],['previous','current'],['R','R'])
# and(equal(color(previous),R),equal(color(current),R))
# print "------------------"
# domain_1card_rules()

prevcards = [('3S', [])]
boardState = State(prevcards, "equal(color(current), B)")
# boardState.setRule()  # god rule
while boardState.cardsPlayed <=200:
    boardState.play(boardState.nextcard(prevcards))
# boardState.play("3H")
print boardState.score()

# tasks:
# 0. rule and cards - initial check to -kaushik
# 1.construct_rule() - kaushik
# 2. domain_1card_rules() - Mounica
# 3. domain_2card_rules() - Ethan
# 4. domain_3card_rules() - Ethan
# 5. nextcard() # small change - Anusha
# 6. Forward_checking #small change - Anusha
# 7. Score() - Anusha
# 8. confidence for rule - Anusha
# 9. satisfying_values(rule) - Mounica
# 10. satisfying_suits(rule) - Mounica
# 11. check against already played cards - next card -kaushik
