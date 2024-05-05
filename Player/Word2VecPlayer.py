# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:52:08 2024

@author: jjb24
"""
import gensim.downloader as api
from Player import Player

###
# This player uses the Word embedding distance between strings to determine 
# similarity.  
###
class Word2VecPlayer(Player):

    PLAYER_NAME = "Word2Vec Player" # Choose a unique name for your player
    
    def __init__(self):
        self.word_vectors = api.load("glove-wiki-gigaword-100")
        super().__init__(self.PLAYER_NAME)


    def choose_card(self, target, hand):
        ### Select the index of the card from the cards list that is closest to target
        bestCardNdx = 0
        bestSim = self.word_vectors.similarity(target, hand[0])
        for i in range(1,len(hand)):
            sim = self.word_vectors.similarity(target, hand[0])
            if sim > bestSim:
                bestSim = sim
                bestCardNdx = i
        return bestCardNdx
    
    def judge_card(self, target, player_cards):
        ### Select the card that is closest to target
        bestCard = player_cards[0]
        bestSim = self.word_vectors.similarity(target, player_cards[0])
        for i in range(1, len(player_cards)):
            sim = self.word_vectors.similarity(target, player_cards[0])
            if sim > bestSim:
                bestSim = sim
                bestCard = player_cards[i]
        return bestCard
        
    
    def process_results(self, result):
        ### Handle results returned from server
        print("Result", result)

if __name__ == '__main__':
    player = Word2VecPlayer()
    player.run()
