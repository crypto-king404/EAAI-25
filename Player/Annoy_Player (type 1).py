from annoy import AnnoyIndex
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from Player import Player

class AnnoyPlayer(Player):

    PLAYER_NAME = "Annoying Player"

    def __init__(self, adjectives_path, nouns_path):
        super().__init__(self.PLAYER_NAME)
        self.adjectives = self.load_words(adjectives_path)
        self.nouns = self.load_words(nouns_path)
        self.vectorizer = TfidfVectorizer(ngram_range=(3))
        self.fit_vectorizer()
        self.build_annoy_index()

    def load_words(self, path):
        with open(path, 'r') as file:
            words = file.read().splitlines()
        return words

    def fit_vectorizer(self):
        all_words = self.adjectives + self.nouns
        self.vectorizer.fit(all_words)
        self.embeddings = self.vectorizer.transform(all_words).toarray()
        self.vector_size = self.embeddings.shape[1]

    def build_annoy_index(self):
        self.annoy_index = AnnoyIndex(self.vector_size, 'angular')
        for i, embedding in enumerate(self.embeddings):
            self.annoy_index.add_item(i, embedding)
        self.annoy_index.build(10)  # Build 10 trees

    def get_embedding(self, word):
        return self.vectorizer.transform([word]).toarray()[0]

    def choose_card(self, target, hand):
        target_embedding = self.get_embedding(target)
        bestCardNdx = 0
        bestSimilarity = -1

        for i, card in enumerate(hand):
            card_embedding = self.get_embedding(card)
            similarity = np.dot(target_embedding, card_embedding) / (np.linalg.norm(target_embedding) * np.linalg.norm(card_embedding))
            if similarity > bestSimilarity:
                bestSimilarity = similarity
                bestCardNdx = i

        return bestCardNdx

    def judge_card(self, target, player_cards):
        target_embedding = self.get_embedding(target)
        bestCard = player_cards[0]
        bestSimilarity = -1

        for card in player_cards:
            card_embedding = self.get_embedding(card)
            similarity = np.dot(target_embedding, card_embedding) / (np.linalg.norm(target_embedding) * np.linalg.norm(card_embedding))
            if similarity > bestSimilarity:
                bestSimilarity = similarity
                bestCard = card

        return bestCard

if __name__ == '__main__':
    adjectives_path = "adjectives.txt"
    nouns_path = "nouns.txt"
    player = AnnoyPlayer(adjectives_path, nouns_path)
    player.run()
