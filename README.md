# Priority-Based Elective Opt-In System

A Django web app for fair, transparent elective course allocation. Students submit preferences, and the system allocates seats based on priority rules (CGPA and submission timestamp), with real-time seat availability via AJAX.

## Core Features
1. **Elective Registration**: Form to accept Student USN and rank preferences 1-3.
2. **Real-Time Seat Counter (AJAX)**: Live seat availability.
3. **Allocation Logic**: Priority-based allocation (CGPA desc → timestamp asc).
4. **Allocation Report (CSV)**: Export allocations with branch filters.
5. **Responsive UI**: Built with Bootstrap 5.

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install django pandas
   ```
2. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. **Seed database with provided dataset:**
   ```bash
   python load_data.py
   ```
4. **Run development server:**
   ```bash
   python manage.py runserver
   ```

## CO Mapping

| CO | How Demonstrated | SDG |
|---|---|---|
| CO1 | URL routing for preferences/allocation/export | SDG 4.3 |
| CO2 | Preference model + validated forms | SDG 4.5 |
| CO3 | Reusable base.html + responsive views | SDG 10.2 |
| CO4 | CSV export with filtered querysets | SDG 16.6 |
| CO5 | AJAX seat counter | SDG 9.C |

## SDG Justification

“Our Priority-Based Elective Opt-In system advances SDG 4: Quality Education (Target 4.5) by implementing a transparent, rule-based allocation algorithm that ensures equitable access to specialized courses regardless of section, background, or submission timing. The CSV export (CO4) supports SDG 16 (Target 16.6) by providing auditable allocation reports. Built with Django validated forms (CO2) and AJAX seat counters (CO5), the system demonstrates responsive design that reduces bias in academic opportunity distribution while promoting inclusive access to technical education.”
