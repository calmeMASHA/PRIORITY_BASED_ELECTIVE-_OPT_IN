from django import forms
from .models import Student, Elective, Preference, Allocation
from django.core.exceptions import ValidationError

class PreferenceSubmitForm(forms.Form):
    usn = forms.CharField(max_length=20, label="Student USN", widget=forms.TextInput(attrs={'class': 'form-control'}))
    preference_1 = forms.ModelChoiceField(
        queryset=Elective.objects.all(), 
        label="Preference 1",
        widget=forms.Select(attrs={'class': 'form-select elective-select'})
    )
    preference_2 = forms.ModelChoiceField(
        queryset=Elective.objects.all(), 
        label="Preference 2",
        widget=forms.Select(attrs={'class': 'form-select elective-select'})
    )
    preference_3 = forms.ModelChoiceField(
        queryset=Elective.objects.all(), 
        label="Preference 3",
        widget=forms.Select(attrs={'class': 'form-select elective-select'})
    )

    def clean_usn(self):
        usn = self.cleaned_data.get('usn')
        if not Student.objects.filter(usn=usn).exists():
            raise ValidationError("Student with this USN does not exist in the system.")
        if Allocation.objects.filter(student__usn=usn).exists():
            raise ValidationError("You have already been allocated an elective.")
        # We allow resubmitting preferences if they aren't allocated yet
        return usn

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('preference_1')
        p2 = cleaned_data.get('preference_2')
        p3 = cleaned_data.get('preference_3')

        usn = cleaned_data.get('usn')
        student = Student.objects.filter(usn=usn).first()

        if p1 and p2 and p3:
            if len({p1.pk, p2.pk, p3.pk}) != 3:
                raise ValidationError("Preferences must be unique. You cannot choose the same elective multiple times.")
                
            if student:
                for i, p in enumerate([p1, p2, p3], 1):
                    if p.max_cet_rank is not None:
                        if student.cet_rank is None:
                            raise ValidationError(f"Preference {i} ({p.name}) requires a CET Rank, but you don't have one.")
                        if student.cet_rank > p.max_cet_rank:
                            raise ValidationError(f"Your CET Rank ({student.cet_rank}) does not meet the requirement for Preference {i} ({p.name}). You need a rank of {p.max_cet_rank} or better.")

        return cleaned_data
