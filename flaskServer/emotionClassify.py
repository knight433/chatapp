from transformers import pipeline
import re

class EmotionClassifier:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmotionClassifier, cls).__new__(cls)
            cls._instance.pipe = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions")
        return cls._instance

    def preprocess(self, text):
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'[^A-Za-z0-9\s.,!?]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text    

    def emoWhat(self, text):
        text = text[0]['content']
        processed_text = self.preprocess(text)
        res = self.pipe(processed_text)
        return res[0]['label']