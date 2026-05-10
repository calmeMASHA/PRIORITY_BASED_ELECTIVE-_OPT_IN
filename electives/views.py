import csv
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .models import Elective, Student, Preference, Allocation
from .forms import PreferenceSubmitForm
from .utils import allocate_electives

def submit_preference(request):
    if request.method == 'POST':
        form = PreferenceSubmitForm(request.POST)
        if form.is_valid():
            usn = form.cleaned_data['usn']
            p1 = form.cleaned_data['preference_1']
            p2 = form.cleaned_data['preference_2']
            p3 = form.cleaned_data['preference_3']
            
            student = Student.objects.get(usn=usn)
            
            # Clear old preferences
            Preference.objects.filter(student=student).delete()
            
            Preference.objects.create(student=student, elective=p1, rank=1)
            Preference.objects.create(student=student, elective=p2, rank=2)
            Preference.objects.create(student=student, elective=p3, rank=3)
            
            messages.success(request, f"Preferences saved successfully for {student.name}.")
            return redirect('submit_preference')
    else:
        form = PreferenceSubmitForm()
        
    return render(request, 'electives/submit.html', {'form': form})

def seat_count(request, elective_id):
    try:
        elective = Elective.objects.get(pk=elective_id)
        return JsonResponse({'available_seats': elective.available_seats})
    except Elective.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

def admin_dashboard(request):
    if request.method == 'POST' and 'allocate' in request.POST:
        count = allocate_electives()
        messages.success(request, f"Successfully allocated {count} students.")
        return redirect('admin_dashboard')
        
    electives = Elective.objects.all()
    allocations = Allocation.objects.all().select_related('student', 'elective')
    preferences = Preference.objects.all().select_related('student', 'elective').order_by('student', 'rank')
    
    # Get distinct branches for filter
    branches = Student.objects.values_list('branch', flat=True).distinct()
    
    return render(request, 'electives/admin_dashboard.html', {
        'electives': electives,
        'allocations': allocations,
        'preferences': preferences,
        'branches': branches
    })

def export_allocations(request):
    branch_filter = request.GET.get('branch', '')
    
    allocations = Allocation.objects.all().select_related('student', 'elective')
    if branch_filter:
        allocations = allocations.filter(student__branch__iexact=branch_filter)
        
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="allocations_{branch_filter or "all"}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Student USN', 'Name', 'Branch', 'CGPA', 'Allocated Elective', 'Elective Code'])
    
    for alloc in allocations:
        writer.writerow([
            alloc.student.usn,
            alloc.student.name,
            alloc.student.branch,
            alloc.student.cgpa,
            alloc.elective.name,
            alloc.elective.code
        ])
        
    return response
