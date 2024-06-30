import itertools
import random
import time

Suits = ["H", "C", "D", "S"]
Values = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]

Cards_List = ["".join(i) for i in itertools.product(Values, Suits)]

def Deal(Cards_List = Cards_List):
    DealerH = []
    PlayerH = []

    while len(DealerH) != 6:
        Dealt_Card = random.choice(Cards_List)
        DealerH.append(Dealt_Card)
        Cards_List.remove(Dealt_Card)

        Dealt_Card = random.choice(Cards_List)
        PlayerH.append(Dealt_Card)
        Cards_List.remove(Dealt_Card)

    Turn_Card = random.choice(Cards_List)

    DealerH = [PartedCard(card) for card in DealerH]   
    PlayerH = [PartedCard(card) for card in PlayerH]
    Turn_Card = PartedCard(Turn_Card)

    return DealerH, PlayerH, [Turn_Card]

def PartedCard(Card):
    Parted = []

    Value = lambda a : 1 if (Card[0] == "A") else (10 if Card[0] in ["J", "Q", "K"] else int(Card[:-1]))

    Parted.extend((Card[:-1], Card[-1:], Value(Card[0])))

    return Parted

def Throw(DealerH, PlayerH):
    Crib = []
    Crib += DealerH[4:]
    Crib += PlayerH[4:]
    DealerH = DealerH[:4]
    PlayerH = PlayerH[:4]
    return Crib, DealerH, PlayerH

def Combs(Hand):
    if len(Hand) == 0:
        return [[]]
    cs = []
    for c in Combs(Hand[1:]):
        cs += [c, c+[Hand[0]]]
    return cs

def Count15s(combs):
    count = 0
    for x in combs: 
        sum = 0
        try:
            for y in x:
                sum += y[2]
        except IndexError:
            pass
        if sum == 15:
            count += 1
    return count

def CountRuns(combs):
    for x in combs:
        for y in x:
            if y[0] == "A":
                y[2] = 1
            elif y[0] == "J":
                y[2] = 11
            elif y[0] == "Q":
                y[2] = 12
            elif y[0] == "K":
                y[2] = 13

    n = 5
    runs = False
    runPts = 0

    while n >= 3:
        CheckList = [x for x in combs if len(x) == n]
        for x in CheckList:
            Values = [y[2] for y in x]
            Values = [x - min(Values) for x in Values]

            if list(range(n)) == sorted(Values):
                runs = True
                runPts += n
        n -= 1

    return runPts

def CountPairs(combs):
    pairs = 0
    for x in combs:
        if len(x) == 2:
            if x[0][0] == x[1][0]:
                pairs += 1#

    return pairs

def FlushPts(combs):
    flushPts = 0

    for x in combs:
        if len(x) == 5:
            if x[1][1] == x[2][1] == x[3][1] == x[4][1]:
                if x[4][1] == x[0][1]:
                    flushPts = 5
                else:
                    flushPts = 4

    return flushPts

DealerH, PlayerH, Turn = Deal()

DealerH, PlayerH, Crib = Throw(DealerH, PlayerH)

combs = Combs(DealerH+Turn)
 
fifteenxTwos = Count15s(combs) * 2
pairPts = CountPairs(combs) * 2
flush = FlushPts(combs)
runPts = CountRuns(combs)

print(pairPts, fifteenxTwos, flush, runPts, DealerH+Turn)

