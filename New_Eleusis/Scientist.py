import new_eleusis
from random import *


class State:
    def __init__(self, prevCards):
        self.prevCards = prevCards

    def setRule(self, rule):
        self.rule = rule

    def rule(self):
        return self.rule

    def boardState(self):
        return self.state

    def play(self, card):
        print "playedcard:"
        print card
        n = len(prevcards)
        self.parsedGodRule = new_eleusis.parse(self.rule())
        tuple3 = (self.prevCards(n-2)[0],self.prevCards(n-1)[0],card)
        legalValue = self.parsedGodRule.evaluate(tuple3)
        print "legalValue {}".format(legalValue)
        self.updateBoardState(card, legalValue)


    def updateBoardState(self,card, legalValue):
        if legalValue:
            c = (card,[])
            self.prevCards.append(c)
        else:
            self.prevCards[len(self.prevcards)-1][2][0] = card
            pass

    def scientist(self):
        pass

    def score(self):
        pass


def nextcard(prevcards):
    # hyp = traverse_hypothesisSpace(prevcards)
    # card = test_hyp(hyp)
    # return card
    domain = build_domain(True)
    print domain
    possibleRules = checkDomainWithVariables(prevcards,domain)
    card = pickCardToTest(possibleRules[0])
    print "Rule Testing: {}".format(possibleRules[0])
    return card

def pickCardToTest(rule):
    values = satisfying_values(rule)
    suit = satisfying_suits(rule)
    return random_card(values,suit)

def satisfying_values(rule):
    #improve
    if 'odd' in rule:
        return [1,3,5,7,9,11,13]
    if 'even' in rule:
        return [2,4,6,8,10,12]
    if 'royal' in rule:
        return [1,11,12,13]
    return [1,2,3,4,5,6,7,8,9,10,11,12,13]



def satisfying_suits(rule):
    #improve
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


def random_card(value=None, suit=None):
    # random_card()
    # select a random odd red card
    # random_card([1,3,5,7,9,11,13],['D','H'])
    i = randint(1, 13)
    s = choice('CDHS')
    if value is not None:
        i = choice(value)
    if suit is not None:
        s = choice(suit)

    v = new_eleusis.number_to_value(i)
    card = v + s
    return card





def cardProperties(card):
    #to do : add more properties
    return {'suit':new_eleusis.suit(card),'value':new_eleusis.value(card),'color':new_eleusis.color(card)}


def checkDomainWithVariables(prevcards, domain):
    # check the domain with variables(c1,c2,..)
    # to play next card we take a rule from satisfing domain
    # if next card is illegal, that means our constraint (next card is legal) is failed,
    # so remove(prune) it from domain and repeat with another rule

    # for rule based on one card
    satisfyingDomain = []
    n = len(prevcards)
    for rule in domain:
        p = new_eleusis.parse(rule)
        legalValue = False
        for card in prevcards:
            # improve
            # putting a random card as there is only one card now
            cards = ("",random_card(),card[0])
            legalValue = p.evaluate(cards)
            if not legalValue:
                break
        if legalValue:
            satisfyingDomain.append(rule)
    return satisfyingDomain

def variables():
    # contraints between cards
    pass

def constraints():
    # next card should evaluate to true
    pass

# def domain():
#     return build_domain()

def build_domain(current=True,prev=False,prev2=False):
    if prev2:
        return build_prev2_curr_domain()
    elif prev:
        return build_prev_curr_domain()
    else:
        return build_curr_domain()


def build_curr_domain():
    func = ['and','or']
    operators = ['equal']
    attributes = ['color','suit']
    cards = ['current']
    values = [['R','B'],['C','H','D','S']]
    list = []
    n =0
    for i in operators:
        for j in attributes:
            n+=1
            for k in cards:
                for v in values[n-1]:
                    #for v in l:
                    oper = [i]
                    attr = [j]
                    card = [k]
                    value = [v]
                    list.append(construct_rule(1,None,oper,attr,card,value))

    print list
    return list

def build_prev_curr_domain():
    # for 2 card rules
    pass

def build_prev2_curr_domain():
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
    rule =''
    for i in range(0,args,1):
        oper = operators[i]
        attr = attributes[i]
        card = cards[i]
        value = values[i]
        prule = oper+'('+attr+'('+card+'), '+value+')' #throwing error here? #'str' object is not callable
        list.append(prule)
    if len(list)>1:
        s = ', '.join(list)
        rule = func+'('+s+')'
    else:
        rule = list[0]

    return rule

# print construct_rule(2, 'and', ['equal','equal'],['color','color'],['previous','current'],['R','R'])
# print "------------------"
# build_curr_domain()

prevcards = [('3S',[])]
boardState = State(prevcards)
boardState.setRule('equal(color(current), B)') #god rule
boardState.play(nextcard(prevcards))
