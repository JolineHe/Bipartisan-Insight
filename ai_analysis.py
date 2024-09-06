import os
import logging
from openai import OpenAI
from config_manager import ConfigManager

class AINewsAnalyzer:
    def __init__(self, config_manager):
        self.model = config_manager.config.get("openai_model", "gpt-4")
        self.client = OpenAI()
        logging.info(f"AINewsAnalyzer initialized with model: {self.model}")

    def analyse_news(self, prompt, content):
        """调用 OpenAI Chat API 进行新闻内容分析"""
        try:
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ]
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            analysis = completion.choices[0].message.content
            logging.info("AI analysis completed successfully.")
            return analysis
        except Exception as e:
            logging.error(f"Error in AI analysis: {e}")
            return f"Error in AI analysis: {e}"

# 用于测试的 __init__ 方法
if __name__ == "__main__":
    # 实例化 ConfigManager 并获取 OpenAI 配置信息
    from config_manager import ConfigManager
    config_manager = ConfigManager()

    # 实例化 AINewsAnalyzer
    analyser = AINewsAnalyzer(config_manager)

    # 读取位于 /prompt/openai_prompt.txt 的 prompt
    with open("prompt/openai_prompt.txt", 'r') as f:
        prompt = f.read().strip()

    # 获取 /data/news/democrat 文件夹下的所有 Markdown 文件路径
    news_dir = "data/news/democrat"
    news_files = [os.path.join(news_dir, file) for file in os.listdir(news_dir) if file.endswith('.md')]

    # 处理每个文件的内容并调用 analyse_news
    for news_file in news_files:
        with open(news_file, 'r') as f:
            content = f.read().strip()
            analysis_result = analyser.analyse_news(prompt, content)
            print(f"Analysis for {news_file}:\n{analysis_result}\n")
