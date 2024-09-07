# Bipartisan Insight: AI-Powered Political News Analysis

## Overview
**Bipartisan Insight** is an AI-powered application that automatically gathers, analyzes, and generates daily reports on political news from the official websites of the Democratic and Republican parties in the United States. The application utilizes OpenAI models (GPT-4 or GPT-3.5) to analyze news articles, identifying key themes, strategies, and focus areas of both parties.

### Key Features:
- **Automated News Fetching**: Fetches daily news from the Democratic and Republican National Committee websites.
- **AI-Powered Analysis**: Leverages OpenAI's GPT models to generate insights based on the fetched news.
- **Gradio Interface**: Provides a simple web interface for generating and browsing reports.
- **Email Notifications**: Automatically sends daily reports via email.
- **Configurable Schedules**: Allows users to set daily schedules for automated tasks.

## Installation

### Prerequisites:
- Python 3.8+
- An OpenAI API key (for GPT-4/GPT-3.5 access)
- SMTP credentials for sending email notifications
- Docker (Optional) for containerized deployment

### Step-by-Step Installation:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/bipartisan-insight.git
   cd bipartisan-insight
   ```

2. **Install Dependencies**:
   You can install the required packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**:
   - Set the OpenAI API key as an environment variable:
     ```bash
     export OPENAI_API_KEY="your_openai_api_key"
     ```
   - Set the email sender password for notifications:
     ```bash
     export SENDER_EMAIL_PASSWORD="your_smtp_password"
     ```

4. **Configure `config.json`**:
   Edit the `config.json` file to configure the schedule, email settings, and URLs for fetching news:
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

## Usage

### 1. Run the Application:
Start the application with:
```bash
python bipartisan_insight.py
```

### 2. Access the Gradio Interface:
Once the application is running, open the Gradio interface in your browser to manually generate reports or browse historical reports:
```
http://localhost:7860
```

### 3. Automatic News Fetching and Report Generation:
The system will automatically fetch news, generate reports, and send email notifications based on the configured schedule.

### 4. Customizing AI Models:
You can adjust the AI model in `config.json` to use either GPT-4 or GPT-3.5:
```json
{
  "openai_model": "gpt-3.5-turbo"
}
```

## Project Structure

```
bipartisan-insight/
│
├── data/                   # Stores the fetched news and generated reports
│   ├── news/               # Raw news articles in markdown format
│   └── reports/            # Generated reports for Democrat and Republican parties
│
├── config.json             # Configuration file for scheduling, URLs, and email settings
├── bipartisan_insight.py   # Main entry point for the application
├── report_generation.py    # Logic for generating reports using OpenAI
├── data_acquisition.py     # Logic for fetching news from party websites
├── ai_analysis.py          # AI analysis using OpenAI GPT models
├── email_notification.py   # Email notification logic
├── report_viewer.py        # Gradio-based report browsing UI
├── requirements.txt        # Python package dependencies
└── README.md               # Project documentation
```

## Troubleshooting

1. **OpenAI Rate Limit Error (Error 429)**:
   If you receive a rate limit error from OpenAI, consider splitting news articles into smaller batches or switching to the `gpt-3.5-turbo` model for analysis.

2. **Email Sending Issues**:
   Ensure that your SMTP settings in `config.json` are correct. If you have 2FA enabled for your email account, you may need to generate an app-specific password.

## Contributing

We welcome contributions! Feel free to submit pull requests or open issues to help improve the project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

### 说明：
- **项目概述** 提供了项目的功能简介。
- **安装步骤** 详细描述了如何设置和运行该项目，包括依赖项、配置和环境变量设置。
- **使用指南** 解释了如何启动应用、访问 Gradio 界面以及自动化报告生成。
- **项目结构** 帮助用户理解项目的文件组织结构。
- **故障排除** 提供了一些常见问题的解决方案。

如果你需要进一步调整或添加内容，请随时告诉我！