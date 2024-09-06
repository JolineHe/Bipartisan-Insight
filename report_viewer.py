import gradio as gr
import os

class ReportViewerUI:
    def __init__(self, bipartisan_insight):
        self.bipartisan_insight = bipartisan_insight  # 传入主业务逻辑类实例

    def get_report_list(self, party):
        """获取指定党派的报告列表"""
        report_dir = f"data/reports/{party}"
        return [f for f in os.listdir(report_dir) if f.endswith('.md')] if os.path.exists(report_dir) else []

    def generate_report(self, party):
        """生成指定党派的当天新闻报告并展示内容"""
        return self.bipartisan_insight.job(party)

    def display_report(self, party, selected_report):
        """根据选中的报告展示其内容"""
        report_file = f"data/reports/{party}/{selected_report}"
        if os.path.exists(report_file):
            with open(report_file, 'r') as f:
                return f.read()
        return "Report not found."

    def create_party_tab(self, party):
        """创建指定党派的Tab，包括生成报告按钮和下拉框"""
        with gr.TabItem(party.capitalize()):
            with gr.Row():
                report_dropdown = gr.Dropdown(choices=self.get_report_list(party), label=f"Select {party.capitalize()} Report")
                generate_button = gr.Button(f"Generate {party.capitalize()} Report")

            report_display = gr.Markdown()

            # Dropdown action to display the selected report
            report_dropdown.change(
                self.display_report, 
                inputs=[gr.State(party), report_dropdown], 
                outputs=report_display
            )

            # Button action to generate today's report and update dropdown
            generate_button.click(
                self.generate_report, 
                inputs=[gr.State(party)], 
                outputs=[report_display, report_dropdown]
            )

    def launch(self):
        """启动 Gradio 界面"""
        with gr.Blocks() as app:
            gr.Markdown("# Political News Report Generator")
            with gr.Tabs():
                self.create_party_tab("democrat")
                self.create_party_tab("republican")
            app.launch()
