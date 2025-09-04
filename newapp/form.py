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





