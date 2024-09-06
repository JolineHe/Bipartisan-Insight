import gradio as gr
import os
from report_generation import ReportGenerator
from config_manager import ConfigManager

def get_report_list(party):
    """获取指定党派的报告列表"""
    report_dir = f"data/reports/{party}"
    if not os.path.exists(report_dir):
        return []
    return [f for f in os.listdir(report_dir) if f.endswith('.md')]

def generate_report(party):
    """生成指定党派的当天新闻报告并展示内容"""
    config_manager = ConfigManager()
    news_dir = f"data/news/{party}"
    news_files = [os.path.join(news_dir, file) for file in os.listdir(news_dir) if file.endswith('.md')]
    
    if not news_files:
        return f"No news available for {party.capitalize()} today.", get_report_list(party)
    
    report_generator = ReportGenerator(config_manager, party)
    report_file = report_generator.generate(news_files)
    
    # 读取生成的报告内容
    with open(report_file, 'r') as f:
        report_content = f.read()
    
    # 更新下拉框的选项
    return report_content, get_report_list(party)

def display_report(party, selected_report):
    """根据选中的报告展示其内容"""
    report_file = f"data/reports/{party}/{selected_report}"
    if os.path.exists(report_file):
        with open(report_file, 'r') as f:
            return f.read()
    return "Report not found."

def create_party_tab(party):
    """创建指定党派的Tab，包括生成报告按钮和下拉框"""
    with gr.TabItem(party.capitalize()):
        # Dropdown to select past reports and button side by side
        with gr.Row():
            report_dropdown = gr.Dropdown(choices=get_report_list(party), label=f"Select {party.capitalize()} Report")
            generate_button = gr.Button(f"Generate {party.capitalize()} Report")

        # Display for selected or generated report
        report_display = gr.Markdown()

        # Dropdown action to display the selected report
        report_dropdown.change(
            display_report, 
            inputs=[gr.State(party), report_dropdown], 
            outputs=report_display
        )

        # Button action to generate today's report and update dropdown
        generate_button.click(
            generate_report, 
            inputs=[gr.State(party)], 
            outputs=[report_display, report_dropdown]
        )

# Gradio app layout
with gr.Blocks() as app:
    gr.Markdown("# Political News Report Generator")
    with gr.Tabs():
        create_party_tab("democrat")
        create_party_tab("republican")

# Launch the app
if __name__ == "__main__":
    app.launch()
