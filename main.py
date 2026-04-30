import os
import csv
import json

class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True
        else:
            print(f"Error: {self.filename} not found!")
            return False

    def create_output_folder(self, folder='output'):
        print("Checking output folder...")
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Output folder created: {folder}/")
        else:
            print(f"Output folder already exists: {folder}/")

class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("Loading data...")
        try:
            with open(self.filename, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                self.students = [row for row in reader]
            print(f"Data loaded successfully: {len(self.students)} students")
            return self.students
        except FileNotFoundError:
            print("Error: File not found during loading.")
            return []

    def preview(self, n=5):
        print(f"First {n} rows:")
        for s in self.students[:n]:
            print(f"{s.get('id', 'N/A')} | {s.get('age', 'N/A')} | {s.get('gender', 'N/A')} | {s.get('country', 'N/A')} | GPA: {s.get('gpa', 'N/A')}")

class DataAnalyser:
    def __init__(self, students):
        self.students = students
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
            "variant": "C",
            "analysis": "Sleep vs GPA Analysis",
            "low_sleep": {"count": len(low_sleep_gpas), "avg_gpa": avg_low},
            "high_sleep": {"count": len(high_sleep_gpas), "avg_gpa": avg_high},
            "gpa_difference": round(abs(avg_high - avg_low), 2)
        }
        return self.result

    def print_results(self):
        res = self.result
        print("Sleep vs GPA Analysis")
        print(f"Students sleeping < 6 hours: {res['low_sleep']['count']} | avg GPA: {res['low_sleep']['avg_gpa']}")
        print(f"Students sleeping >= 6 hours: {res['high_sleep']['count']} | avg GPA: {res['high_sleep']['avg_gpa']}")
        print(f"GPA difference: {res['gpa_difference']}")

    def run_task_c3(self):
        low_sleep = list(filter(lambda s: float(s['sleep_hours']) < 6, self.students))
        print(f"Count of filtered students (sleep < 6): {len(low_sleep)}")

        gpa_values = list(map(lambda s: float(s['gpa']), self.students))
        print(f"First 5 GPA values: {gpa_values[:5]}")

        stressed = list(filter(lambda s: float(s['mental_stress_level']) > 7, self.students))
        print(f"Count of filtered students (stress > 7): {len(stressed)}")

class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(self.result, f, indent=4)
            print(f"Result saved to {self.output_path}")
        except Exception as e:
            print(f"Save error: {e}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    fm = FileManager('students.csv')
    if not fm.check_file():
        print('Stopping program.')
        exit()
    fm.create_output_folder()

    dl = DataLoader('students.csv')
    dl.load()
    dl.preview()

    analyser = DataAnalyser(dl.students)
    analyser.analyse()
    analyser.print_results()
    analyser.run_task_c3()

    saver = ResultSaver(analyser.result, 'output/result.json')
    saver.save_json()