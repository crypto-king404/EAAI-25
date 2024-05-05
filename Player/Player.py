# -*- coding: utf-8 -*-
"""
Created on Thu May  2 18:25:27 2024

@author: jjb24
"""
from time import sleep
import requests
import json
import ast

class Player(object):
    
    # The first three methods must be overridden
    def __init__(self, name):
        self.URL = "http://localhost:8000/player"
        self.name = name
    
    def choose_card(self, target, hand):
        return None

    def judge_card(self, target, player_cards):
        return None
        
    def process_results(self, result):
        pass
    
    def send_register_player_message(self):
        try:
            request = {'action':'register','name':self.name}
            resp = requests.post(self.URL, json=request)
            
            resp_data = ast.literal_eval(resp.text)
            if 'status' in resp_data and resp_data['status'] == 'ok':
                print("Player registered with id", resp_data['id'])
                return int(resp_data['id'])
            
            print("Error in response:", str(resp_data))
            return -1
        except Exception as e:
            print("Error registering player:", e)
            return -1
    
    def send_message(self,request):
        try:
            resp = requests.post(self.URL, json=request)
            resp_data = ast.literal_eval(resp.text)
            if 'status' in resp_data and resp_data['status'] == 'ok':
                return
            
            print("Error in response:", str(resp_data), "for message:", str(request))
            self.gameInProcess = False

        except Exception as e:
            print("Error sending message:", str(request), "Error:", e)
            self.gameInProcess = False
    
        
    def poll_server(self):
        try:
            request = {'action':'get_status','id':self.pid}
            resp = requests.post(self.URL, json=request)
            
            resp_data = ast.literal_eval(resp.text)
            if 'status' in resp_data and resp_data['status'] == 'ok':
                for message in resp_data['message']:
                    self.process_message(message)
            else:
                print("Error in response:", str(resp_data))
                self.gameInProcess = False
        except Exception as e:
            print("Error polling server for messages:", e)
            self.gameInProcess = False
    
    def process_message(self, message): 
        try:
            if isinstance(message, str):
                message = ast.literal_eval(message)
            if 'type' not in message:
                print("Error processing message.  No type field: " + str(message))
            else:
                if message['type'] == "choosing":
                    choice = self.choose_card(message['target'], message['cards'])
                    self.send_message({'action':'submit_card','id':self.pid,'card': choice})
                elif message['type'] == "judging":
                    choice = self.judge_card(message['target'], message['choices'])
                    self.send_message({'action':'judge_card','id':self.pid,'card': choice})
                elif message['type'] == "summary":
                    if 'gameOver' in message:
                        self.gameInProcess = False
                    self.process_results(message['recap'])
                else:
                    print("Unknown message type: " + str(message))   
                    self.gameInProcess = False
        except Exception as e:
            print("Error processing message: " + str(message),e)
            self.gameInProcess = False

    def run(self):
        self.pid = self.send_register_player_message()
        self.gameInProcess = True
        if self.pid >= 0:
            while self.gameInProcess:
                try:
                    sleep(0.25)
                    self.poll_server()
                except KeyboardInterrupt:
                    self.gameInProcess = False    