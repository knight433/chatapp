from transformers import pipeline
import re

# text = "Yess, We will show future plan ki ye phone pe rahega, Nd google maps ke saath it will be linked, Toh like if someone has their destination passing thru that avalanche area ..so they will get notified" 

# print(summarizer(text, max_length=120, min_length=5, do_sample=False))

class Summary:
    def __init__(self, model_name="facebook/bart-large-cnn") -> None:
        self.summarizer = pipeline("summarization", model=model_name)

    def get_summary(self, messages):
        string_to_sum = ' '.join(mes['content'] for mes in messages)

        if len(string_to_sum) < 50:
            return string_to_sum  # Return the original text if it's too short to summarize

        max_len = 36

        try:
            summary = self.summarizer(string_to_sum, max_length=max_len, min_length=10, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            print(f"An error occurred during summarization: {e}")
            return string_to_sum 

# # Example usage
# messages = [
#     {"user": "Alice", "content": "I had a great day at the park."},
#     {"user": "Bob", "content": "The weather was fantastic, and we had a picnic."},
#     {"user": "Alice", "content": "We played games and enjoyed the sun."},
#     {"user": "Bob", "content": "Overall, it was a wonderful experience."}
# ]

# summarizer = Summary()
# summary_text = summarizer.get_summary(messages)
# print(summary_text)

class EmotionClassifier:
    def __init__(self) -> None:
        self.pipe = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions")

    def preprocess(self, text):
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'[^A-Za-z0-9\s.,!?]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text    

    def emoWhat(self,text):
        text = text[0]['content']
        processed_text = self.preprocess(text)
        res = self.pipe(processed_text)

        return res[0]['label']
        
