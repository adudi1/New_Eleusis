'''
Team Name : Neurons
Anusha Dudi
Kaushik Velusamy
Mounica Kalavakuri
Ethan Hein
'''

import new_eleusis
from random import *


class Score:
    LEGALCARD = 1
    ILLEGALCARD = 2
    WRONGRULE = 15
    BOARDWRONGRULE = 30

class Board_State:
    cardsPlayed = 0
    currentScore = 0
    currentRule = ""
    currentRuleConfidence = 0.0
    totalCardsForRule = {}
    possibleRules = []
    playingLegalCard = True
    cardsToPlay = []
    current_domain = 1

    def __init__(self, prevCards, godrule):  # prevCards = cards on table so far
        self.prevCards = prevCards
        prevString = str(prevCards).strip('[]')
        for i in range(1,14,1):
            for s in ['C', 'D', 'H', 'S']:
                v = new_eleusis.number_to_value(i)
                card = v + s
                self.cardsToPlay.append(card)

        self.setRule(godrule)
        if self.current_domain == 3:
            self.possibleRules = self.forward_checking(build_domain(True, True, True))
        else:
            self.possibleRules = self.forward_checking(build_domain(True))
        self.pickRule()

    def setNewDomain(self):
        if self.current_domain ==1:
            self.current_domain +=1
            self.possibleRules = self.forward_checking(build_domain(True, True))
        else:
            self.declareRule()

    def setRule(self, rule):
        self.rule = rule  # gods rule

    def rule(self):
        return self.rule

    def boardState(self):
        return self.state

    def play(self, card):
        if card == None:
            return
        print "Play number: {} playedcard: {}".format(self.cardsPlayed, card)
        if self.cardsPlayed >=200:
            self.declareRule()
        self.cardsPlayed += 1
        if self.cardsPlayed % 10 == 0:
            self.possibleRules = self.forward_checking(self.possibleRules)
        n = len(self.prevCards)
        self.parsedGodRule = new_eleusis.parse(self.rule)
        if n == 0:
            tuple3 = ("", self.random_card(), card)
        elif 0 < n <= 1:
            tuple3 = ("", self.prevCards[n - 1][0], card)
        else:
            tuple3 = (self.prevCards[n - 2][0], self.prevCards[n - 1][0], card)
        try:
            legalValue = self.parsedGodRule.evaluate(tuple3)
        except:
            print "god rule can't evaluate"
            exit()
        self.updateBoardState(card, legalValue)

    def setCurrentRule(self, rule):
        self.currentRule = rule
        self.currentRuleConfidence = 0.0

    def scientist(self):
        pass

    def score(self):
        return self.currentScore

    def updateBoardState(self,card,legalValue):
        if legalValue:
            c = (card, [])
            self.prevCards.append(c)
            self.updateScore(Score.LEGALCARD)
        else:
            self.prevCards[len(self.prevCards) - 1][1].append(card)
            self.updateScore(Score.ILLEGALCARD)

        if self.playingLegalCard:
            if legalValue:
                self.updatecurrentRuleConfidence(1.0/52)
            else:
                self.updatecurrentRuleConfidence(0)
        else:
            if not legalValue:
                self.updatecurrentRuleConfidence(1.0/52)
            else:
                self.updatecurrentRuleConfidence(0)

    def updateScore(self, value):
        if self.cardsPlayed > 20:
            self.currentScore += value

    def updateCardsPlayed(self, value=1):
        self.cardsPlayed += value
        if self.cardsPlayed >= 200:
            self.declareRule()

    def updatecurrentRuleConfidence(self, value):
        if value > 0:
            self.currentRuleConfidence += value
            if self.currentRuleConfidence >= 15.0/52:  # confidence level to declare rule
                self.declareRule()
            else:
                self.play(self.nextcard())
        else:
            self.currentRuleConfidence = 0
            self.pickRule()

    def pickRule(self):
        if len(self.possibleRules) > 0:
            self.setCurrentRule(self.possibleRules.pop(0))
            self.play(self.nextcard())
        else:
            self.setNewDomain()

    def declareRule(self):
        print "Output Rule: {} score : {} confidence:{}".format(self.currentRule,self.score(),self.currentRuleConfidence)
        exit()
        # return self.currentRule

    def nextcard(self):
        # return card
        card = self.pickCardToTest(self.currentRule)
        return card

    def pickCardToTest(self, rule):
        try:
            p = new_eleusis.parse(rule) # if not parse pick different rule to do
        except:
            self.evaluateFail(rule)
            return self.random_card()
        n = len(self.prevCards)
        r = self.random_card()

        if n == 0:
            print "not enough cards"
        elif n == 1:
            cards = ("",self.prevCards[n-1][0],r)
        else:
            cards = (self.prevCards[n-2][0],self.prevCards[n-1][0],r)
        try:
            b = p.evaluate(cards)
            self.playingLegalCard = b
            return r
        except:
            self.evaluateFail(rule)
            return self.random_card()

        # else:
            # self.pickCardToTest(rule,playingLegalCard)

    def evaluateFail(self,rule):
        if rule in self.possibleRules:
            self.possibleRules.remove(rule)
        self.pickRule()

    def pickCardToTest_old(self, rule, playingLegalCard):
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

    def forward_checking(self, domain):
        # check the domain with variables(c1,c2,..)
        # to play next card we take a rule from satisfing domain
        # if next card is illegal, that means our constraint (next card is legal) is failed,
        # so remove(prune) it from domain and repeat with another rule


        satisfyingDomain = []
        n = len(self.prevCards)
        if n < 3:
            return domain
        for rule in domain:
            p = new_eleusis.parse(rule)
            legalValue = False
            s = self.prevCards
            for i in range(0,len(self.prevCards)-2,1):
                cards = (self.prevCards[i][0],self.prevCards[i+1][0],self.prevCards[i+2][0])
                try:
                    legalValue = p.evaluate(cards)
                except:
                    pass
                if not legalValue:
                    break
            if legalValue:
                satisfyingDomain.append(rule)
        return satisfyingDomain

    def random_card(self):
        r = choice(self.cardsToPlay)
        return r

    def random_card_old(self, value=None, suit=None):
        i = randint(1, 13)
        s = choice('CDHS')
        if value is not None:
            i = choice(value)
        else:
            value = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        if suit is not None:
            s = choice(suit)
        else:
            suit = ['C', 'H', 'D', 'S']

        v = new_eleusis.number_to_value(i)
        card = v + s
        s = self.prevCards
        while card in str(s).strip('[]') and len(self.prevCards) < len(value) * len(suit):
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
    func = ['and','or']
    operators = ['equal','notf']#,'less','greater']
    attributes = ['color','suit','value','is_royal','even']
    cards = ['current']
    values = [['R','B'],['C','H','D','S'],['1','2','3','4','5','6','7','8','9','10','11','12','13'],['True','False'],['True','False']]
    list = []
    for i in operators:
        n=0;
        if i=='equal' or i == 'notf':
            for j in attributes:
                n+=1;
                for k in cards:
                    for v in values[n-1]:
                        #funct = [f]
                        if (i=='notf') and ((j=='suit')or j=='value') or i=='equal':
                            oper = [i]
                            attr = [j]
                            card = [k]
                            value = [v]
                            list.append(construct_rule(1,None,oper,attr,card,value))
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
                    m+=1
                    k=k+1
                    for j2 in attributes:
                        n += 1
                        l=l+1
                        for v in values[m-1]:
                            for v2 in values[n-1]:
                                if(j!=j2):
                                    if (k<l):
                                        if (((i == 'notf' or i2 == 'notf') and ((j == 'suit' or j == 'value') and (j2 == 'suit' or j2 == 'value')))) or (i != 'notf' and i2!='notf'):
                                            fun = h
                                            oper = [i, i2]
                                            attr = [j, j2]
                                            card = [cards[0], cards[1]]
                                            value = [v, v2]
                                            list.append(construct_rule(2,fun,oper,attr,card,value))
                    #values.remove(values[0])
                    n = 0
                    l=0
                    #attributes.remove(attributes[0])
                m=0


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
                                    if (k < l) :
                                        if (((i == 'notf' or i2 == 'notf') and ((j == 'suit' or j == 'value') and (j2 == 'suit' or j2 == 'value')))) or (i != 'notf' and i2!='notf'):
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
    attributes = ['color','suit','value', 'is_royal', 'even']
    cards = ['current', 'previous']
    values = [['R','B'],['C','H','D','S'],['A','2','3','4','5','6','7','8','9','10','J','Q','K'], ['True', 'False'], ['True', 'False']]
    list = []
    m = 0
    n = 0
    card = [cards[1], cards[0]]
    #for h in func:
    for i in operators:
        for i2 in operators:
            for j in attributes:
                m += 1
                for j2 in attributes:
                        n += 1
                        for v in values[m-1]:
                            for v2 in values[n-1]:
                                fun = 'or' #can't actually have just 'and'
                                oper = [i, i2]
                                attr = [j, j2]
                                value = [v, v2]
                                list.append(construct_rule(2,fun,oper,attr,card,value))
                n = 0
            m = 0
    func = ['and', 'or']
    operators = ['greater', 'less']
    attributes = ['value']
    cards = ['current', 'previous']
    values = [['A','2','3','4','5','6','7','8','9','10','J','Q','K']]
    m = 0
    n = 0
    #for h in func:
    for i in operators:
        for i2 in operators:
            for j in attributes:
                m += 1
                for j2 in attributes:
                        n += 1
                        for v in values[m-1]:
                            for v2 in values[n-1]:
                                fun = 'or'
                                oper = [i, i2]
                                attr = [j, j2]
                                value = [v, v2]
                                list.append(construct_rule(2,fun,oper,attr,card,value))
                n = 0
            m = 0
    return list


def domain_3card_rules():
    func = ['and', 'or']
    operators = ['equal', 'notf']
    attributes = ['color','suit','value', 'is_royal', 'even']
    cards = ['current', 'previous', 'previous2']
    values = [['R','B'],['C','H','D','S'],['A','2','3','4','5','6','7','8','9','10','J','Q','K'], ['True', 'False'], ['True', 'False']]
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
                            for v in values[m-1]:
                                for v2 in values[n-1]:
                                    for v3 in values[p-1]:
                                        fun = 'or'
                                        oper = [i, i2, i3]
                                        attr = [j, j2, j3]
                                        value = [v, v2, v3]
                                        list.append(construct_rule(3,fun,oper,attr,card,value))
                        p = 0
                    n = 0
                m = 0
    func = ['and', 'or']
    operators = ['greater', 'less']
    attributes = ['value']
    cards = ['current', 'previous', 'previous2']
    values = [['A','2','3','4','5','6','7','8','9','10','J','Q','K']]
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
                            for v in values[m-1]:
                                for v2 in values[n-1]:
                                    for v3 in values[p-1]:
                                        fun = 'or'
                                        oper = [i, i2, i3]
                                        attr = [j, j2, j3]
                                        value = [v, v2, v3]
                                        list.append(construct_rule(3,fun,oper,attr,card,value))
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






def scientist(cards_on_the_boards_state, initial_number_of_cards, gods_rule):

    bs = Board_State(cards_on_the_boards_state, gods_rule)

    if len(cards_on_the_boards_state) >=2:
        bs.current_domain = 3
    else:
        bs.current_domain = 1
    while bs.cardsPlayed <= 200:
        bs.play(bs.nextcard())
    bs.declareRule()
