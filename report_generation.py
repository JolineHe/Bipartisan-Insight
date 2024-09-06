# Description: 生成报告的主要逻辑
import os
import logging
from datetime import datetime
from ai_analysis import AINewsAnalyzer

class ReportGenerator:
    def __init__(self, config_manager, party):
        self.analyzer = AINewsAnalyzer(config_manager)
        self.party = party  # 存储党派信息
        self.report_dir = f"data/reports/{self.party}"
        os.makedirs(self.report_dir, exist_ok=True)  # 创建党派对应的报告目录

    def generate(self, news_files):
        """读取所有新闻文件，调用 AI 分析，综合生成报告"""
        report_content = ""
        today_str = datetime.today().strftime('%Y-%m-%d')

        # 读取 prompt 内容
        try:
            with open("prompt/openai_prompt.txt", 'r') as f:
                prompt = f.read().strip()
                logging.info("Prompt loaded successfully from /prompt/openai_prompt.txt")
        except Exception as e:
            logging.error(f"Error reading prompt file: {e}")
            return f"Error reading prompt file: {e}"

        # 综合处理每个新闻文件
        combined_content = ""
        for news_file in news_files:
            try:
                with open(news_file, 'r') as f:
                    content = f.read()
                    logging.info(f"Reading content from {news_file}")
                    
                combined_content += f"\n\n### {os.path.basename(news_file)}\n\n{content}\n"
            except Exception as e:
                logging.error(f"Error processing {news_file}: {e}")
                combined_content += f"Error processing {news_file}: {e}\n"

        # 调用 AI 分析整个综合内容
        try:
            analysis = self.analyzer.analyse_news(prompt, combined_content)
            report_content += f"### AI Analysis Report for {today_str}\n\n"
            report_content += analysis
        except Exception as e:
            logging.error(f"Error during AI analysis: {e}")
            return f"Error during AI analysis: {e}"

        # 保存生成的报告
        report_file = os.path.join(self.report_dir, f"{today_str}.md")
        try:
            with open(report_file, 'w') as f:
                f.write(report_content)
            logging.info(f"Report generated and saved to {report_file}")
        except Exception as e:
            logging.error(f"Error saving report: {e}")
            return f"Error saving report: {e}"

        return report_file




if __name__ == "__main__":
    # 实例化 ConfigManager 并获取 OpenAI 配置信息
    from config_manager import ConfigManager
    config_manager = ConfigManager()

    # 获取 /data/news/democrat 文件夹下的所有 Markdown 文件路径
    news_dir = "data/news/democrat"
    news_files = [os.path.join(news_dir, file) for file in os.listdir(news_dir) if file.endswith('.md')]

    # 实例化 ReportGenerator 并生成报告
    report_generator = ReportGenerator(config_manager, party="democrat")
    report_file = report_generator.generate(news_files)
    print(f"Report generated: {report_file}")
