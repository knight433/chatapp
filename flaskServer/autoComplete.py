import json
import tensorflow as tf
from tensorflow.keras.preprocessing.text import tokenizer_from_json #type: ignore 
from tensorflow.keras.preprocessing.sequence import pad_sequences #type: ignore 
from tensorflow.keras.models import load_model #type: ignore 
import numpy as np

class NextWord:
    def __init__(self):
        
        tokenizer_config_path = r'C:\programs\projects\NLP powered chatapp\web\chatapp\flaskServer\nextWord\tokenizer_config.json'
        word_index_path = r'C:\programs\projects\NLP powered chatapp\web\chatapp\flaskServer\nextWord\word_index.json'
        model_path = r'C:\programs\projects\NLP powered chatapp\web\chatapp\flaskServer\nextWord\my_model.h5'
        
        # Load tokenizer configuration
        with open(tokenizer_config_path) as f:
            tokenizer_config = json.load(f)
            
        # Load word index
        with open(word_index_path) as f:
            word_index = json.load(f)

        # Reconstruct the tokenizer
        self.tokenizer = tokenizer_from_json(tokenizer_config)
        self.tokenizer.word_index = word_index

        # Load the model
        self.model = load_model(model_path)
        self.input_length = 150
    
    def nextWord(self, text, words=3):
        for i in range(words):
            # Tokenize the current text
            token_text = self.tokenizer.texts_to_sequences([text])[0]
            
            # Padding the sequence to the length expected by the model
            padded_token_text = pad_sequences([token_text], maxlen=self.input_length, padding='pre')
            
            # Predict the next word
            prediction = self.model.predict(padded_token_text)
            
            # Get the index of the predicted word
            pos = np.argmax(prediction)
            
            # Find the word corresponding to the predicted index
            word = self.tokenizer.index_word.get(pos)
            if word:
                text = text + " " + word
                print(text)
            else:
                print("Predicted index not found in tokenizer")
                break


