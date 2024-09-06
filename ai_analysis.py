import openai
import os

class AINewsAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def analyze(self, news_file):
        with open(news_file, "r") as f:
            news_content = f.read()

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Analyze the following political news and identify key topics and positions:\n\n{news_content}",
            max_tokens=500
        )
        
        analysis_result = response['choices'][0]['text']
        return analysis_result
