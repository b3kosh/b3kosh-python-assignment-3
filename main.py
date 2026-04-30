import os
import csv
import json

class FileManager:
    def setup(self):
        if not os.path.exists('students.csv'):
            return False
        if not os.path.exists('output'):
            os.makedirs('output')
        return True

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        students = []
        try:
            with open(self.file_path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    students.append(row)
            return students
        except Exception:
            return None

class DataAnalyser:
    def __init__(self, students_list):
        self.students = students_list
        self.result = {}

    def analyse(self):
        low_sleep_gpas = []
        high_sleep_gpas = []
        for s in self.students:
            try:
                sleep = float(s['sleep_hours'])
                gpa = float(s['gpa'])
                if sleep < 6:
                    low_sleep_gpas.append(gpa)
                else:
                    high_sleep_gpas.append(gpa)
            except (ValueError, KeyError):
                continue

        avg_low = round(sum(low_sleep_gpas) / len(low_sleep_gpas), 2) if low_sleep_gpas else 0
        avg_high = round(sum(high_sleep_gpas) / len(high_sleep_gpas), 2) if high_sleep_gpas else 0
        
        self.result = {
            "analysis": "Sleep vs GPA",
            "total_students": len(self.students),
            "low_sleep": {"count": len(low_sleep_gpas), "avg_gpa": avg_low},
            "high_sleep": {"count": len(high_sleep_gpas), "avg_gpa": avg_high},
            "gpa_difference": round(abs(avg_high - avg_low), 2)
        }
        return self.result

    def run_filters(self):
        low_sleep = list(filter(lambda s: float(s['sleep_hours']) < 6, self.students))
        print(f"Count of filtered students (sleep < 6): {len(low_sleep)}")
        
        gpa_values = list(map(lambda s: float(s['gpa']), self.students))
        print(f"First 5 GPA values: {gpa_values[:5]}")

        stressed = list(filter(lambda s: float(s['mental_stress_level']) > 7, self.students))
        print(f"Count of filtered students (stress > 7): {len(stressed)}")

class ResultSaver:
    def __init__(self, report_data):
        self.report_data = report_data

    def save(self):
        path = 'output/result.json'
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.report_data, f, indent=4)
            print(f"Results saved to {path}")
        except Exception:
            pass

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    f_manager = FileManager()
    if f_manager.setup():
        loader = DataLoader('students.csv')
        data = loader.load()
        if data:
            analyser = DataAnalyser(data)
            report = analyser.analyse()
            analyser.run_filters()
            
            saver = ResultSaver(report)
            saver.save()
    else:
        print("Error: students.csv not found!")