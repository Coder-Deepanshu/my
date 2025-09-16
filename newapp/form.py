from django import forms
# for editing bulk students
class BulkStudentEditForm(forms.Form):
    FIELD_CHOICES = [
        ('father_name','Father_name'),
        ('course', 'Course'),
        ('year', 'Year'),
        ('semester', 'Semester'),
        ('address', 'Address'),
        ('city', 'City'),
        ('state', 'State'),
        ('country', 'Country'),
    ]
    
    field = forms.ChoiceField(choices=FIELD_CHOICES)
    value = forms.CharField(max_length=100)


from django import forms
from .models import Students,Department



class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['roll_no', 'name', 'course']


from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name","code","type","programs_count","faculty_count","student_capacity"]







