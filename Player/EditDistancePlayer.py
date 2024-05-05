# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:52:08 2024

@author: jjb24
"""
from Player import Player
import nltk


###
# This player uses the Word embedding distance between strings to determine 
# similarity.  
###
class EditDistancePlayer(Player):

    PLAYER_NAME = "EditDistance Player" # Choose a unique name for your player
    
    def __init__(self):
        super().__init__(self.PLAYER_NAME)


    def choose_card(self, target, hand):
        ### Select the index of the card from the cards list that is closest to target
        bestCardNdx = 0
        bestDistance = nltk.edit_distance(target, hand[0])
        for i in range(1,len(hand)):
            dist = nltk.edit_distance(target, hand[0])
            if dist < bestDistance:
                bestDistance = dist
                bestCardNdx = i
        return bestCardNdx

    
    def judge_card(self, target, player_cards):
        ### Select the card that is closest to target
        bestCard = player_cards[0]
        bestDistance = nltk.edit_distance(target, player_cards[0])
        for i in range(1, len(player_cards)):
            dist = nltk.edit_distance(target, player_cards[0])
            if dist < bestDistance:
                bestDistance = dist
                bestCard = player_cards[i]
        return bestCard
        
    
    def process_results(self, result):
        ### Handle results returned from server
        print("Result", result)

if __name__ == '__main__':
    player = EditDistancePlayer()
    player.run()