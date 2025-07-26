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
from .models import Faculty_Add
class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty_Add
        fields = '__all__'
        exclude = ('employee_id',)  # <-- sahi syntax
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
            'father_name': forms.TextInput(attrs={'placeholder': "Enter Father's Name"}),
            'department': forms.TextInput(attrs={'placeholder': 'Enter Department'}),
            'position': forms.TextInput(attrs={'placeholder': 'Enter Position'}),
            'experience': forms.NumberInput(attrs={'placeholder': 'e.g., 5.5'}),
            'date_of_joining': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
            'qualification':forms.TextInput(attrs={'placeholder':'Enter Qualification'}),
            # Select Dropdowns
            'gender': forms.Select(attrs={'placeholder': 'Select Gender'}),
            'dob': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter Address'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter City'}),
            'state': forms.TextInput(attrs={'placeholder': 'Enter State'}),
            'pin_code': forms.TextInput(attrs={'placeholder': 'Enter Pin Code'}),

            'category': forms.Select(attrs={'placeholder': 'Select Category'}),
            'nationality': forms.Select(attrs={'placeholder': 'Select Nationality'}),
            'religion': forms.Select(attrs={'placeholder': 'Select Religion'}),

            'adhar_no': forms.NumberInput(attrs={'placeholder': 'Enter Aadhar Number'}),
            'pan_no': forms.TextInput(attrs={'placeholder': 'Enter PAN Number'}),

            'status': forms.Select(attrs={'placeholder': 'Select Marital Status'}),

        }
# for adding students
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


