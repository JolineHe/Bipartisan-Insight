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
