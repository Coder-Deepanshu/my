from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your Username'})
    )
    user_id = forms.CharField(
        max_length=100,
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your User ID'})
    )

from django import forms
from .models import result

class uploadresultform(forms.ModelForm):
    class Meta:
        model = result
        exclude = ['Student_rollno','course']  # <-- yahan sirf yeh line badli hai
        widgets = {
            'one': forms.TextInput(),
            'two': forms.TextInput(),
            'three': forms.TextInput(),
            'four': forms.TextInput(),
            'five': forms.TextInput(),
            'six': forms.TextInput(),
            'seven': forms.TextInput(attrs={'placeholder': 'Enter Email Address (e.g., example@gmail.com)'}),
            'eight': forms.TextInput(attrs={'placeholder': 'Select Course'}),
            'nine': forms.TextInput(attrs={'placeholder': 'Enter Your 10th Percentage'}),
            'ten': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'eleven': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twelve': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirteen': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourteen': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifteen': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'sixteen': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'seventeen': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'eighteen': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'nineteen': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_one': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_two': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_three': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_four': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_five': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_six': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_seven': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_eight': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'twenty_nine': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_one': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_two': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_three': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_four': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_five': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_six': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_seven': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_eight': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'thirty_nine': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty_one': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty_two': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty_three': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty_five': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty_six': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty_seven': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty_eight': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fourty_nine': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_one': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_two': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_three': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_four': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_five': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_six': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_seven': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_eight': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'fifty_nine': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'sixty': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'sixty_one': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'sixty_two': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'sixty_three': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'}),
            'sixty_four': forms.TextInput(attrs={'placeholder': 'Enter Your 12th Percentage'})
                }    
from .models import Faculty
class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'
        exclude = ('employee_id',)  # <-- sahi syntax
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Full Name'}),
            'department': forms.TextInput(attrs={'placeholder': 'Enter Department'}),
            'qualification': forms.TextInput(attrs={'placeholder': 'Enter Qualification'}),
            'experience': forms.NumberInput(attrs={'placeholder': 'Enter Experience (e.g., 5.5)'}),
            'date_of_joining': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
            'gender': forms.Select(attrs={'placeholder': 'Select Gender'}),
            'dob': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter Address'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter City'}),
            'state': forms.TextInput(attrs={'placeholder': 'Enter State'}),
            'pin_code': forms.TextInput(attrs={'placeholder': 'Enter Pin Code'}),
        }


from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['status', 'remarks']
        
class DateSelectionForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
class MonthYearForm(forms.Form):
    month = forms.ChoiceField(choices=[(i, i) for i in range(1, 13)])
    year = forms.ChoiceField(choices=[(i, i) for i in range(2020, 2030)])

from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

from django import forms

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


