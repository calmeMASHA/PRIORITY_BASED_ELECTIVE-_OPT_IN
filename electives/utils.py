from django.db.models import Min
from .models import Student, Preference, Allocation

def allocate_electives():
    """
    Allocates electives based on priority:
    1. CGPA (Descending)
    2. Timestamp of submission (Ascending)
    """
    # Find students who haven't been allocated yet, but have submitted preferences
    students = Student.objects.exclude(
        allocation__isnull=False
    ).annotate(
        min_submitted_at=Min('preference__submitted_at')
    ).filter(
        min_submitted_at__isnull=False
    ).order_by('-cgpa', 'min_submitted_at')
    
    allocated_count = 0
    
    for student in students:
        preferences = Preference.objects.filter(student=student).order_by('rank')
        for pref in preferences:
            elective = pref.elective
            # Check available seats (dynamically calculated)
            if elective.available_seats > 0:
                Allocation.objects.create(student=student, elective=elective)
                allocated_count += 1
                break  # Successfully allocated, move to next student
                
    return allocated_count
