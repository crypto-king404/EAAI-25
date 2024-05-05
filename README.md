# EAAI25

This repository houses an evaluation system and sample bots for the EAAI 25 Undergraduate Research Challenge.

The evaluation system uses a simple web server.  Player bots communicate with the server to choose cards to play,
judge cards selected by other players, and process round completion messages.  There is a web interface that is 
available to run games.

## Running a game

To run the evalution system, you should do the following:

1) Run the web server, by typing the following command in the Server directory:

  python driver.py

2) Use a web browser to open the URL: http://localhost:8000/

3) Launch at least 3 players bots.  There are three sample player bots in the Player directory.  You can launch them by running the following commands:

  python EditDistancePlayer.py

  python RandomPlayer.py

  python Word2VecPlayer.py
  
4) You can play a game once the three players have been launched and assigned id's (Note that the Word2VecPlayer takes a bit of time to initialize).  The game is played a round at a time, by clicking the "Play round" button.  You can manually step through the three phases of the game, if you would like by unchecking the checkbox in the admin webpage.  When a game completes, you need to restart the game and relaunch the player bots.

## Developing your own bots

To develop a bot, you need to subclass the Player class, and do the following:

1) Give you player a name by setting the PLAYER_NAME field.

2) Override the choose_card method.  This method takes as arguments the target adjective and a hand array,
   containing possible nouns.  Your method should return the index of the card chosen from the hand array.
   Note that if you do not choose a card in time, the system will choose a random card for you.

3) Override the judge_card method.  This method takes as arguments the target adjective and a player_cards
   array, containing the nouns chosen by the players.  Your bot should return a string chosen from the
   player_cards array that it judges to be the best of the submissions.
    
4) Optional: Override the process results method.  This method receives the results from the previous round
   including which card was provided by each player and whose card was chosen.

The sample Players provide three examples of simple (and not very good) ways to play the game.  As you 
develop your bot(s), you will likely want to replace all of these bots to achieve high quality game play.



