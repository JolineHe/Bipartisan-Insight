import os
import datetime

class ReportGenerator:
    def __init__(self):
        pass

    def generate(self, analysis_result):
        today = datetime.date.today().strftime("%Y-%m-%d")
        report_file = f"data/reports/{today}_report.md"
        
        with open(report_file, "w") as f:
            f.write(f"# Daily Political Analysis Report ({today})\n\n")
            f.write(analysis_result)
        
        return report_file
