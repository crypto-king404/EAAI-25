
#Thought 1: Checking text similarity using WordNet
# import nltk
# from nltk.corpus import wordnet

# # Get the sets of synonyms that include the target words
# syns1 = wordnet.synsets("friend")
# syns2 = wordnet.synsets("enemy")

# # Get the highest similarity value among all pairs of synonyms
# max_sim = max(word1.wup_similarity(word2) or 0 for word1 in syns1 for word2 in syns2)

# print(max_sim)


# Thought 2: Checking text similarity using Chroma DB and Langchain
# from langchain.embeddings import MagnitudeEmbeddings
# from langchain.vectorstores import ChromaStore

# # Connect to Chroma DB
# store = ChromaStore(host="localhost", port=8500)

# # Load GoogleNews vectors
# embeddings = MagnitudeEmbeddings.from_file("GoogleNews-vectors-negative300.bin")

# # Target word
# target_word = "happy"

# # Generate random words (replace with your random word generation method)
# random_words = ["sad", "joyful", "angry", "confused"]

# # Get embeddings
# target_embedding = embeddings.get_embedding(target_word)
# random_embeddings = [embeddings.get_embedding(word) for word in random_words]

# # Calculate cosine similarities
# similarities = [embeddings.cosine_similarity(target_embedding, embedding) for embedding in random_embeddings]

# # Find most similar word (index corresponds to random_words list)
# most_similar_index = similarities.index(max(similarities))
# most_similar_word = random_words[most_similar_index]

# print(f"Most similar word to '{target_word}': {most_similar_word}")


# Thought 3: Checking text similarity using spaCy and Hugging Face Transformers
import spacy
import numpy as np
import random
from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity
from Player import Player

class Space_Player(Player):

    PLAYER_NAME = "Space Player"

    def __init__(self):
        super().__init__(self.PLAYER_NAME)
        self.nlp = spacy.load("en_core_web_lg")
        self.sentiment_analysis = pipeline("sentiment-analysis")


    def choose_card(self,target, hand):
        target_word = target
        random_words = hand

        target_embedding = self.nlp(target_word).vector
        random_embeddings = [self.nlp(word).vector for word in random_words]

        similarities = [cosine_similarity(target_embedding, embedding) for embedding in random_embeddings]

        most_similar_index = similarities.index(max(similarities))
        most_similar_word = random_words[most_similar_index]

        humor_scores = [self.sentiment_analysis(word)[0]['score'] for word in random_words] 

        most_humorous_index = humor_scores.index(max(humor_scores))
        most_humorous_word = random_words[most_humorous_index]

        if similarities[most_similar_index]< 0.5: # if the most similar word has a similarity score of less than 0.5 then, it will pick the most humorous word
            return most_humorous_word
        return most_similar_word
    
    def judge_card(self, target, player_cards):
        return self.choose_card(target, player_cards)
    
    def process_results(self, result):
        print("Result", result)

if __name__ == '__main__':
    player = Space_Player()
    player.run()



# target_embedding = self.nlp(target_word).vector
# random_embeddings = [self.nlp(word).vector for word in random_words]

# similarities = [cosine_similarity(target_embedding, embedding) for embedding in random_embeddings]

# most_similar_index = similarities.index(max(similarities))
# most_similar_word = random_words[most_similar_index]

# humor_scores = [self.sentiment_analysis(word)[0]['score'] for word in random_words] 

# most_humorous_index = humor_scores.index(max(humor_scores))
# most_humorous_word = random_words[most_humorous_index]

# if similarities[most_similar_index]< 0.5: # if the most similar word has a similarity score of less than 0.5 then, it will pick the most humorous word
#     print(f"Most humorous word: {most_humorous_word}")
# print(f"Most similar word to '{target_word}': {most_similar_word}")
# print(random_words)

# def get_random_words(vocab, num_words=5):
#     words = [word for word in vocab if word.is_alpha and not word.is_stop and word.has_vector]
#     random_words = random.sample(words, num_words)
#     return [word.text for word in random_words]

# random_words = get_random_words(nlp.vocab, 6)

# target_word = "friend"


# random_words = ["enemy", "acquaintance", "companion", "ally"]
