# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:52:08 2024

@author: jjb24
"""
import random
from Player import Player

###
# This player makes all choices completely at random
###
class RandomPlayer(Player):

    PLAYER_NAME = "Random Player" # Choose a unique name for your player
    
    def __init__(self):
        super().__init__(self.PLAYER_NAME)


    def choose_card(self, target, hand):
        ### Select the index of the card from the cards list that is closest to target
        return random.randrange(0,len(hand))
    
    
    def judge_card(self, target, player_cards):
        ### Select the card that is closest to target
        return player_cards[random.randrange(0,len(player_cards))]
        
    
    def process_results(self, result):
        ### Handle results returned from server
        print("Result", result)

if __name__ == '__main__':
    player = RandomPlayer()
    player.run()
