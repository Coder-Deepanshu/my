# import csv
# from django.http import HttpResponse
from django.shortcuts import render, redirect
# from reportlab.pdfgen import canvas
# from .form import LoginForm
# from newapp.models import result

# def generate_csv(request):
#     # Create the HttpResponse object with the appropriate CSV header.
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="data.csv"'

#     # Create a CSV writer object.
#     writer = csv.writer(response)

#     # Write the header row.
#     writer.writerow(['Column 1', 'Column 2', 'Column 3'])

#     # Write some example data rows.
#     writer.writerow(['Row 1 Col 1', 'Row 1 Col 2', 'Row 1 Col 3'])
#     writer.writerow(['Row 2 Col 1', 'Row 2 Col 2', 'Row 2 Col 3'])

#     return response

# def generate_pdf(request):
#     # Create the HttpResponse object with the appropriate PDF headers.
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="students.pdf"'

#     # Create a PDF object using ReportLab.
#     p = canvas.Canvas(response)

#     # Write content to the PDF.
#     students = Student_add.objects.all()
#     y = 800  # Start position for writing
#     p.drawString(100, y, "Student List")
#     y -= 20
#     for student in students:
#         p.drawString(100, y, f"Roll No: {student.Student_rollno}, Name: {student.Student_name}, Class: {student.course}")
#         y -= 20

#     # Finalize the PDF.
#     p.showPage()
#     p.save()
#     return response

def login_view(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        role=request.POST.get('role')
        if role =='admin':
            if (username == "Deepanshu" and password == "12345") or (username == "Zyasha" and password == "12346") :  # Replace with your logic
                # Set session data
                request.session['username1'] = username
                return redirect('dashboard')  # Redirect to the dashboard
            else:
                return redirect("login")
        elif role=='faculty':
            if username == 'Kunal' and password== "12345":
                request.session['username2']=username
                return redirect('dashboard1')
            else:
                return redirect("login")
        else :
            if username == 'Abhishek' and password== "12345":
                request.session['username3']=username
                return redirect('dashboard2')
            else:
                return redirect("login")

    return render(request, 'home.html')

def dashboard_view(request):
    # Check if the user is logged in
    username = request.session.get('username1')  # Retrieve username from session
    if username:
        return render(request, 'dashboard.html', {'username': username})
    else:
        return redirect('login') 

def dashboard1(request):
    # Check if the user is logged in
    username = request.session.get('username2')  # Retrieve username from session
    if username:
        return render(request, 'dashboard1.html', {'username': username})
    else:
        return redirect('login')  # Redirect to login if not logged in
    
def dashboard2(request):
    # Check if the user is logged in
    username = request.session.get('username3')  # Retrieve username from session
    if username:
        return render(request, 'dashboard2.html', {'username': username})
    else:
        return redirect('login') 

def logout_view(request):
    # Clear session data
    request.session.flush()
    return redirect('login')


from django.shortcuts import render, redirect
from .models import Student
from django.contrib import messages

def student_functions(request):
    context = {}

    if request.method == "POST":
        action = request.POST.get("action")

        # Add student
        if action == "add":
            try:
                Student.objects.create(
                    roll_no=request.POST.get("roll_no"),
                    name=request.POST.get("name"),
                    father_name=request.POST.get("father_name"),
                    email=request.POST.get("email"),
                    phone=request.POST.get("phone"),
                    gender=request.POST.get("gender"),
                    course=request.POST.get("course"),
                    birthday=request.POST.get("birthday"),
                    address=request.POST.get("address"),
                    city=request.POST.get("city"),
                    state=request.POST.get("state"),
                    state_code=request.POST.get("state_code"),
                    country=request.POST.get("coountry"),
                    date_of_joining=request.POST.get("date_of_joining"),
                    tenth_percent=request.POST.get("tenth_percent"),
                    twelfth_percent=request.POST.get("twelfth_percent"),
                )
                messages.success(request, "Student added successfully!")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")

        # View student
        elif action == "view":
            roll = request.POST.get("roll_no")
            try:
                student = Student.objects.get(roll_no=roll)
                context["student"] = student
            except Student.DoesNotExist:
                messages.error(request, "No student found with this roll number.")

        # Delete student
        elif action == "delete":
            roll = request.POST.get("roll_no")
            try:
                student = Student.objects.get(roll_no=roll)
                student.delete()
                messages.success(request, "Student deleted successfully.")
            except Student.DoesNotExist:
                messages.error(request, "Student not found.")

        # Alter student
        elif action == "alter":
            try:
                student = Student.objects.get(roll_no=request.POST.get("roll_no"))
                student.name = request.POST.get("name")
                student.father_name = request.POST.get("father_name")
                student.email = request.POST.get("email")
                student.phone = request.POST.get("phone")
                student.gender = request.POST.get("gender")
                student.course = request.POST.get("course")
                student.birthday = request.POST.get("birthday")
                student.address = request.POST.get("address")
                student.semester = request.POST.get("semester")
                student.year = request.POST.get("year")
                student.city = request.POST.get("city")
                student.state = request.POST.get("state")
                student.country = request.POST.get("country",'India')
                student.state_code = request.POST.get("state_code")
                student.date_of_joining = request.POST.get("date_of_joining")
                student.tenth_percent = request.POST.get("tenth_percent")
                student.twelfth_percent = request.POST.get("twelfth_percent")
                student.save()
                messages.success(request, "Student details updated.")
            except Student.DoesNotExist:
                messages.error(request, "Student not found.")

    return render(request, "student_page.html", context)



from django.shortcuts import render, redirect
from .form import FacultyForm
from .models import Faculty
from django.db import models

def add_faculty(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            max_id = Faculty.objects.aggregate(max_roll=models.Max('employee_id'))['max_roll']
            if max_id is None:
                max_id = 'GK20250'
            else:
                try:
                    max_id = str(max_id)
                except ValueError:
                    max_id = 'GK20250'
            faculty = form.save(commit=False)
            faculty.employee_id = max_id[0:6]+str(int(max_id[6])+1)
            faculty.save()
            return render(request, 'add_faculty.html', {
                'form': FacultyForm(),
                'success_message': '    Faculty added successfully!'
            })

        else:
            return render(request, 'add_faculty.html', {'form': form, 'error_message': form.errors})
    else:
        form = FacultyForm()
    return render(request, 'add_faculty.html', {'form':form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Faculty  # or from your_app.models import Faculty


def delete_faculty(request):
    employee_id = request.GET.get('employee_id')
    if employee_id:
        faculty = get_object_or_404(Faculty, employee_id=employee_id)
        return render(request, 'delete_faculty.html', {'faculty': faculty})
    return render(request, 'delete_faculty.html')


def confirm_delete_faculty(request, faculty_id):
    faculty = get_object_or_404(Faculty, pk=faculty_id)
    if request.method == 'POST':
        faculty.delete()
        messages.success(request, f'Faculty {faculty.name} deleted successfully!')
        return redirect('delete_faculty')
    return redirect('delete_faculty')

def view_faculty(request):
    faculty = None
    error_message = None
    if request.method == 'GET':
        id= request.GET.get('employee_id')
        try:
            faculty = Faculty.objects.get(employee_id=id)
        except Faculty.DoesNotExist:
            error_message = "No Faculty found with the provided Employee ID."
    return render(request, 'view_faculty.html', {'faculty': faculty, 'error_message': error_message})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db.models import Count
from datetime import datetime, date
from .models import Faculty, Attendance
from .form import AttendanceForm, DateSelectionForm, MonthYearForm

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_attendance(request):
    today = date.today()
    selected_date = today
    
    if request.method == 'POST' and 'date' in request.POST:
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['date']
    else:
        form = DateSelectionForm(initial={'date': today})
    
    faculties = Faculty.objects.all()
    attendance_data = []
    
    for faculty in faculties:
        attendance, created = Attendance.objects.get_or_create(
            faculty=faculty,
            date=selected_date,
            defaults={'status': 'absent'}  # Default status if creating new
        )
        attendance_data.append({
            'faculty': faculty,
            'attendance': attendance,
            'form': AttendanceForm(instance=attendance, prefix=str(faculty.id))
        })
    
    context = {
        'today': today,
        'selected_date': selected_date,
        'attendance_data': attendance_data,
        'date_form': form,
    }
    return render(request, 'admin_attendance.html', context)

@login_required
@user_passes_test(is_admin)
def save_attendance(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty_id')
        date_str = request.POST.get('date')
        status = request.POST.get('status')
        remarks = request.POST.get('remarks')
        
        try:
            faculty = Faculty.objects.get(id=faculty_id)
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            attendance, created = Attendance.objects.update_or_create(
                faculty=faculty,
                date=date_obj,
                defaults={'status': status, 'remarks': remarks}
            )
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def faculty_attendance(request):
    faculty = request.user.faculty
    today = date.today()
    month = today.month
    year = today.year
    
    if request.method == 'POST':
        form = MonthYearForm(request.POST)
        if form.is_valid():
            month = int(form.cleaned_data['month'])
            year = int(form.cleaned_data['year'])
    else:
        form = MonthYearForm(initial={'month': month, 'year': year})
    
    # Get attendance for the selected month/year
    attendance_records = Attendance.objects.filter(
        faculty=faculty,
        date__year=year,
        date__month=month
    ).order_by('-date')
    
    # Calculate summary counts
    summary = attendance_records.values('status').annotate(count=Count('status'))
    summary_dict = {item['status']: item['count'] for item in summary}
    
    context = {
        'faculty': faculty,
        'attendance_records': attendance_records,
        'form': form,
        'summary': {
            'present': summary_dict.get('present', 0),
            'absent': summary_dict.get('absent', 0),
            'leave': summary_dict.get('leave', 0),
            'late': summary_dict.get('late', 0),
        },
        'current_month': month,
        'current_year': year,
    }
    return render(request, 'faculty_attendance.html', context)