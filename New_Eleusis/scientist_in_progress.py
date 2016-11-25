
class State:

    def __init__(self, state):
        self.state = state

    def setRule(self, rule):
        self.rule = rule

    def rule(self):
        return self.rule

    def boardState(self):
        return self.state

    def play(self,card):
        #to do
        pass

    def scientist(self):
        pass

    def score(self):
        pass


def hypothesis():
    #rules involving only one card
    theSuit = suit(state[0])
    theColor = color(state[0])
    theValue = value(state[0])
    isRoyal = is_royal(state[0])
    isEven = even(state[0])
    isOdd = odd(state[0])
    for (i in range(1, size(state))):
        if not (isEqual(theSuit, suit(state[i]))):
            theSuit = -1 #-1 means that this is not a one-card rule
        if not (isEqual(theColor, color(state[i]))):
            theColor = -1 #-1 means that this is not a one-card rule
        if not (isEqual(theValue, value(state[i]))):
            theValue = -1 #-1 means that this is not a one-card rule
        if not (isEqual(isRoyal, is_royal(state[i]))):
            isRoyal = -1 #-1 means that this is not a one-card rule
        if not (isEqual(isEven, even(state[i]))):
            isEven = -1
        if not (isEqual(isOdd, odd(state[i]))):
            isOdd = -1
    if not (theSuit == -1):
        return theSuit #slight pseudocode, return a rule that suit = theSuit
    if not (theColor == -1):
        return theColor
    if not (theValue == -1):
        return theValue
    if not (isRoyal == -1):
        return isRoyal
    if not (isEven == -1):
        return isEven
    if not (isOdd == -1):
        return isOdd
    #now try 2-card rules
    theRule = None
    for (i in range(1, size(state))):
        prev = state[i-1]
        current = state[i]
        
    if not (theRule == None):
        return theRule
    #now try 3-card rules
    pass

def card():
    #return card to be played to test hypothesis
    pass

