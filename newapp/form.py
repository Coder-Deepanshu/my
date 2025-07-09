from django import forms
from .models import Student_add

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
from .models import Student_add

class Addstudentform(forms.ModelForm):
    class Meta:
        model = Student_add
        exclude = ['Student_rollno']  # <-- yahan sirf yeh line badli hai
        widgets = {
            'Student_name': forms.TextInput(attrs={'placeholder': 'Enter Full Name of the Student'}),
            'Father_name': forms.TextInput(attrs={'placeholder': 'Enter Father\'s Name'}),
            'phone_no': forms.TextInput(attrs={'placeholder': 'Enter Phone Number (e.g., 9876543210)'}),
            'Address': forms.TextInput(attrs={'placeholder': 'Enter Residential Address'}),
            'Email': forms.EmailInput(attrs={'placeholder': 'Enter Email Address (e.g., example@gmail.com)'}),
            'course': forms.Select(attrs={'placeholder': 'Select Course'}),
            'tenth_dmc': forms.ClearableFileInput(attrs={'placeholder': 'Upload 10th Marksheet'}),
            'twelth': forms.ClearableFileInput(attrs={'placeholder': 'Upload 12th Marksheet'}),
        }

    # def clean_Student_rollno(self):
    #     rollno = self.cleaned_data.get('Student_rollno')
    #     if Student_add.objects.filter(Student_rollno=rollno).exists():
    #         raise forms.ValidationError("A student with this roll number already exists.")
    #     return rollno

    # def clean_phone_no(self):
    #     phone_no = self.cleaned_data.get('phone_no')
    #     if not phone_no.isdigit() or len(phone_no) != 10:
    #         raise forms.ValidationError("Enter a valid 10-digit phone number.")
    #     if Student_add.objects.filter(phone_no=phone_no).exists():
    #         raise forms.ValidationError("A student with this phone number already exists.")
    #     return phone_no

    # def clean_Email(self):
    #     email = self.cleaned_data.get('Email')
    #     if Student_add.objects.filter(Email=email).exists():
    #         raise forms.ValidationError("A student with this email already exists.")
    #     return email

# for delete data
from django import forms

class DeleteStudentForm(forms.Form):
    roll_no = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Roll Number'}),
        label="Roll Number")
    
#  for add_result 
class add_result(forms.Form):
    roll_no = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Roll Number'}),
        label="Roll Number")
    
# for BBA
from .models import BBA,BCA,B_Com,B_A,B_Sc
class B_B_A(forms.ModelForm):
    class Meta:
        model = BBA
        fields = '__all__'  # Include all fields from the model
        widgets = {
            'rollno': forms.TextInput(attrs={'placeholder': 'Enter Student Roll Number'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter Student Name'}),
            'management': forms.TextInput(attrs={'placeholder': 'Principle of Management'}),
            'economics': forms.TextInput(attrs={'placeholder': 'Business Economics'}),
            'mathematics': forms.TextInput(attrs={'placeholder': 'Business Mathematics'}),
            'accounting': forms.TextInput(attrs={'placeholder': 'Principle of Accounting'}),
            'communication': forms.TextInput(attrs={'placeholder': 'Business Communication'}),
            'computer': forms.TextInput(attrs={'placeholder':'Fundamental of Computer'}),
        }
# for BCA
class B_C_A(forms.ModelForm):
    class Meta:
        model = BCA
        fields = '__all__'  # Include all fields from the model
        widgets = {
            'rollno': forms.TextInput(attrs={'placeholder': 'Enter Student Roll Number'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter Student Name'}),
            'C': forms.TextInput(attrs={'placeholder': 'Programming C'}),
            'Digital_Electronics': forms.TextInput(attrs={'placeholder': 'Digital Electronics'}),
            'mathematics_I': forms.TextInput(attrs={'placeholder': 'Mathematics-1'}),
            'communication': forms.TextInput(attrs={'placeholder': 'Communication Skills'}),
            'computer': forms.TextInput(attrs={'placeholder':'Fundamental of Computer'}),
        }

# for B.sc
class B_sc(forms.ModelForm):
    class Meta:
        model = B_Sc
        fields = '__all__'  # Include all fields from the model
        widgets = {
            'rollno': forms.TextInput(attrs={'placeholder': 'Enter Student Roll Number'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter Student Name'}),
            'Physics': forms.TextInput(attrs={'placeholder': 'Physics'}),
            'Chemistry': forms.TextInput(attrs={'placeholder': 'Chemistry'}),
            'mathematics_I': forms.TextInput(attrs={'placeholder': 'Mathematics-1'}),
            'communication': forms.TextInput(attrs={'placeholder': 'Communication Skills'}),
            'computer': forms.TextInput(attrs={'placeholder':'Fundamental of Computer'}),
            'Environmental_science': forms.TextInput(attrs={'placeholder':'Environmental Science'}),
        }

# for B.a
class B_a(forms.ModelForm):
    class Meta:
        model = B_A
        fields = '__all__'  # Include all fields from the model
        widgets = {
            'rollno': forms.TextInput(attrs={'placeholder': 'Enter Student Roll Number'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter Student Name'}),
            'english_literature': forms.TextInput(attrs={'placeholder': 'English Literature'}),
            'history': forms.TextInput(attrs={'placeholder': 'History'}),
            'economics': forms.TextInput(attrs={'placeholder': 'Economics-Macro'}),
            'sociology': forms.TextInput(attrs={'placeholder': 'Sociology'}),
            'political_science': forms.TextInput(attrs={'placeholder':'Political Science'}),
            'hindi': forms.TextInput(attrs={'placeholder':'Hindi'}),
            'psychology':forms.TextInput(attrs={'placeholder':'Psychology'})
        }

# for B.com
class B_com(forms.ModelForm):
    class Meta:
        model = B_Com
        fields = '__all__'  # Include all fields from the model
        widgets = {
            'rollno': forms.TextInput(attrs={'placeholder': 'Enter Student Roll Number'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter Student Name'}),
            'Financial_Accounting': forms.TextInput(attrs={'placeholder': 'Enter Marks'}),
            'Business_management': forms.TextInput(attrs={'placeholder': 'Enter Marks'}),
            'mathematics': forms.TextInput(attrs={'placeholder': 'Enter Marks'}),
            'communication': forms.TextInput(attrs={'placeholder': 'Enter Marks'}),
            'environmental_studies': forms.TextInput(attrs={'placeholder':'Enter Marks'}),
            'Business_law': forms.TextInput(attrs={'placeholder':'Enter Marks'}),
            'Business_economics': forms.TextInput(attrs={'placeholder':'Enter Marks'}),
        }

#  for delete result
class delete_result(forms.Form):
    roll_no = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Roll Number'}),
        label="Roll Number")

# for view the result
class view_result(forms.Form):
    roll_no = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Roll Number'}),
        label="Roll Number")





