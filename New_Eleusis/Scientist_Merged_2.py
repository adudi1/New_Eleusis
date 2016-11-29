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
        print "in init"
        self.prevCards = prevCards
        prevString = str(prevCards).strip('[]')
        for i in range(1,14,1):
            for s in ['C', 'D', 'H', 'S']:
                v = new_eleusis.number_to_value(i)
                card = v + s
                # if card not in prevString:
                self.cardsToPlay.append(card)

        self.setRule(godrule)
        # self.domain = build_domain(True)
        # print self.domain
        if self.current_domain == 3:
            self.possibleRules = self.forward_checking(build_domain(True, True, True))
        else:
            self.possibleRules = self.forward_checking(build_domain(True))
        print "pickrule3"
        self.pickRule()
        print "done init:".format(self.currentRule)

    def setNewDomain(self):
        if self.current_domain ==1:
            self.current_domain +=1
            del self.possibleRules[:]
            self.possibleRules = self.forward_checking(build_domain(True, True))
        # elif self.current_domain ==2:
        #     self.current_domain +=1
        #     del self.possibleRules[:]
        #     self.possibleRules = self.forward_checking(build_domain(True, True, True))
        else:
            print "no domain - declare"
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
        print "\n \nPlay number : ", self.cardsPlayed
        print "playedcard: {}".format(card)
        self.cardsPlayed += 1
        if self.cardsPlayed % 10 == 0:
            self.possibleRules = self.forward_checking(self.possibleRules)
        # if card in self.cardsToPlay:
        #     self.cardsToPlay.remove(card) # check if card in cards to play to do
        # else:
        #     print "card already played {}".format(self.prevCards)
        n = len(self.prevCards)
        print "god:rule: {}".format(self.rule)
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
        print "legalValue {} expected:{}".format(legalValue, self.playingLegalCard)
        self.updateBoardState(card, legalValue)
        print self.prevCards

    def setCurrentRule(self, rule):
        print "setcurrentrule {}".format(rule)
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

        if self.playingLegalCard == legalValue:
            self.updatecurrentRuleConfidence(1.0/52)
        else:
            self.updatecurrentRuleConfidence(0)





    def updateBoardState2(self, card, legalValue):
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
        else:  # when playing a card that should be illegal accori=ding to our current rule
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
        print "\n \n Play number : ", self.cardsPlayed
        if self.cardsPlayed >= 200:
            print "update cards played - declare"
            self.declareRule()

    def updatecurrentRuleConfidence(self, value):
        if value > 0:
            self.currentRuleConfidence += value
            if self.currentRuleConfidence >= 15.0/52:  # confidence level to declare rule
                print "confident - declare"
                self.declareRule()
            else:
                self.play(self.nextcard())
        else:
            self.currentRuleConfidence = 0
            print "pickrule1"
            self.pickRule()

        print "Rule: {} Confidence: {}".format(self.currentRule, self.currentRuleConfidence)

    # def updatecurrentRuleConfidence2(self, value):
    #     if value == Score.LEGALCARD:
    #         fraction = float(1.0 / self.totalCards(self.currentRule))
    #         self.currentRuleConfidence += fraction
    #         if self.currentRuleConfidence >= 30.0/52:  # confidence level to declare rule
    #             print "confident"
    #             self.declareRule()
    #     else:
    #         self.currentRuleConfidence = 0
    #         self.pickRule()
    #     print "Rule: {} Confidence: {}".format(self.currentRule, self.currentRuleConfidence)

    def pickRule(self):
        print "pickrule"
        if len(self.possibleRules) > 0:
            self.setCurrentRule(self.possibleRules.pop(0))
            self.play(self.nextcard())
        else:
            self.setNewDomain()

    def declareRule(self):
        print "Output Rule: {} confidence:{}".format(self.currentRule,self.currentRuleConfidence)
        exit()
        # return self.currentRule

    def nextcard(self):
        # return card
        card = self.pickCardToTest(self.currentRule)
        return card

    # def nextcard2(self, playingLegalCard):
    #     # return card
    #     card = self.pickCardToTest(self.currentRule)
    #     return card

    def pickCardToTest(self, rule):
        # self.playingLegalCard = playingLegalCard
        # print "rule picked: {}".format(rule)
        print "currentrule: {}".format(rule)
        p = new_eleusis.parse(rule) # if not parse pick different rule to do
        print "error here?"
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
            print "card: {} rule: {} eval:{}".format(r, rule,b)
            print "returning: {}".format(r)
            return r
        except:
            self.evaluateFail(rule)

        # else:
            # self.pickCardToTest(rule,playingLegalCard)

    def evaluateFail(self,rule):
        if rule in self.possibleRules:
            self.possibleRules.remove(rule)
        print "pickrule2"
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

        # while len(self.prevCards) < 3:
        #     self.play(self.random_card())

        print "Cards onTable: {}".format(self.prevCards)

        satisfyingDomain = []
        n = len(self.prevCards)
        for rule in domain:
            p = new_eleusis.parse(rule)
            legalValue = False
            s = self.prevCards
            for card in self.prevCards:
                if n == 0:
                    print "not enough cards";
                elif n == 1:
                    cards = ("",self.prevCards[n-1][0],card[0])
                else:
                    cards = (self.prevCards[n-2][0],self.prevCards[n-1][0],card[0])
                # print "cards: {} {}".format(cards, rule)
                legalValue = False
                try:
                    legalValue = p.evaluate(cards)
                except:
                    print "not valid rule"
                if not legalValue:
                    break
            if legalValue:
                satisfyingDomain.append(rule)

        return satisfyingDomain

    def random_card(self):
        print "cards: {} {}".format(self.cardsToPlay, self.prevCards)
        r = choice(self.cardsToPlay)
        print "R** : {}".format(r)
        return r

    def random_card_old(self, value=None, suit=None):
        # random_card()
        # select a random odd red card
        # random_card([1,3,5,7,9,11,13],['D','H'])
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
        print "self.prevCards: {}".format(self.prevCards)
        s = self.prevCards
        while card in str(s).strip('[]') and len(self.prevCards) < len(value) * len(suit):
            # print "card in prevcards: True {} {}".format(card, self.prevCards)
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
    #for f in func:
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
    #print list
    #return list
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
    print list
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
    #for h in func:
        #for h2 in func:
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
    #for h in func:
        #for h2 in func:
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


# print construct_rule(2, 'and', ['equal','equal'],['color','color'],['previous','current'],['R','R'])
# and(equal(color(previous),R),equal(color(current),R))
# print "------------------"
# domain_1card_rules()




def scientist(cards_on_the_boards_state, initial_number_of_cards, gods_rule):

    # print domain_1card_rules()
    # print domain_2card_rules()
    # print domain_3card_rules()

    # global prevcards
    #prevcards = [('3S', [])]
    # prevcards = cards_on_the_boards_state
    print "Marker : Stuff before board state object declaration"
    #boardState = State(prevcards, "equal(color(current), B)")
    bs = Board_State(cards_on_the_boards_state, gods_rule)
    print "Marker : Stuff after board state object declaration. /n The while counter starts here \n"
    if len(cards_on_the_boards_state) >=2:
        bs.current_domain = 3
    else:
        bs.current_domain = 1
    whilecounter = 0
    while bs.cardsPlayed <= 200:
        print "\n \n Whilenumber cardsplayed : ", bs.cardsPlayed
        whilecounter += 1
        print "\n\tThe while counter value is ", whilecounter

        bs.play(bs.nextcard())
    print "plays >200 -declare"
    bs.declareRule();
    #if its more than 200 print message that it crossed 200
    print bs.score()

#
# prevcards = [('3S', [])]
# boardState = Board_State(prevcards, "equal(color(current), B)")