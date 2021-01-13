import os
import random
import numpy as np
import pandas as pd

def deal(deck):
    hand = []
    for i in range(2):
        random.shuffle(deck)
        card = deck.pop()
        hand.append(card)
    return hand

def hit(hand, deck):
    card = deck.pop()
    hand.append(card)
    return hand

def total(hand):
    t = 0
    count_i = hand.count('I')
    count_a = hand.count('A')
    for card in hand:
        if card == "J" or card == "Q" or card == "K":
            t += 10
        elif card == "I":
            continue
        elif card == "A":
            t += 11
        else:t += card
    if count_i%4==1:
        t += 0
    elif count_i%4==2:
        t += -1
    elif count_i%4==3:
        t += 0
    elif count_i%4==0 and count_i!=0:
        t += 1
    while t > 21 and count_a>0:
        t -= 10
        count_a -=1
    return t

def dealers_strategy(hand, deck):
    while total(hand)<17:# or total(hand) in [22]:
        hand = hit(hand, deck)
    return hand

def players_strategy(hand, deck, stand):
    while total(hand)<stand:# or total(hand) in [22]:
        hand = hit(hand, deck)
    return hand

def payoff(players_hand, dealers_hand):
    player_total = total(players_hand)
    dealer_total = total(dealers_hand)
    if player_total == 21 and len(players_hand)==2 and dealer_total == 21 and len(dealers_hand)==2:
        return 0
    elif dealer_total == 21 and len(dealers_hand)==2:
        return -1
    elif player_total == 21 and len(players_hand)==2:
        return 1.5
    elif player_total > 21:
        return -1
    elif dealer_total>21 and player_total <= 21:
        return 1
    elif player_total > dealer_total:
        return 1
    elif player_total == dealer_total:
        return 0
    elif dealer_total > player_total:
        return -1
    else:
        print('player', players_hand, player_total)
        print('dealer', dealers_hand, dealer_total)

def play(n=1, stand=17):
    games = []
    for i in range(n):
        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']*4 + ['I']*8
        dealers_hand = deal(deck)
        players_hand = deal(deck)

        players_hand = players_strategy(players_hand, deck, stand)
        dealers_hand = dealers_strategy(dealers_hand, deck)
        games.append(payoff(players_hand, dealers_hand))
    return np.array(games)

data = {'stand':[], 'result':[]}
for stand in range(5,21):
    result = play(10000000, stand).mean()
    data['stand'].append(stand)
    data['result'].append(result)
    print(f'End {stand} with mean {result}')
pd.DataFrame(data).set_index('stand').plot(kind='bar')