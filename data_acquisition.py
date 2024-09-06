import requests
from bs4 import BeautifulSoup
import os
import datetime
from newspaper import Article
import time
import random
import logging
from config_manager import ConfigManager

class NewsCrawlerBase:
    def __init__(self, config_manager, party):
        self.news_dir = f"data/news/{party}"
        os.makedirs(self.news_dir, exist_ok=True)
        self.today_str = datetime.date.today().strftime("%Y-%m-%d")
        self.url_template = config_manager.get_party_url(party)
        logging.info(f"Initialized {party} news crawler with directory: {self.news_dir}")

    def fetch_news(self):
        """子类实现特定网站的新闻抓取"""
        raise NotImplementedError("Subclasses must implement this method")

    def _save_news_to_md(self, title, content):
        """将新闻保存为 Markdown 文件，并返回文件路径，文件名格式为 日期_新闻稿标题.md"""
        file_name = f"{self.news_dir}/{self.today_str}_{title.replace(' ', '_')}.md"
        with open(file_name, "w") as f:
            f.write(f"# {title}\n\n")
            f.write(content)
        logging.info(f"Saved news to {file_name}")
        return file_name  # 返回生成的 Markdown 文件路径

class DemocratNewsCrawler(NewsCrawlerBase):
    def __init__(self, config_manager):
        super().__init__(config_manager, "democrat")

    def fetch_news(self):
        print("Fetching Democrat news...")
        page = 1
        news_list = []
        saved_files = []  # 存储生成的 md 文件路径
        while True:
            url = self.url_template.format(page)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # 查找所有 class 为 "posts-list__item" 的 <li> 标签
            articles = soup.find_all('li', class_='posts-list__item')
            if not articles:
                break

            for article in articles:
                # 查找 class 为 "posts-list__data" 的 <span> 标签，获取发布日期
                date_tag = article.find('span', class_='posts-list__date')
                if date_tag:
                    news_date_str = date_tag.text.strip()
                    # 日期格式为 mm/dd/yyyy，转换为 yyyy-mm-dd
                    news_date = datetime.datetime.strptime(news_date_str, "%m/%d/%Y").strftime("%Y-%m-%d")

                    # 检查新闻日期是否为今天
                    if news_date == self.today_str:
                        # 获取新闻链接
                        link_tag = article.find('a')
                        if link_tag and 'href' in link_tag.attrs:
                            news_link = link_tag['href']
                            news_list.append(news_link)

            # 如果当天没有新闻，说明已经获取完当天的所有新闻
            if not news_list or len(news_list) < len(articles):
                break
            page += 1

        # 遍历当天的新闻链接，获取标题和正文并保存为 Markdown 文件
        for link in news_list:
            md_file = self._fetch_and_save_full_news(link)
            if md_file:
                saved_files.append(md_file)

        return saved_files  # 返回保存的 md 文件路径列表

    def _fetch_and_save_full_news(self, news_link):
        """使用 newspaper3k 获取新闻的标题和正文并保存，返回生成的文件路径"""
        article = Article(news_link)
        article.download()
        article.parse()

        title = article.title
        content = article.text

        # 保存为 Markdown 文件，并返回文件路径
        return self._save_news_to_md(title, content) if title and content else None

class RepublicanNewsCrawler(NewsCrawlerBase):
    def __init__(self, config_manager):
        super().__init__(config_manager, "republican")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }  # 模拟浏览器请求头

    def fetch_news(self):
        print("Fetching Republican news...")
        page = 1
        news_list = []
        saved_files = []  # 存储生成的 md 文件路径
        while True:
            url = self.url_template.format(page)
            response = requests.get(url, headers=self.headers)  # 添加请求头
            if response.status_code == 403:
                print("Access Forbidden. Trying again with a delay...")
                time.sleep(random.uniform(3, 6))  # 随机延迟以避免被屏蔽
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            # 查找所有新闻稿，标题在 class="c-blog-title" 的 h5 内的 <a> 标签，日期在 class="c-publish-date" 的 <span> 标签
            articles = soup.find_all('div', class_='c-blog-item')
            if not articles:
                break

            for article in articles:
                # 获取新闻链接
                title_tag = article.find('h5', class_='c-blog-title')
                link_tag = title_tag.find('a') if title_tag else None
                if link_tag and 'href' in link_tag.attrs:
                    news_link = link_tag['href']

                    # 获取新闻发布日期
                    date_tag = article.find('span', class_='c-publish-date')
                    if date_tag:
                        news_date_str = date_tag.text.strip()

                        # 日期格式为 "sep 05, 2024"，转换为 "yyyy-mm-dd"
                        news_date = datetime.datetime.strptime(news_date_str, "%b %d, %Y").strftime("%Y-%m-%d")

                        # 检查新闻日期是否为今天
                        if news_date == self.today_str:
                            news_list.append(news_link)

            # 如果没有新的新闻，或者已经获取完当天新闻，则退出循环
            if not news_list or len(news_list) < len(articles):
                break
            page += 1

        # 遍历当天的新闻链接，获取标题和正文并保存为 Markdown 文件
        for link in news_list:
            md_file = self._fetch_and_save_full_news(link)
            if md_file:
                saved_files.append(md_file)

        return saved_files  # 返回保存的 md 文件路径列表

    def _fetch_and_save_full_news(self, news_link):
        """使用 requests 和 BeautifulSoup 获取新闻的标题和正文并保存，返回生成的文件路径"""
        response = requests.get(news_link, headers=self.headers)
        if response.status_code == 403:
            print(f"Access Forbidden for {news_link}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # 假设标题和正文的标签如下，实际情况需要根据页面的 HTML 结构调整
        title = soup.find('div', class_='c-title').get_text(strip=True)
        content = soup.find('div', class_='c-blog-description').get_text(strip=True)

        # 保存为 Markdown 文件，并返回文件路径
        return self._save_news_to_md(title, content) if title and content else None

# 测试代码
if __name__ == '__main__':
    config_manager = ConfigManager()
    
    democrat_crawler = DemocratNewsCrawler(config_manager)
    democrat_crawler.today_str = '2024-09-04'
    democrat_news = democrat_crawler.fetch_news()
    print(democrat_news)

    republican_crawler = RepublicanNewsCrawler(config_manager)
    republican_crawler.today_str = '2024-09-04'
    republican_news = republican_crawler.fetch_news()
    print(republican_news)
