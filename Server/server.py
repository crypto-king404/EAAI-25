# Web server adapted from Andrew Klatzke's server code at https://github.com/aklatzke/python-webserver-part-2/blob/master/main.py

import os
import json
from http.server import BaseHTTPRequestHandler
from game import Game
from response.staticHandler import StaticHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler

routes = {
    "/" : {
        "template" : "index.html" 
    },
}

class Server(BaseHTTPRequestHandler):
    
    VERBOSE = False # Set to true to see messages about each request
    
    game = Game()
    
    def do_HEAD(self):
        return

    def do_GET(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]

        if request_extension == "" or request_extension == ".html":
            if self.path in routes:
                handler = TemplateHandler()
                handler.find(routes[self.path])
            else:
                handler = BadRequestHandler()
        elif request_extension == ".py":
            handler = BadRequestHandler()
        else:
            handler = StaticHandler()
            handler.find(self.path)
 
        self.respond({
            'handler': handler
        })
        
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        if self.path == "/admin":
            response = self.handle_admin()
        elif self.path == "/player":
            response = self.handle_player()
        else:
            response = json.dumps({'status':'error','message':'unrecognized path: ' + self.path})
        
        self.wfile.write(response.encode(encoding='utf_8'))                
            
    def handle_http(self, handler):
        status_code = handler.getStatus()

        self.send_response(status_code)

        if status_code == 200:
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())
        else:
            content = "404 Not Found"

        self.end_headers()

        if isinstance(content, bytes):
            return content
        else:
            return bytes(content, 'UTF-8')

    # Handle requests from web page
    def handle_admin(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = json.loads(self.rfile.read(content_length)) 
        if 'action' not in post_data:
            response = json.dumps({'status':'error','message':'Message must contain an action field.'})
        elif post_data['action'] == "/start":
            self.game.reset()
            response = json.dumps({'status':'ok','message':'Restarting. Note players must reregister.'})
            
        elif post_data['action'] == "play_round":
            res, message = self.game.start_round()
            if res:
                response = json.dumps({'status':'ok','message':message})
            else:
                response = json.dumps({'status':'error','message':message})
                
        elif post_data['action'] == "judge_round":
            res, message = self.game.start_judging()
            if res:
                response = json.dumps({'status':'ok','message':message})
            else:
                response = json.dumps({'status':'error','message':message})

        elif post_data['action'] == "end_round":
            res, message = self.game.end_round()
            if res:
                response = json.dumps({'status':'ok','message':message})
            else:
                response = json.dumps({'status':'error','message':message})
                
        elif post_data['action'] == "server_update":
            res, details = self.game.read_messages("master")
            if res:
                response = json.dumps({'status':'ok', 'results': details})
            else:
                response = json.dumps({'status':'error', 'message': details})
        else:
            response = json.dumps({'status':'error', 'message': 'Unknown action: "' + str(post_data['action'] + '"')})
            
        return response

    # Handle requests from the players
    def handle_player(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = json.loads(self.rfile.read(content_length)) 
        if 'action' in post_data:
            if post_data['action'] == 'register':
                if 'name' not in post_data:
                    response = json.dumps({'status':'error', 'message':'name field must be defined for a registration message.'})
                else:
                    res, message = self.game.register_player(post_data['name'])
                    if res:
                        response = json.dumps({'status':'ok','id':message})
                    else:
                        response = json.dumps({'status':'error','message':message})
            elif post_data['action'] == 'get_status':
                if 'id' not in post_data:
                    response = json.dumps({'status':'error', 'message':'id field must be defined for a get status message.'})
                else:
                    res, results = self.game.read_messages(post_data['id'])
                    if res:
                        response = json.dumps({'status':'ok','message':results})
                    else:
                        response = json.dumps({'status':'error','message':results})
            elif post_data['action'] == 'submit_card':
                if 'id' not in post_data or 'card' not in post_data:
                    response = json.dumps({'status':'error', 'message':'id and card fields must be defined for a choose_card message.'})
                else:
                    res, message = self.game.submit_card(post_data['id'], post_data['card'])
                    if res:
                        response = json.dumps({'status':'ok','message': message})
                    else:
                        response = json.dumps({'status':'error','message': message})
            elif post_data['action'] == 'judge_card':
                if 'id' not in post_data or 'card' not in post_data:
                    response = json.dumps({'status':'error','message':'id and card fields must be defined for a judge message.'})
                else:
                    res, message = self.game.judge_card(post_data['id'], post_data['card'])
                    if res:
                        response = json.dumps({'status':'ok','message': message})
                    else:
                        response = json.dumps({'status':'error','message': message})
            else:
                response = json.dumps({'status':'error', message:"bad action field value '" + post_data['action'] + "'"})  
        else:
            response = json.dumps({'status':'error', message:'message must contain an action field.'})
        return response
            
    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)
        
    def log_message(self, format, *args):
        if self.VERBOSE:
            super.log_message(format, *args)
