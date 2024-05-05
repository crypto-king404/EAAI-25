# -*- coding: utf-8 -*-
"""
Created on Thu May  2 10:21:04 2024

@author: jjb24
"""

import random
import queue

class Game:
    HAND_SIZE = 7 # Noun cards per hand
    MAX_SCORE = 3 # Game ends when a player reaches the max score or we run out of cards
    
    def __init__(self):
        self.reset()

    def reset(self):
        # Reading and initializing noun cards
        with open('cards/nouns.txt', 'r') as f:
            self.noun_cards = [line.strip() for line in f]
        random.shuffle(self.noun_cards)
        
        # Reading and initializing adjective cards
        with open('cards/adjectives.txt', 'r') as f:
            self.adjective_cards = [line.strip() for line in f]
        random.shuffle(self.adjective_cards)
        
        self.players = {}
        self.rounds_played = 0
        self.state = "registering"
        self.judge_order = queue.Queue()
        self.messages = {'master': queue.Queue()}
        
    def register_player(self, name):
        if self.state != "registering":
            return False, "Game is underway.  New players cannot be registered"
        else:
            if len(self.noun_cards) < self.HAND_SIZE:
                return False, "Insufficient noun cards available to create a new player."
                
            player_id = random.randint(1,1_000_000_000)
            while (player_id in self.players):
                player_id = random.randint(1,1_000_000_000)
            self.players[player_id] = {'name': name, 'score': 0, 'cards': [self.noun_cards.pop() for i in range(self.HAND_SIZE)]}
            self.judge_order.put(player_id)
            self.messages[player_id] = queue.Queue()
            self.send_message("Player '" + name + "' registered with id " + str(player_id), "master")
            return True, str(player_id)

    def start_round(self):
        if self.state == "done":
            return False, "Game is completed."
        if len(self.players) < 3:
            return True, "You need at least 3 players to play a game."
            
        self.judge = self.judge_order.get()
        self.judge_order.put(self.judge)
        
        if len(self.adjective_cards) == 0:
            self.state = "done"
            return False, "No more adjective cards left. Game complete."
        self.target_card = self.adjective_cards.pop()
        
        for pid in self.players:
            while len(self.players[pid]['cards']) < self.HAND_SIZE:
                if len(self.noun_cards) == 0:
                    self.state = "done"
                    return False, "No more noun cards left. Game complete."
                self.players[pid]['cards'].append(self.noun_cards.pop())
        
        self.state = "round started"
        #self.send_message("Round started.  Target card: '" + self.target_card + "'", "master")
        self.submitted_cards = {}
        self.chosen_card = None
        
        for pid in self.players:
            if pid != self.judge:
                self.send_message({'type': 'choosing', 'target': self.target_card, 'cards': self.players[pid]['cards']}, pid)
                
        return True, "Round started.  Target word: " + self.target_card
        
    def submit_card(self, pid, card_num):
        if self.state == "done":
            return False, "Game is completed."
            
        if self.state != "round started":
            return True, "Guesses can only be registered during the first phase of a round."

        if pid not in self.players:
            return False, "Bad player id: " + str(pid)

        if card_num < 0 or card_num >= self.HAND_SIZE:
            return True, "Player guess must be between 0 and " + (str(self.HAND_SIZE)-1) + ", inclusive. Received " + card_num
        
        if pid in self.submitted_cards:
            return True, "Player has alread registered a guess."


        card = self.players[pid]["cards"].pop(card_num)

        self.submitted_cards[pid] = card
        self.send_message("Player '" + self.players[pid]['name'] + "' played '" + card + "' over other choices: " + str(self.players[pid]["cards"]), "master")
        return True,""

    def judge_card(self, pid, chosen_card):
        if self.state == "done":
            return False, "Game is completed."

        if self.state != "judging":
            return True, "A card can only be chosen in the judging phase of a round."

        if pid != self.judge:
            return True, "Only the judge can select a card judge id (" + str(self.judge) + "), choosing player id (" + str(pid) + ")"

        self.chosen_card = chosen_card
        
        self.send_message("Judge '" + self.players[self.judge]['name'] + "' selected '" + chosen_card + "'", "master")
        return True, "Choice recorded."


    def start_judging(self):
        if self.state == "done":
            return False, "Game is completed."

        if self.state != "round started":
            return True, "A round can only be judged if it is in the started state."

        for pid in self.players:
            if pid not in self.submitted_cards and pid != self.judge:
                random_card = random.randrange(0, self.HAND_SIZE)
                self.submit_card(pid, random_card)
                self.send_message("A card was not recieved from " + self.players[pid]['name'] + ". Randomly selecting '" + self.submitted_cards[pid] + "' for this player.", "master")                                

        guesses = []            
        for pid in self.submitted_cards:
            guesses.append(self.submitted_cards[pid])
                
        random.shuffle(guesses)
        self.state = "judging"
        
        message = {'type': 'judging', 'target': self.target_card, 'choices': guesses}
        
        self.send_message(message, self.judge)
        
        return True,""
            
    def end_round(self):
        if self.state == "done":
            return False, "Game is completed."

        summary = {'type': 'summary'}
        if self.state != "judging":
            return True, "A card can only be selected by a judge when the game is in the judging phase."
        
        chosen_pid = None
        for pid in self.submitted_cards:
            if self.chosen_card == self.submitted_cards[pid]:
                chosen_pid = pid
                break
        
        if self.chosen_card is None:
            self.send_message("The card chosen by the judge '" + str(self.chosen_card) + "' is not in the list of selected cards. Randomly selecting winner", "master")    
            ndx = random.randrange(0,len(self.submitted_cards))
            for pid in self.submitted_cards:
                if ndx == 0:
                    chosen_pid = pid
                    break
                ndx -= 1
        self.players[chosen_pid]['score'] += 1

        # Send message to Web controller        
        results = "Round winner: '" + self.players[chosen_pid]['name'] + "'.<BR><TABLE class='center'><TR><TH>Team</TH><TH>Score</TH></TR>"
        scoreboard = []
        for pid in self.players:
            scoreboard.append((self.players[pid]['name'], self.players[pid]['score']))
        scoreboard = sorted(scoreboard, key= lambda x: x[1])
        for score in scoreboard:
            results += "<TR><TD>" + str(score[0]) + "</TD><TD>" + str(score[1]) + "</TD></TR>"
        results += "</TABLE>"
        self.send_message(results, "master")
        
        if self.players[chosen_pid]['score'] >= self.MAX_SCORE:
            self.send_message("Game over.", 'master')
            self.state = "done"
            summary['game_over'] = True
        else:
            self.state = "round over"     
            
        # Send message to players
        recap = {}
        recap['round_winner'] = self.players[chosen_pid]['name']
        recap['target_card'] =  self.target_card
        recap['submitted_cards'] =  []
        recap['scores'] = []
        for pid in self.submitted_cards:
            recap['submitted_cards'].append((self.players[pid]['name'], self.submitted_cards[pid]))
            recap['scores'].append((self.players[pid]['name'], self.players[pid]['score']))
        summary['recap'] = recap
        
        for pid in self.players:
            self.send_message(summary, pid)
        
        return True, ""



    def send_message(self, message, key):
        self.messages[key].put(str(message))
        
    def read_messages(self, key):
        if key not in self.messages:
            return False, "unknown player id '" + str(key) + "'"
        results = []
        while not self.messages[key].empty():
            results.append(self.messages[key].get())
        return True,results
    

