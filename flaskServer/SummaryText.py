from transformers import pipeline

class Summary:
    _instance = None

    def __new__(cls, model_name="facebook/bart-large-cnn"):
        if cls._instance is None:
            cls._instance = super(Summary, cls).__new__(cls)
            cls._instance.summarizer = pipeline("summarization", model=model_name)
        return cls._instance

    def get_summary(self, messages):
        string_to_sum = ' '.join(mes['content'] for mes in messages)

        if len(string_to_sum) < 50:
            return string_to_sum  # Return the original text if it's too short to summarize

        max_len = 40

        try:
            summary = self.summarizer(string_to_sum, max_length=max_len, min_length=10, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            print(f"An error occurred during summarization: {e}")
            return string_to_sum 