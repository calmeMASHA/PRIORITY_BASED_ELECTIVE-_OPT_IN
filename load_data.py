import os
import django
import csv
import random
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elective_optin.settings')
django.setup()

from electives.models import Student, Elective

def run():
    print("Clearing existing data...")
    Student.objects.all().delete()
    Elective.objects.all().delete()

    print("Creating Electives...")
    electives_data = [
        {'code': 'CS501', 'name': 'Advanced Algorithms', 'total_seats': 40, 'max_cet_rank': 10000},
        {'code': 'CS502', 'name': 'Machine Learning', 'total_seats': 50, 'max_cet_rank': 15000},
        {'code': 'CS503', 'name': 'Cloud Computing', 'total_seats': 60, 'max_cet_rank': 20000},
        {'code': 'CS504', 'name': 'Cyber Security', 'total_seats': 30, 'max_cet_rank': None},
        {'code': 'CS505', 'name': 'Artificial Intelligence', 'total_seats': 40, 'max_cet_rank': 25000},
        {'code': 'CS506', 'name': 'Internet of Things', 'total_seats': 50, 'max_cet_rank': 40000},
        {'code': 'CS507', 'name': 'Blockchain Tech', 'total_seats': 40, 'max_cet_rank': 60000},
        {'code': 'CS508', 'name': 'Web Development', 'total_seats': 80, 'max_cet_rank': None},
        {'code': 'CS509', 'name': 'Data Science', 'total_seats': 50, 'max_cet_rank': 100000},
        {'code': 'CS510', 'name': 'Software Engineering', 'total_seats': 80, 'max_cet_rank': None},
    ]

    for ed in electives_data:
        Elective.objects.create(code=ed['code'], name=ed['name'], total_seats=ed['total_seats'], max_cet_rank=ed['max_cet_rank'])

    print("Loading Students...")
    try:
        with open('data.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            headers = reader.fieldnames
            if headers:
                headers = [h.strip() for h in headers]
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    count = 0
    try:
        with open('data.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                # Clean up row keys
                clean_row = {k.strip(): v for k, v in row.items()}
                
                usn = clean_row.get('USN', '').strip()
                if not usn or usn == 'nan':
                    continue
                
                name = clean_row.get('Student Name', f'Student {count}').strip()
                branch = clean_row.get('Branch', 'CSE').strip()
                
                # Generate random CGPA between 5.0 and 10.0 for simulation
                cgpa = round(random.uniform(5.0, 10.0), 2)
                
                # Parse CET rank
                cet_rank_val = clean_row.get('CET/COMEDK/DCET Rank', '').strip()
                cet_rank = None
                if cet_rank_val and cet_rank_val != 'nan' and cet_rank_val != '':
                    try:
                        # Remove any letters like 'G55' (e.g. 19601G55 from the dataset)
                        clean_rank = re.sub(r'[^\d]', '', str(cet_rank_val))
                        if clean_rank:
                            cet_rank = int(clean_rank)
                    except ValueError:
                        pass
                
                Student.objects.update_or_create(
                    usn=usn,
                    defaults={
                        'name': name,
                        'branch': branch,
                        'cgpa': cgpa,
                        'cet_rank': cet_rank
                    }
                )
                count += 1
    except Exception as e:
        print(f"Error loading students: {e}")
        return

    print(f"Loaded {count} students successfully.")

if __name__ == '__main__':
    run()
