import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from config_manager import ConfigManager
import os
import markdown2


class EmailNotifier:
    def __init__(self, config_manager):
        # 从 config.json 获取邮件发送相关的配置
        email_config = config_manager.config.get("email", {})
        self.smtp_server = email_config.get("smtp_server", "")
        self.smtp_port = email_config.get("smtp_port", 587)
        self.sender_email = email_config.get("sender_email", "")
        self.sender_password = os.getenv("SENDER_EMAIL_PASSWORD")  # 从环境变量中获取密码
        self.recipient_email = email_config.get("recipient_email", "")
        logging.info(f"EmailNotifier initialized with SMTP server: {self.smtp_server}")

    def send(self, report_file):
        """发送带有报告的邮件"""
        # 创建邮件
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.recipient_email
        message["Subject"] = "Daily Report"

        # 邮件正文
        with open(report_file, "r") as f:
            report_content = f.read()

        # 将Markdown内容转换为HTML
        html_report = markdown2.markdown(report_content)

        message.attach(MIMEText(html_report, 'html'))
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                logging.debug("登录SMTP服务器")
                server.login(message['From'], self.sender_password)
                server.sendmail(message['From'], message['To'], message.as_string())
                logging.info("邮件发送成功！")
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            return f"Error sending email: {e}"




# 测试邮件发送
if __name__ == "__main__":
    # 实例化 ConfigManager 并获取配置
    config_manager = ConfigManager()

    # 实例化 EmailNotifier
    email_notifier = EmailNotifier(config_manager)

    # 测试发送报告邮件
    test_report = "data/reports/test_report.md"  # 假设有一个测试报告
    result = email_notifier.send(test_report)
    if result:
        print(result)
    else:
        print("Email sent successfully.")
