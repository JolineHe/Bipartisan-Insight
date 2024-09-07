# 两党洞察：AI 驱动的政治新闻分析

## 概述
**两党洞察** 是一个 AI 驱动的应用程序，自动从美国民主党和共和党官方网站获取、分析每日新闻，并生成报告。该应用利用 OpenAI 模型（GPT-4 或 GPT-3.5）对新闻稿进行分析，帮助识别两党关注的关键主题、策略和立场。

### 主要功能：
- **自动新闻抓取**：自动从民主党和共和党全国委员会网站获取每日新闻。
- **AI 驱动分析**：利用 OpenAI 的 GPT 模型生成基于新闻内容的洞察报告。
- **Gradio 界面**：提供简易的 Web 界面，用于生成和浏览报告。
- **邮件通知**：自动通过邮件发送每日生成的新闻报告。
- **可配置的定时任务**：允许用户设置每日任务的执行时间，自动化流程。

## 安装步骤

### 前提条件：
- Python 3.8+
- OpenAI API 密钥（用于 GPT-4/GPT-3.5 访问）
- SMTP 邮箱服务配置（用于发送邮件通知）
- Docker（可选，用于容器化部署）

### 安装步骤：

1. **克隆仓库**：
   ```bash
   git clone https://github.com/yourusername/bipartisan-insight.git
   cd bipartisan-insight
   ```

2. **安装依赖项**：
   使用 `pip` 安装依赖项：
   ```bash
   pip install -r requirements.txt
   ```

3. **设置环境变量**：
   - 设置 OpenAI API 密钥：
     ```bash
     export OPENAI_API_KEY="your_openai_api_key"
     ```
   - 设置发送邮件的 SMTP 密码：
     ```bash
     export SENDER_EMAIL_PASSWORD="your_smtp_password"
     ```

4. **配置 `config.json` 文件**：
   编辑 `config.json` 文件以配置定时任务、邮件设置以及新闻获取的 URL：
   ```json
   {
     "schedule_time": "10:00",
     "urls": {
       "democrat": "https://democrats.org/news/page/{}/",
       "republican": "https://gop.com/press-releases/?page={}"
     },
     "openai_model": "gpt-4",
     "email": {
       "smtp_server": "smtp.example.com",
       "smtp_port": 587,
       "sender_email": "your_email@example.com",
       "recipient_email": "recipient_email@example.com"
     }
   }
   ```

## 使用方法

### 1. 运行应用程序：
使用以下命令启动应用程序：
```bash
python bipartisan_insight.py
```

### 2. 访问 Gradio 界面：
应用程序启动后，打开浏览器访问 Gradio 界面，可以手动生成报告或浏览历史报告：
```
http://localhost:7860
```

### 3. 自动新闻抓取与报告生成：
系统会根据配置的定时任务，自动抓取新闻、生成报告并发送邮件通知。

### 4. 自定义 AI 模型：
可以在 `config.json` 中调整 AI 模型，使用 GPT-4 或 GPT-3.5：
```json
{
  "openai_model": "gpt-3.5-turbo"
}
```

## 项目结构

```
bipartisan-insight/
│
├── data/                   # 存储获取的新闻和生成的报告
│   ├── news/               # 以 Markdown 格式保存的新闻文章
│   └── reports/            # 生成的民主党和共和党报告
│
├── config.json             # 配置文件，包括定时任务、URL 和邮件设置
├── bipartisan_insight.py   # 主程序入口
├── report_generation.py    # 使用 OpenAI 生成报告的逻辑
├── data_acquisition.py     # 从党派网站获取新闻的逻辑
├── ai_analysis.py          # 使用 OpenAI GPT 模型进行 AI 分析
├── email_notification.py   # 邮件通知逻辑
├── report_viewer.py        # 基于 Gradio 的报告浏览界面
├── requirements.txt        # Python 依赖项
└── README.md               # 项目文档
```

## 故障排除

1. **OpenAI 令牌限制错误 (Error 429)**：
   如果收到 OpenAI 速率限制错误，可以将新闻分成更小的批次，或切换到 `gpt-3.5-turbo` 模型以减少令牌使用量。

2. **邮件发送问题**：
   请确保 `config.json` 中的 SMTP 设置正确。如果使用 2FA，请生成应用专用密码。

## 贡献

欢迎贡献！可以提交 PR 或者打开 Issue 来帮助改进项目。

## 许可证

本项目遵循 MIT 许可证。详细信息请参见 [LICENSE](LICENSE) 文件。
```

### 说明：
- **中文版概述** 提供了项目的功能简介。
- **安装步骤**、**使用方法** 和 **项目结构** 翻译了项目的各个方面，确保中文用户可以顺利使用项目。
- **故障排除** 部分列出了常见问题的解决方案。

如果你有其他修改意见或进一步需求，请告诉我！