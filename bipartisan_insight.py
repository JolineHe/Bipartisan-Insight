import schedule
import time
import logging
from config_manager import ConfigManager
from data_acquisition import DemocratNewsCrawler, RepublicanNewsCrawler
from ai_analysis import AINewsAnalyzer
from report_generation import ReportGenerator
from email_notification import EmailNotifier
from report_viewer import ReportViewerUI

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
        self.analyzer = AINewsAnalyzer(config_manager)
        self.email_notifier = EmailNotifier(config_manager)
        
        # 为两个党派创建独立的报告生成器对象
        self.democrat_report_gen = ReportGenerator(config_manager, "democrat")
        self.republican_report_gen = ReportGenerator(config_manager, "republican")
        logging.info("BipartisanInsight initialized successfully.")

    def job(self, party):
        logging.info(f"Starting {party.capitalize()} data acquisition job.")
        try:
            if party == "democrat":
                news = self.democrat_crawler.fetch_news()
                report_gen = self.democrat_report_gen
            else:
                news = self.republican_crawler.fetch_news()
                report_gen = self.republican_report_gen

            if not news:
                logging.info(f"No news available for {party.capitalize()} today.")
                return f"No news available for {party.capitalize()} today."

            # 生成报告
            report_file = report_gen.generate(news)
            logging.info(f"Report generated for {party.capitalize()}: {report_file}")

            # 发送报告邮件
            email_result = self.email_notifier.send(report_file)
            if email_result:
                logging.error(f"Error in sending email: {email_result}")
            else:
                logging.info(f"Email sent successfully for {party.capitalize()}.")

            return f"{party.capitalize()} report generated and emailed."

        except Exception as e:
            logging.error(f"Error during job execution for {party.capitalize()}: {e}")
            return f"Error during job execution for {party.capitalize()}: {e}"

if __name__ == "__main__":
    logging.info("Starting Bipartisan Insight service.")
    bipartisan_insight = BipartisanInsight()

    # 从配置文件获取定时任务执行时间
    schedule_time = config_manager.get_schedule_time()
    logging.info(f"Scheduled job will run at {schedule_time}.")

    # 立即执行定时任务
    #bipartisan_insight.job("democrat")
    #bipartisan_insight.job("republican")

    # 每天执行一次定时任务
    #schedule.every().day.at(schedule_time).do(bipartisan_insight.job, "democrat")
    #schedule.every().day.at(schedule_time).do(bipartisan_insight.job, "republican")

    # 启动报告浏览 UI
    report_viewer_ui = ReportViewerUI(bipartisan_insight)
    report_viewer_ui.launch()

    # 保持定时任务的运行
    while True:
        schedule.run_pending()  # 检查并运行定时任务
        time.sleep(60)  # 每分钟检查一次定时任务
