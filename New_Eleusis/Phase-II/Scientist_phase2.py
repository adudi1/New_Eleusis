'''
Team Name : Neurons
Anusha Dudi
Kaushik Velusamy
Mounica Kalavakuri
Ethan Hein
'''

import new_eleusis
from random import *


DECLARERULE_CONFIDENCE = 10.0/20

class Score:
    LEGALCARD = 1 # +1 for every successful play over 20 and under 200;
    ILLEGALCARD = 2 # +2  for every failed play;
    WRONGRULE = 15 # +15 for a rule that is not equivalent to the correct rule;
    BOARDWRONGRULE = 30 # +30 for a rule that does not describe all cards on the board.
    CORRECT_RULE_POINT = -75 # Each player that guesses the correct rule (or its logical equivalent), with no extra terms, receives an  additional  bonus of -75 points.
    ENDEDPLAYER_CORRECT_RULE_POINT = -25 #If the player that ended the game gives the correct rule, it receives an additional -25 points.


class Scientist:
    prevCards = []
    cardsToPlay = []
    cardsPlayed = 0
    currentScore = 0
    currentRule = ""
    currentRuleConfidence = 0.0
    totalCardsForRule = {}
    possibleRules = []
    playingLegalCard = True
    current_domain = 1
    god_rule = ""
    game_ended = False
    no_rules = False

    def __init__(self):
        self.possibleRules = self.forward_checking(build_domain(True))
        self.pickRule()

    def update_board(self, card, legal_value):
        if legal_value:
            c = (card, [])
            self.prevCards.append(c)
        else:
            self.prevCards[len(self.prevCards) - 1][1].append(card)

    def hand(self, cards):
        # print "The card's in the scientist's hand: ", cards
        self.cardsToPlay = cards

    def declareRule(self):
        print "\n"
        if self.currentRuleConfidence >= DECLARERULE_CONFIDENCE:
            self.currentScore += Score.CORRECT_RULE_POINT
            print "-75 points for guessing the correct/logical equivalent rule. Score {}".format(self.currentScore)
            self.currentScore += Score.ENDEDPLAYER_CORRECT_RULE_POINT
            print "-25 points because our scientist ended the game giving the correct rule. Score: {}".format(self.currentScore)
        elif self.rule() == self.currentRule:
            self.currentScore += Score.CORRECT_RULE_POINT
            print "-75 points for guessing the correct/logical equivalent rule. Score {}".format(self.currentScore)
        elif self.currentRuleConfidence == 0:
            self.currentScore += Score.BOARDWRONGRULE
            print "+30 point for hypothesis that does not describe all cards on the board."
        else:
            self.currentScore += Score.WRONGRULE
            print "+15 points for guessing the wrong rule"

        print "********************************************************************************"
        print "Hypothesis: {} score : {} confidence:{}".format(self.currentRule, self.score(),
                                                                self.currentRuleConfidence)
        print "\nGod's Rule Was: {}. \n--Manually check here for logical equivalency.".format(self.rule())
        print "********************************************************************************"
        return self.currentRule

    def play_card(self, card):
        if card == None:
            return self.declareRule()
        if card in self.cardsToPlay:
            self.cardsToPlay.remove(card)
            self.cardsToPlay.append(self.draw_card())
        print "Play number: {}  playedcard: {} score: {}".format(self.cardsPlayed+1, card, self.score())
        if len(self.prevCards) == 0:
            self.game_ended = True
            return self.declareRule()

        self.cardsPlayed += 1

        legalValue = self.play(card)
        self.update_board(card, legalValue)
        self.update_score(legalValue)
        self.update_confidence(legalValue)

        if self.game_ended:
            return self.declareRule()

        return card

    def update_confidence(self, legal_value):
        if self.playingLegalCard:
            if legal_value:
                self.updatecurrentRuleConfidence(1.0 / 20)
            else:
                self.updatecurrentRuleConfidence(0)
        else:
            if not legal_value:
                self.updatecurrentRuleConfidence(1.0 / 20)
            else:
                self.updatecurrentRuleConfidence(0)

    def update_score(self, legal_value):
        if legal_value:
            self.increment_score(Score.LEGALCARD)
            # print "-- Incrementing Score by +1 for every successful play"
        else:
            self.increment_score(Score.ILLEGALCARD)
            # print "-- Incrementing Score by +2 for every failed play"


    def increment_score(self, value):
        if self.cardsPlayed >= 20:
            self.currentScore += value

    def nextcard(self):
        # return card
        if len(self.cardsToPlay) == 0:
            return None
        card = self.pickCardToTest(self.currentRule)
        return card

    def setNewDomain(self):
        if self.current_domain == 1:
            self.current_domain += 1
            self.possibleRules = self.forward_checking(build_domain(True, True))
        elif self.current_domain == 2:
            self.current_domain += 1
            self.possibleRules = self.forward_checking(build_domain(True, True, True))
        else:
            self.no_rules = True
            self.game_ended = True

    def boardState(self):
        return self.state

    def setCurrentRule(self, rule):
        self.currentRule = rule
        self.currentRuleConfidence = 0.0

    def updatecurrentRuleConfidence(self, value):
        if value > 0:
            self.currentRuleConfidence += value
            if self.currentRuleConfidence >= DECLARERULE_CONFIDENCE:  # confidence level to declare rule
                self.game_ended = True
        else:
            self.currentRuleConfidence = 0
            self.pickRule()

    def pickRule(self):
        if len(self.possibleRules) > 0:
            self.setCurrentRule(self.possibleRules.pop(0))
        else:
            self.setNewDomain()


    def pickCardToTest(self, rule):
        try:
            p = new_eleusis.parse(rule)  # if not parse pick different rule to do
        except:
            self.evaluateFail(rule)
            return self.random_card()
        n = len(self.prevCards)

        r = self.random_card()

        if n == 0:
            print "not enough cards"
        elif n == 1:
            cards = ("", self.prevCards[n - 1][0], r)
        else:
            cards = (self.prevCards[n - 2][0], self.prevCards[n - 1][0], r)
        try:
            b = p.evaluate(cards)
            self.playingLegalCard = b
            return r
        except:
            self.evaluateFail(rule)
            return self.random_card()

    def checkCurrentRule(self):
        rule_list = self.forward_checking([self.currentRule])
        while len(rule_list) == 0 and not self.no_rules:
            self.pickRule()
            # print "here-cr: ", self.currentRule
            rule_list = self.forward_checking([self.currentRule])

    def evaluateFail(self, rule):
        if rule in self.possibleRules:
            self.possibleRules.remove(rule)
        self.pickRule()

    def forward_checking(self, domain):
        # check the domain with variables(c1,c2,..)
        # to play next card we take a rule from satisfing domain
        # if next card is illegal, that means our constraint (next card is legal) is failed,
        # so remove(prune) it from domain and repeat with another rule

        prevCards = self.prevCards
        satisfyingDomain = []
        n = len(prevCards)
        if n < 3:
            return domain
        for rule in domain:
            p = new_eleusis.parse(rule)
            legalValue = False
            s = prevCards
            for i in range(0, len(prevCards) - 2, 1):
                cards = (prevCards[i][0], prevCards[i + 1][0], prevCards[i + 2][0])
                try:
                    legalValue = p.evaluate(cards)
                except:
                    pass
                if not legalValue:
                    break
            if legalValue:
                legalValue2 = False
                cards2 = []
                for i in range(-1, len(prevCards) - 2, 1):

                    k = len(prevCards[i + 2][1])
                    if k > 0:
                        for j in range(0, k, 1):
                            cards2 = (prevCards[i + 1][0], prevCards[i + 2][0], prevCards[i + 2][1][j])
                            try:
                                legalValue2 = p.evaluate(cards2)
                                # print legalValue2, cards2
                                legalValue = not (legalValue2)
                            except:
                                pass
                            if legalValue2:
                                break
                    if legalValue2:
                        break
            # print rule, cards, legalValue
            if legalValue:
                satisfyingDomain.append(rule)
        return satisfyingDomain


    def scientist(self, cards, hand, game_ended):
        # print cards, hand, game_ended, self.rule()
        if self.game_ended:
            exit(0)
        for card in cards:
            self.update_board(card, self.play(card))
        self.possibleRules = self.forward_checking(self.possibleRules)
        self.checkCurrentRule();

        if hand is not None:
            self.hand(hand)

        if game_ended or self.game_ended:
            print "The Current board state :", self.prevCards
            return self.declareRule()
        return self.play_card(self.nextcard())


    def setRule(self, rule):
        self.god_rule = rule


    def rule(self):  # returns god's rule or hypothesis?
        return self.god_rule


    def boardState(self):
        return self.prevCards


    def play(self,card):  # checks if a card is legal or not
        if self.rule() == "":
            return True
        parsedGodRule = new_eleusis.parse(self.rule())
        n = len(self.boardState())
        if n < 3:
            return True
        else:
            tuple3 = (self.prevCards[n - 2][0], self.prevCards[n - 1][0], card)
        try:
            legalValue = parsedGodRule.evaluate(tuple3)
        except:
            print "god rule can't evaluate"
            exit()
        return legalValue


    def score(self):
        return self.currentScore


    def random_card(self):
        r = choice(self.cardsToPlay)
        return r

    def draw_card(self):
        values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        suits = ["S", "H", "D", "C"]
        return values[randint(0, len(values) - 1)] + suits[randint(0, len(suits) - 1)]

def build_domain(current=True, prev=False, prev2=False):
    if prev2:
        return domain_3card_rules()
    elif prev:
        return domain_2card_rules()
    else:
        return domain_1card_rules()


def domain_1card_rules():
    func = ['and', 'or']
    operators = ['equal', 'notf']  # ,'less','greater']
    attributes = ['color', 'suit', 'value', 'is_royal', 'even']
    cards = ['current']
    values = [['R', 'B'], ['C', 'H', 'D', 'S'], ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'],
              ['True', 'False'], ['True', 'False']]
    list = []
    for i in operators:
        n = 0;
        if i == 'equal' or i == 'notf':
            for j in attributes:
                n += 1;
                for k in cards:
                    for v in values[n - 1]:
                        # funct = [f]
                        if (i == 'notf') and ((j == 'suit') or j == 'value') or i == 'equal':
                            oper = [i]
                            attr = [j]
                            card = [k]
                            value = [v]
                            list.append(construct_rule(1, None, oper, attr, card, value))
    func = ['and']
    cards = ['current', 'current']

    for h in func:
        m = 0
        n = 0
        for i in operators:
            for i2 in operators:
                k = 0
                l = 0
                for j in attributes:
                    m += 1
                    k = k + 1
                    for j2 in attributes:
                        n += 1
                        l = l + 1
                        for v in values[m - 1]:
                            for v2 in values[n - 1]:
                                if (j != j2):
                                    if (k < l):
                                        if (((i == 'notf' or i2 == 'notf') and (
                                            (j == 'suit' or j == 'value') and (j2 == 'suit' or j2 == 'value')))) or (
                                                i != 'notf' and i2 != 'notf'):
                                            fun = h
                                            oper = [i, i2]
                                            attr = [j, j2]
                                            card = [cards[0], cards[1]]
                                            value = [v, v2]
                                            list.append(construct_rule(2, fun, oper, attr, card, value))
                    n = 0
                    l = 0
                m = 0

    func = ['or']
    cards = ['current', 'current']
    m = 0
    n = 0
    for h in func:
        for i in operators:
            for i2 in operators:
                k = 0
                l = 0
                for j in attributes:
                    m += 1
                    k = k + 1
                    for j2 in attributes:
                        n += 1
                        l = l + 1
                        for v in values[m - 1]:
                            for v2 in values[n - 1]:
                                if (v != v2):
                                    if (k < l):
                                        if (((i == 'notf' or i2 == 'notf') and (
                                            (j == 'suit' or j == 'value') and (j2 == 'suit' or j2 == 'value')))) or (
                                                i != 'notf' and i2 != 'notf'):
                                            fun = h
                                            oper = [i, i2]
                                            attr = [j, j2]
                                            card = [cards[0], cards[1]]
                                            value = [v, v2]
                                            list.append(construct_rule(2, fun, oper, attr, card, value))
                    n = 0
                    l = 0
                m = 0

    return list


def domain_2card_rules():
    func = ['and', 'or']
    operators = ['equal', 'notf']
    attributes = ['color', 'suit', 'value', 'is_royal', 'even']
    cards = ['current', 'previous']
    values = [['R', 'B'], ['C', 'H', 'D', 'S'], ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'],
              ['True', 'False'], ['True', 'False']]
    list = []
    m = 0
    n = 0
    card = [cards[1], cards[0]]
    # for h in func:
    for i in operators:
        for i2 in operators:
            for j in attributes:
                m += 1
                for j2 in attributes:
                    n += 1
                    for v in values[m - 1]:
                        for v2 in values[n - 1]:
                            fun = 'or'  # can't actually have just 'and'
                            oper = [i, i2]
                            attr = [j, j2]
                            value = [v, v2]
                            list.append(construct_rule(2, fun, oper, attr, card, value))
                n = 0
            m = 0
    func = ['and', 'or']
    operators = ['greater', 'less']
    attributes = ['value']
    cards = ['current', 'previous']
    values = [['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']]
    m = 0
    n = 0
    # for h in func:
    for i in operators:
        for i2 in operators:
            for j in attributes:
                m += 1
                for j2 in attributes:
                    n += 1
                    for v in values[m - 1]:
                        for v2 in values[n - 1]:
                            fun = 'or'
                            oper = [i, i2]
                            attr = [j, j2]
                            value = [v, v2]
                            list.append(construct_rule(2, fun, oper, attr, card, value))
                n = 0
            m = 0
    return list


def domain_3card_rules():
    func = ['and', 'or']
    operators = ['equal', 'notf']
    attributes = ['color', 'suit', 'value', 'is_royal', 'even']
    cards = ['current', 'previous', 'previous2']
    values = [['R', 'B'], ['C', 'H', 'D', 'S'], ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'],
              ['True', 'False'], ['True', 'False']]
    list = []
    card = [cards[2], cards[1], cards[0]]
    m = 0
    n = 0
    p = 0

    for i in operators:
        for i2 in operators:
            for i3 in operators:
                for j in attributes:
                    m += 1
                    for j2 in attributes:
                        n += 1
                        for j3 in attributes:
                            p += 1
                            for v in values[m - 1]:
                                for v2 in values[n - 1]:
                                    for v3 in values[p - 1]:
                                        fun = 'or'
                                        oper = [i, i2, i3]
                                        attr = [j, j2, j3]
                                        value = [v, v2, v3]
                                        list.append(construct_rule(3, fun, oper, attr, card, value))
                        p = 0
                    n = 0
                m = 0
    func = ['and', 'or']
    operators = ['greater', 'less']
    attributes = ['value']
    cards = ['current', 'previous', 'previous2']
    values = [['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']]
    m = 0
    n = 0
    p = 0

    for i in operators:
        for i2 in operators:
            for i3 in operators:
                for j in attributes:
                    m += 1
                    for j2 in attributes:
                        n += 1
                        for j3 in attributes:
                            p += 1
                            for v in values[m - 1]:
                                for v2 in values[n - 1]:
                                    for v3 in values[p - 1]:
                                        fun = 'or'
                                        oper = [i, i2, i3]
                                        attr = [j, j2, j3]
                                        value = [v, v2, v3]
                                        list.append(construct_rule(3, fun, oper, attr, card, value))
                        p = 0
                    n = 0
                m = 0
    return list


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
