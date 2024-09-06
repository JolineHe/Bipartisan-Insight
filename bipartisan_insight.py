import schedule
import time
import logging
from config_manager import ConfigManager
from data_acquisition import DemocratNewsCrawler, RepublicanNewsCrawler
from ai_analysis import AINewsAnalyzer
from report_generation import ReportGenerator
from email_notification import EmailNotifier
from report_viewer import GradioViewer

# 初始化日志配置
logging.basicConfig(
    filename='project.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 加载配置文件
config_manager = ConfigManager()

class BipartisanInsight:
    def __init__(self):
        self.democrat_crawler = DemocratNewsCrawler(config_manager)
        self.republican_crawler = RepublicanNewsCrawler(config_manager)
        self.analyzer = AINewsAnalyzer()
        self.report_gen = ReportGenerator()
        self.email_notifier = EmailNotifier()
        logging.info("BipartisanInsight initialized successfully.")

    def job(self):
        logging.info("Starting data acquisition job.")
        try:
            # 只获取当天新闻
            democrat_news = self.democrat_crawler.fetch_news()
            republican_news = self.republican_crawler.fetch_news()

            # 如果有新闻，进行分析并生成报告
            if democrat_news or republican_news:
                logging.info("Starting AI analysis.")
                analysis_result = self.analyzer.analyze(democrat_news + republican_news)
        
                logging.info("Generating report.")
                report_file = self.report_gen.generate(analysis_result)

                logging.info(f"Sending report {report_file} via email.")
                self.email_notifier.send(report_file)

        except Exception as e:
            logging.error(f"Error during job execution: {e}")

def run_gradio_viewer():
    viewer = GradioViewer()
    viewer.launch()

if __name__ == "__main__":
    logging.info("Starting Bipartisan Insight service.")
    bipartisan_insight = BipartisanInsight()

    # 获取定时任务执行时间
    schedule_time = config_manager.get_schedule_time()
    logging.info(f"Scheduled job will run at {schedule_time}.")
    
    # 每天执行一次定时任务
    schedule.every().day.at(schedule_time).do(bipartisan_insight.job)

    # 启动 Gradio 服务来浏览报告
    run_gradio_viewer()

    while True:
        schedule.run_pending()  # 检查并运行定时任务
        time.sleep(60)  # 每分钟检查一次定时任务
