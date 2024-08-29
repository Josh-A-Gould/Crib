import itertools
import random
import time

Suits = ["H", "C", "D", "S"]
Values = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]

Cards_List = ["".join(i) for i in itertools.product(Values, Suits)]

def Deal(Cards_List):
    Cards_List_Tmp = Cards_List.copy()
    DealerH = []
    PlayerH = []

    while len(DealerH) != 6:
        Dealt_Card = random.choice(Cards_List_Tmp)
        DealerH.append(Dealt_Card)
        Cards_List_Tmp.remove(Dealt_Card)

        Dealt_Card = random.choice(Cards_List_Tmp)
        PlayerH.append(Dealt_Card)
        Cards_List_Tmp.remove(Dealt_Card)

    Turn_Card = random.choice(Cards_List_Tmp)

    DealerH = [PartedCard(card) for card in DealerH]   
    PlayerH = [PartedCard(card) for card in PlayerH]
    Turn_Card = PartedCard(Turn_Card)

    return DealerH, PlayerH, [Turn_Card]

def PartedCard(Card):
    Parted = []

    Value = lambda a : 1 if (Card[0] == "A") else (10 if Card[0] in ["J", "Q", "K"] else int(Card[:-1]))

    Parted.extend((Card[:-1], Card[-1:], Value(Card[0])))

    return Parted

def Throw(DealerH, PlayerH, Dealer):
    Crib = []    
    
    if Dealer == 1:
        Throw = input("From the following cards which do you wish to throw to your crib? "+str(DealerH)+"\n")
        try:
            Crib += [DealerH[int(Throw[0])-1]]
            Crib += [DealerH[int(Throw[1])-1]]
        except: 
            raise ValueError("Please enter two integers in the format xx")
        DealerH.pop(int(Throw[1])-1)
        DealerH.pop(int(Throw[0])-1)

        Crib += PlayerH[4:]        
        PlayerH = PlayerH[:4]
    elif Dealer == 2:
        Throw = input("From the following cards which do you wish to throw to opponents crib? "+str(PlayerH)+"\n")
        try:
            Crib += [PlayerH[int(Throw[0])-1]]
            Crib += [PlayerH[int(Throw[1])-1]]
        except: 
            raise ValueError("Please enter two integers in the format xx")
        PlayerH.pop(int(Throw[1])-1)
        PlayerH.pop(int(Throw[0])-1)

        Crib += DealerH[4:]        
        DealerH = DealerH[:4]
    else:
        raise ValueError("Dealer value of non-(1/2)")

    return DealerH, PlayerH, Crib

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

    while n >= 3 and runs == False:
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
                pairs += 1

    return pairs

def FlushPts(hand):
    flushPts = 0

    if hand[0][1] == hand[1][1] == hand[2][1] == hand[3][1]:
        if hand[4][1] == hand[0][1]:
            flushPts = 5
        else:
            flushPts = 4

    return flushPts

def NibsPts(hand, turn):
    for x in hand:
        if x[0] == "J" and x[1] == turn[0][1]:
            return 1
    else:
        return 0

def NobsPts(turn):
    if turn[0][0] == "J":
        return 2
    else:
        return 0

def Cut(Cards_List):
    Cards_List_Tmp = Cards_List.copy()
    P1Card = []
    P2Card = []

    P1_Card = random.choice(Cards_List_Tmp)
    Cards_List_Tmp.remove(P1_Card)

    P2_Card = random.choice(Cards_List_Tmp)
    Cards_List_Tmp.remove(P2_Card)

    print(P1_Card, P2_Card)

    P1_Card, P2_Card = PartedCard(P1_Card), PartedCard(P2_Card)

    if P1_Card[2] > P2_Card[2]:
        First = 2
    elif P1_Card[2] < P2_Card[2]:
        First = 1
    else:
        First = Cut(Cards_List)

    return First

def Main():
    global P1Pts
    global P2Pts

    P1Pts = 0
    P2Pts = 0

    FirstCrib = Cut(Cards_List)

    while True:
        Hand(FirstCrib)
        Hand(FirstCrib%2 + 1)
        if P1Pts >= 121 or P2Pts >= 121:
            break

    if P1Pts >= 121:
        print("P1 wins")
    elif P2Pts >= 121:
        print("P2 wins")

    print(P1Pts, P2Pts)

def Hand(Dealer):
    global P1Pts
    global P2Pts

    DealerH, PlayerH, Turn = Deal(Cards_List)

    if Dealer == 1:
        P1Pts += NobsPts(Turn)
    else:
        P2Pts += NobsPts(Turn)

    if P1Pts >= 121 or P2Pts >= 121:
        print("This shouldn't have happened")
        return

    DealerH, PlayerH, Crib = Throw(DealerH, PlayerH, Dealer)

    print(DealerH, PlayerH, Crib, Dealer, P1Pts, P2Pts)

    combs = Combs(PlayerH+Turn)

    PlayerPts = Count15s(combs) * 2 + CountPairs(combs) * 2 + FlushPts(PlayerH+Turn) + CountRuns(combs) + NibsPts(PlayerH, Turn)

    combs = Combs(DealerH+Turn)

    DealerPts = Count15s(combs) * 2 + CountPairs(combs) * 2 + FlushPts(DealerH+Turn) + CountRuns(combs) + NibsPts(DealerH, Turn)

    if Dealer == 1:
        P2Pts += PlayerPts
        if P2Pts >= 121:
            return
        P1Pts += DealerPts
    else:
        P1Pts += PlayerPts
        if P1Pts >= 121:
            return
        P2Pts += DealerPts

Main()