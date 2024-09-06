import json
import os

class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self):
        """加载配置文件"""
        if not os.path.exists(self.config_file):
            # 如果配置文件不存在，返回默认配置
            return {
                "schedule_time": "10:00",  # 默认定时任务时间
                "urls": {
                    "democrat": "https://democrats.org/news/page/{}/",
                    "republican": "https://gop.com/press-releases/?page={}"
                }
            }
        with open(self.config_file, 'r') as f:
            return json.load(f)

    def get_schedule_time(self):
        """获取定时任务的执行时间"""
        return self.config.get("schedule_time", "10:00")

    def get_party_url(self, party):
        """获取指定党派的新闻 URL 模板"""
        return self.config["urls"].get(party)

    def set_schedule_time(self, time_str):
        """设置定时任务的执行时间并保存配置"""
        self.config["schedule_time"] = time_str
        self._save_config()

    def _save_config(self):
        """保存配置文件"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
