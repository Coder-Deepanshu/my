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


from django import forms
from .models import FriendshipProposal

class ContactForm(forms.ModelForm):
    class Meta:
        model = FriendshipProposal
        fields = ['friend_name', 'user_phone', 'user_email']
        widgets = {
            'friend_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name (optional)'
            }),
            'user_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your phone number',
                'required': True
            }),
            'user_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email (optional)'
            }),
        }
    
    def clean_user_phone(self):
        phone = self.cleaned_data.get('user_phone')
        if phone:
            # Remove all non-numeric characters
            phone = ''.join(filter(str.isdigit, phone))
            
            # Basic phone validation
            if len(phone) < 10:
                raise forms.ValidationError("Phone number must be at least 10 digits")
            
            # Check if phone already exists (optional)
            if FriendshipProposal.objects.filter(user_phone=phone).exists():
                # You can comment this out if you want to allow duplicates
                raise forms.ValidationError("This phone number has already been registered")
        
        return phone
    
    def clean_user_email(self):
        email = self.cleaned_data.get('user_email')
        if email:
            # Check if email already exists (optional)
            if FriendshipProposal.objects.filter(user_email=email).exists():
                # You can comment this out if you want to allow duplicates
                raise forms.ValidationError("This email has already been registered")
        return email


from django import forms
from .models import BirthdayGreeting

class BirthdayGreetingForm(forms.ModelForm):
    greeting_message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Enter your birthday message here...',
            'class': 'form-control'
        }),
        required=False,
        initial="Happy Birthday! Wishing you all the happiness in the world!"
    )
    
    class Meta:
        model = BirthdayGreeting
        fields = ['photo', 'greeting_message']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

