import re
from tqdm import tqdm
from nltk.corpus import stopwords
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import hashing_trick
from keras import backend as K

class NeuralNetwork:
    def __init__(self, model_path):
        """Initiates properties and loads the Neural network module"""
        try:
            K.clear_session()
            self.vocab_size = 200000
            self.max_length = 150
            self.vector_dim = 200
            self.model = load_model(model_path)
            self.model_summary = self.model.summary()
        except:
            print('Error: Failed to load Neural Network Model')

    def remove_at(self, text):
        """Removes @address from text"""
        return re.sub('(@\w+)','', text)

    def remove_link(self, text):
        """Removes all links from text"""
        return re.sub('\w+://\S+', '', text)

    def remove_stopwords(self, text):
        """Removes stopwords from text"""
        words = set(stopwords.words('english'))
        big_regex = re.compile('\s+|\s+'.join(map(re.escape, words)))
        return big_regex.sub(' ', text)

    def predict(self, data):
        """Predicts the sentiment of given data. The input must be of iterable type"""
        data = [self.remove_stopwords(text) for text in tqdm(data)]
        data = [self.remove_at(text) for text in tqdm(data)]
        data = [self.remove_link(text) for text in tqdm(data)]
        encoded_docs = [hashing_trick(d, self.vocab_size, hash_function = 'md5') for d in tqdm(data)]
        padded_docs = pad_sequences(encoded_docs, maxlen = self.max_length, padding = 'post')
        return self.model.predict(padded_docs)

if __name__ == '__main__':
    neural_model = NeuralNetwork('nn_model.h5')
    print(neural_model.predict(["Negative people, negative mind",
                      "Tuesday Thoughts We must fight the negative The only way we are going to change the world is with #love #kindness and #LISTENING",
                      "Despite obtaining an A, he was sad",
                      "My heart melts for Syria",
                      "Hurray! Our team won",
                      "I'm so proud of our Country!",
                      "This might not work out",
                      "Am I supposed to feel sad?"]))
