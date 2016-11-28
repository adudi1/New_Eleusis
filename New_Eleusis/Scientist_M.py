import new_eleusis
from random import *


class State:
    def __init__(self, prevCards): #prevCards = cards on table so far
        self.prevCards = prevCards

    def setRule(self, rule):
        self.rule = rule # gods rule

    def rule(self):
        return self.rule

    def boardState(self):
        return self.state

    def play(self, card):
        print "playedcard:"
        print card
        n = len(self.prevCards)
        self.parsedGodRule = new_eleusis.parse(self.rule)
        # tuple3 = (self.prevCards[n-2][0],self.prevCards[n-1][0],card)
        tuple3 = ("",self.prevCards[n-1][0],card)
        legalValue = self.parsedGodRule.evaluate(tuple3)
        print "legalValue {}".format(legalValue)
        self.updateBoardState(card, legalValue)
        print prevcards


    def updateBoardState(self,card, legalValue):
        if legalValue:
            c = (card,[])
            self.prevCards.append(c)
        else:
            self.prevCards[len(self.prevCards)-1][1].append(card)
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
    possibleRules = forward_checking(prevcards,domain)
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
    if 'is_royal' in rule:
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


def forward_checking(prevcards, domain):
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
        return domain_3card_rules()
    elif prev:
        return domain_2card_rules()
    else:
        return domain_1card_rules()

def domain_1card_rules():
    func = ['and','or']
    operators = ['equal','notf']#,'less','greater']
    attributes = ['color','suit','value','is_royal','even','odd']
    cards = ['current']
    values = [['R','B'],['C','H','D','S'],['1','2','3','4','5','6','7','8','9','10','11','12','13'],['T','F'],['T','F'],['T','F']]
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
    attributes2 = ['color', 'suit', 'value', 'is_royal', 'even']  # ,'odd']
    m = 0
    n = 0
    k = 0
    l = 0
    for h in func:
        for i in operators:
            for i2 in operators:
                for j in attributes:
                    m+=1
                    k=k+1
                    for j2 in attributes:
                        #if (attributes != 'color'):
                        n += 1
                        l=l+1
                        for v in values[m-1]:
                            for v2 in values[n-1]:
                                #if (v!=v2):
                                if(j!=j2):
                                    if (k<l) and (k!=3) and (k<5):
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
    print list
    return list

def domain_2card_rules():
    func = ['and', 'or']
    operators = ['equal']
    attributes = ['color','suit','value', 'is_royal', 'even']
    cards = ['current', 'prev']
    values = [['R','B'],['C','H','D','S'],['A','2','3','4','5','6','7','8','9','10','J','Q','K'], ['True', 'False'], ['True', 'False']]
    list = []
    m = 0
    n = 0
    for h in func:
        for i in operators:
            for i2 in operators:
                for j in attributes:
                    m += 1
                    for j2 in attributes:
                            n += 1
                            for v in values[m-1]:
                                for v2 in values[n-1]:
                                    fun = h
                                    oper = [i, i2]
                                    attr = [j, j2]
                                    card = [cards[0], cards[1]]
                                    value = [v, v2]
                                    list.append(construct_rule(2,fun,oper,attr,card,value))
                    n = 0
                m = 0
    return list

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
    rule =''
    for i in range(0,args,1):
        oper = operators[i]
        attr = attributes[i]
        card = cards[i]
        value = values[i]
        prule = oper+'('+attr+'('+card+'), '+value+')'
        list.append(prule)
    if len(list)>1:
        s = ', '.join(list)
        rule = func+'('+s+')'
    else:
        rule = list[0]

    return rule

# print construct_rule(2, 'and', ['equal','equal'],['color','color'],['previous','current'],['R','R'])
# and(equal(color(previous),R),equal(color(current),R))
# print "------------------"
# domain_1card_rules()

prevcards = [('3S',[])]
boardState = State(prevcards)
boardState.setRule("equal(color(current), B)") #god rule
boardState.play(nextcard(prevcards))
boardState.play("3H")

#tasks:
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
