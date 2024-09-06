#!/bin/bash

# 创建项目目录结构
mkdir -p bipartisan_insight/data/news
mkdir -p bipartisan_insight/data/reports

# 创建 Python 文件
touch bipartisan_insight/bipartisan_insight.py
touch bipartisan_insight/data_acquisition.py
touch bipartisan_insight/ai_analysis.py
touch bipartisan_insight/report_generation.py
touch bipartisan_insight/email_notification.py
touch bipartisan_insight/report_viewer.py
touch bipartisan_insight/config.json

# 创建 requirements.txt
echo "Creating requirements.txt..."
cat <<EOL > bipartisan_insight/requirements.txt
requests
beautifulsoup4
openai
schedule
smtplib
gradio
EOL

# 编写各个 Python 文件的内容

echo "Writing bipartisan_insight.py..."
cat <<EOL > bipartisan_insight/bipartisan_insight.py
import schedule
import time
import json
from datetime import datetime
from data_acquisition import DemocratNewsCrawler, RepublicanNewsCrawler
from ai_analysis import AINewsAnalyzer
from report_generation import ReportGenerator
from email_notification import EmailNotifier
from report_viewer import GradioViewer

CONFIG_FILE = 'config.json'

class BipartisanInsight:
    def __init__(self):
        self.democrat_crawler = DemocratNewsCrawler()
        self.republican_crawler = RepublicanNewsCrawler()
        self.analyzer = AINewsAnalyzer()
        self.report_gen = ReportGenerator()
        self.email_notifier = EmailNotifier()
        self._load_config()

    def _load_config(self):
        """加载配置文件"""
        if not os.path.exists(CONFIG_FILE):
            self.config = {"last_run": None}
            self._save_config()
        else:
            with open(CONFIG_FILE, "r") as f:
                self.config = json.load(f)

    def _save_config(self):
        """保存配置文件"""
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f)

    def job(self):
        print("Starting data acquisition...")

        # 只获取当天新闻
        democrat_news = self.democrat_crawler.fetch_news()
        republican_news = self.republican_crawler.fetch_news()

        # 如果有新闻，进行分析并生成报告
        if democrat_news or republican_news:
            print("Starting AI analysis...")
            analysis_result = self.analyzer.analyze(democrat_news + republican_news)
        
            print("Generating report...")
            report_file = self.report_gen.generate(analysis_result)

            print(f"Sending report {report_file} via email...")
            self.email_notifier.send(report_file)

        # 更新最后执行时间
        self.config["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_config()

def run_gradio_viewer():
    viewer = GradioViewer()
    viewer.launch()

if __name__ == "__main__":
    bipartisan_insight = BipartisanInsight()

    # 每天执行一次定时任务
    schedule.every().day.at("10:00").do(bipartisan_insight.job)

    # 启动 Gradio 服务来浏览报告
    run_gradio_viewer()

    print("Starting Bipartisan Insight service...")

    while True:
        schedule.run_pending()  # 检查并运行定时任务
        time.sleep(60)  # 每分钟检查一次定时任务
EOL

echo "Writing data_acquisition.py..."
cat <<EOL > bipartisan_insight/data_acquisition.py
import requests
from bs4 import BeautifulSoup
import os
import datetime

class NewsCrawlerBase:
    def __init__(self):
        self.news_dir = "data/news/"
        os.makedirs(self.news_dir, exist_ok=True)
        self.today_str = datetime.date.today().strftime("%Y-%m-%d")

    def fetch_news(self):
        """子类实现特定网站的新闻抓取"""
        raise NotImplementedError("Subclasses must implement this method")

    def _save_news_to_md(self, title, content):
        """将新闻保存为 Markdown 文件，文件名格式为 日期_新闻稿标题.md"""
        file_name = f"{self.news_dir}{self.today_str}_{title.replace(' ', '_')}.md"
        with open(file_name, "w") as f:
            f.write(f"# {title}\n\n")
            f.write(content)
        print(f"Saved: {file_name}")
        return file_name

class DemocratNewsCrawler(NewsCrawlerBase):
    def __init__(self):
        super().__init__()
        self.url_template = 'https://democrats.org/news/page/{}/'

    def fetch_news(self):
        print("Fetching Democrat news...")
        page = 1
        news_list = []
        while True:
            url = self.url_template.format(page)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            articles = soup.find_all('article')  # 根据页面结构调整
            if not articles:
                break

            for article in articles:
                news_date_str = article.find('time').get('datetime')[:10]  # 假设获取到的是 'YYYY-MM-DD'
                if news_date_str == self.today_str:
                    news_title = article.find('a').text.strip()
                    news_link = article.find('a')['href']
                    news_content = self._fetch_full_news(news_link)
                    news_file = self._save_news_to_md(news_title, news_content)
                    news_list.append(news_file)
                else:
                    return news_list

            page += 1
        return news_list

    def _fetch_full_news(self, news_link):
        """抓取新闻全文"""
        response = requests.get(news_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_content = soup.find('div', class_='news-content').text.strip()
        return news_content

class RepublicanNewsCrawler(NewsCrawlerBase):
    def __init__(self):
        super().__init__()
        self.url_template = 'https://gop.com/press-releases/?page={}'

    def fetch_news(self):
        print("Fetching Republican news...")
        page = 1
        news_list = []
        while True:
            url = self.url_template.format(page)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            articles = soup.find_all('article')  # 根据页面结构调整
            if not articles:
                break

            for article in articles:
                news_date_str = article.find('time').get('datetime')[:10]  # 假设获取到的是 'YYYY-MM-DD'
                if news_date_str == self.today_str:
                    news_title = article.find('a').text.strip()
                    news_link = article.find('a')['href']
                    news_content = self._fetch_full_news(news_link)
                    news_file = self._save_news_to_md(news_title, news_content)
                    news_list.append(news_file)
                else:
                    return news_list

            page += 1
        return news_list

    def _fetch_full_news(self, news_link):
        """抓取新闻全文"""
        response = requests.get(news_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_content = soup.find('div', class_='news-content').text.strip()
        return news_content
EOL

echo "Writing ai_analysis.py..."
cat <<EOL > bipartisan_insight/ai_analysis.py
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
EOL

echo "Writing report_generation.py..."
cat <<EOL > bipartisan_insight/report_generation.py
import os
import datetime

class ReportGenerator:
    def __init__(self):
        pass

    def generate(self, analysis_result):
        today = datetime.date.today().strftime("%Y-%m-%d")
        report_file = f"data/reports/{today}_report.md"
        
        with open(report_file, "w") as f:
            f.write(f"# Daily Political Analysis Report ({today})\n\n")
            f.write(analysis_result)
        
        return report_file
EOL

echo "Writing email_notification.py..."
cat <<EOL > bipartisan_insight/email_notification.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

class EmailNotifier:
    def __init__(self):
        self.sender = 'your_email@example.com'
        self.recipient = 'recipient@example.com'
        self.smtp_server = 'smtp.example.com'
        self.password = 'your_password'

    def send(self, report_file):
        subject = "Daily Political Analysis Report"
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.recipient
        msg['Subject'] = subject

        with open(report_file, 'r') as f:
            report_content = f.read()

        msg.attach(MIMEText(report_content, 'plain'))
        
        with smtplib.SMTP(self.smtp_server, 587) as server:
            server.starttls()
           
