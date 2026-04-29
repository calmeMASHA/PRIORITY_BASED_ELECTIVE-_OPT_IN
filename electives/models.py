from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Student(models.Model):
    usn = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    branch = models.CharField(max_length=50)
    cgpa = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    cet_rank = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.usn})"

class Elective(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    total_seats = models.PositiveIntegerField()
    max_cet_rank = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum CET rank allowed. Leave blank for no limit.")

    @property
    def allocated_seats(self):
        return self.allocation_set.count()

    @property
    def available_seats(self):
        return max(0, self.total_seats - self.allocated_seats)

    def __str__(self):
        if self.max_cet_rank:
            return f"{self.name} ({self.code}) - Max Rank: {self.max_cet_rank}"
        return f"{self.name} ({self.code})"

class Preference(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    elective = models.ForeignKey(Elective, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('student', 'elective'), ('student', 'rank'))
        ordering = ['student', 'rank']

    def clean(self):
        if Preference.objects.filter(student=self.student, rank=self.rank).exclude(pk=self.pk).exists():
            raise ValidationError(f"Rank {self.rank} is already assigned to another elective for this student.")

    def __str__(self):
        return f"{self.student.usn} - {self.elective.code} (Rank {self.rank})"

class Allocation(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    elective = models.ForeignKey(Elective, on_delete=models.CASCADE)
    allocated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.usn} -> {self.elective.code}"
