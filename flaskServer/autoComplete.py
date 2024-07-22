import json
import os
import warnings
import tensorflow as tf
from tensorflow.keras.preprocessing.text import tokenizer_from_json  #type: ignore 
from tensorflow.keras.preprocessing.sequence import pad_sequences #type: ignore 
from tensorflow.keras.models import load_model #type: ignore 
import numpy as np


class NextWord:
    def __init__(self):
        
        tokenizer_config_path = r'C:\programs\projects\NLP powered chatapp\web\chatapp\flaskServer\nextWord\tokenizer_config.json'
        word_index_path = r'C:\programs\projects\NLP powered chatapp\web\chatapp\flaskServer\nextWord\word_index.json'
        model_path = r'C:\programs\projects\NLP powered chatapp\web\chatapp\flaskServer\nextWord\my_model.h5'
        
        with open(tokenizer_config_path) as f:
            tokenizer_config = json.load(f)
            
        with open(word_index_path) as f:
            word_index = json.load(f)

        self.tokenizer = tokenizer_from_json(tokenizer_config)
        self.tokenizer.word_index = word_index

        self.model = load_model(model_path)
        self.input_length = 150
    
    def nextWords(self, text, top_k=3):

        token_text = self.tokenizer.texts_to_sequences([text])[0]
        
        padded_token_text = pad_sequences([token_text], maxlen=self.input_length, padding='pre')
        
        prediction = self.model.predict(padded_token_text)
        
        top_indices = np.argsort(prediction[0])[-top_k:][::-1]
        
        words = [self.tokenizer.index_word.get(index) for index in top_indices if self.tokenizer.index_word.get(index)]
        
        return words
                
