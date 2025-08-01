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

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student,Faculty  # assuming Student model is imported

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_id=request.POST.get('userId')
        role = request.POST.get('role')
        
        if not username or not password or not role or not user_id:
            messages.error(request, "Please fill all the fields")
            return redirect('login')
        
        if role == 'admin':
            if username == "Deepanshu" and password == "12345" and user_id=='AD20250':
                request.session['username1'] = username
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid admin credentials")
                return redirect('login')
                
        elif role == 'faculty':
            try:
                faculty_email = Faculty.objects.all().values_list('email', flat=True)
                if username in faculty_email:
                    faculty_detail=Faculty.objects.get(email=username)
                    faculty_college_id=faculty_detail.college_id
                    faculty_phone=faculty_detail.phone
                    if password==faculty_phone and user_id == faculty_college_id:
                       request.session['username2'] =  faculty_detail.name
                       request.session['faculty_college_id']= faculty_college_id
                       request.session['role'] = role
                       return redirect('dashboard1')
                    else:
                       messages.error(request, "Invalid faculty credentials")
                       return redirect('login')
                else:
                    messages.error(request, "Invalid faculty credentials")
                    return redirect('login')
                    
            except Student.DoesNotExist:
                messages.error(request, "Faculty not found")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('login')
                
        elif role == 'student':
            try:
                student_emails = Student.objects.all().values_list('email', flat=True)
                if username in student_emails:
                    student_detail=Student.objects.get(email=username)
                    student_phone=student_detail.phone
                    student_college_id=student_detail.college_id
                    if password == student_phone and user_id == student_college_id:
                      request.session['username3'] = student_detail.name
                      request.session['student_college_id'] = student_college_id
                      request.session['role'] = role
                      return redirect('dashboard2')
                    else:
                      messages.error(request, "Invalid student credentials")
                      return redirect('login')
                else:
                    messages.error(request, "Invalid student credentials")
                    return redirect('login')
                    
            except Student.DoesNotExist:
                messages.error(request, "Student not found")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('login')
    
    return render(request, 'home.html')

# for forget password:
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Still needed for other potential AJAX requests
def forget_password(request):
    if request.method == 'GET':
        college_id = request.GET.get('collegeId')
        ID_str=str(college_id)
        try:
         if ID_str[0:2] == 'ST':
            student_detail = Student.objects.get(college_id=college_id)
            return JsonResponse({
                'success': True,
                'username': student_detail.username,
                'user_id': student_detail.user_id,
                'password': student_detail.password  # Make sure this field exists in your model
            })
         elif ID_str[0:2] == 'GK':
             faculty_detail = Faculty.objects.get(college_id=college_id)
             return JsonResponse({
                'success': True,
                'username': faculty_detail.username,
                'user_id': faculty_detail.user_id,
                'password': faculty_detail.password  # Make sure this field exists in your model
            })
        except (Student.DoesNotExist,Faculty.DoesNotExist):
            return JsonResponse({
                'success': False,
                'error': 'User not found'
            }, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


# for admin signup
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

def admin_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        if username == "Deepanshu" and password == "12345" and user_id =="AD20250":
            # Store admin authentication in session
            request.session['admin_authenticated'] = True
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid admin credentials'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


# for admin add page
def add_new_admin(request):
    # Check if admin is authenticated
    if not request.session.get('admin_authenticated'):
        return redirect('login')  # Or your login page
    
    # Render the add new admin page
    return render(request, 'admin_page.html')  # Create this template

# profile details
def profile_details(request):
    role = request.session.get('role')
    if role == 'faculty':
        faculty_id=request.session.get('faculty_college_id')
        details=Faculty.objects.get(college_id=faculty_id)
        return render(request,'profile.html',{'faculty':details})
    elif role == 'student':
        student_id=request.session.get('student_college_id')
        details=Student.objects.get(college_id=student_id)
        return render(request,'profile.html',{'student':details})

# for uploading picture 
def profile_upload(request):
    role = request.session.get('role')
    if role == 'student':
        try:
            student = Student.objects.get(college_id=request.session.get('student_college_id'))
        except Student.DoesNotExist:
            return redirect('dashboard2')
        
        if request.method == 'POST' and 'profile_picture' in request.FILES:
            student.profile_picture = request.FILES['profile_picture']
            student.save()
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('profile_details')
        
    elif role == 'faculty':
        try:
            faculty = Faculty.objects.get(college_id=request.session.get('faculty_college_id'))
        except Faculty.DoesNotExist:
            return redirect('dashboard1')
        
        if request.method == 'POST' and 'profile_picture' in request.FILES:
            faculty.profile_picture = request.FILES['profile_picture']
            faculty.save()
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('profile_details')
    
    # If none of the above conditions are met, redirect to appropriate dashboard
    return redirect('dashboard1' if role == 'faculty' else 'dashboard2')

# for id card
def id_card(request):
    role=request.session.get('role')
    context = {}
    
    try:
        # Check user type and add appropriate details to context
        if role == 'student':
            student = Student.objects.get(college_id=request.session.get('student_college_id'))
            context['detail'] = student
            context['user_type'] = 'Student'
        elif role == 'faculty':
            faculty = Faculty.objects.get(college_id=request.session.get('faculty_college_id'))
            context['detail'] = faculty
            context['user_type'] = 'Faculty'
            
    except (Student.DoesNotExist, Faculty.DoesNotExist):
        return redirect('logoutdoor')
    
    return render(request, 'id_card.html', context)

# for admin dashboard
def dashboard_view(request):
    # Check if the user is logged in
    username = request.session.get('username1')  # Retrieve username from session
    if username:
        return render(request, 'dashboard.html', {'username': username})
    else:
        return redirect('login') 

# for faculty dashboard
def dashboard1(request):
    # Check if the user is logged in
    username = request.session.get('username2')  # Retrieve username from session
    if username:
        return render(request, 'dashboard1.html', {'username': username})
    else:
        return redirect('login')  # Redirect to login if not logged in

# for student dashboard
def dashboard2(request):
    # Check if the user is logged in
    username = request.session.get('username3')  # Retrieve username from session
    if username:
        return render(request, 'dashboard2.html', {'username': username})
    else:
        return redirect('login') 

# for logout from account
def logout_view(request):
    # Clear session data
    request.session.flush()
    return redirect('login')

# for single students operations 
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
                max_id = Student.objects.aggregate(max_id=models.Max('college_id'))['max_id']
                
                if max_id is None:
                    college_id = 'ST20250'  # Initial ID
                else:
                    try:
                        # Extract numeric part and increment
                        numeric_part = int(max_id[2:])  # Remove 'GK' prefix
                        college_id = f'ST{numeric_part + 1}'
                    except (ValueError, IndexError):
                        college_id = 'ST20250'  # Fallback if format is wrong
                email=request.POST.get("email")
                phone=request.POST.get("phone")
                Student.objects.create(
                    college_id = college_id,
                    name=request.POST.get("name"),
                    father_name=request.POST.get("father_name"),
                    mother_name=request.POST.get('mother_name'),
                    occupation=request.POST.get('occupation'),
                    income=request.POST.get('income'),
                    email=email,
                    phone=phone,
                    other_phone_no=request.POST.get("other_phone_no"),
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
                    adhar_no=request.POST.get("adhar_no"),
                    pan_no=request.POST.get("pan_no"),
                    family_id=request.POST.get("family_id"),
                    family_id_phone_no=request.POST.get("family_id_phone_no"),
                    category=request.POST.get("category"),
                    nationality=request.POST.get("nationality"),
                    religion=request.POST.get("religion"),
                    martial_status=request.POST.get("martial_status"),
                    user_id=college_id, 
                    username=email,
                    password=phone,
                )
                messages.success(request, "Student added successfully!")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")

        # View student
        elif action == "view":
            college_id = request.POST.get("college_id")
            try:
                student = Student.objects.get(college_id=college_id)
                context["student"] = student
            except Student.DoesNotExist:
                messages.error(request, "No student found with this roll number.")

        # Delete student
        elif action == "delete":
            college_id = request.POST.get("college_id")
            try:
                student = Student.objects.get(college_id=college_id)
                student.delete()
                messages.success(request, "Student deleted successfully.")
            except Student.DoesNotExist:
                messages.error(request, "Student not found.")

        # Alter student
        elif action == "alter":
            try:
                student = Student.objects.get(college_id=request.POST.get("college_id"))
                student.name = request.POST.get("name")
                student.father_name = request.POST.get("father_name")
                student.mother_name = request.POST.get("mother_name")
                student.occupation = request.POST.get("occupation")
                student.income = request.POST.get("income")
                student.email = request.POST.get("email")
                student.phone = request.POST.get("phone")
                student.other_phone_no = request.POST.get("other_phone_no")
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
                student.save()
                messages.success(request, "Student details updated.")
            except Student.DoesNotExist:
                messages.error(request, "Student not found.")

    return render(request, "student_page.html", context)

#  for multiple student filtering
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Student, Course
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

def student_filter_page(request):
    try:
        # Get all courses from Course model (not from Student records)
        courses = Course.objects.all().values_list('name', flat=True)
        return render(request, 'student_filter.html', {'courses': courses})
    except Exception as e:
        messages.error(request, f"Error loading courses: {str(e)}")
        return render(request, 'student_filter.html', {'courses': []})

def get_course_details(request):
    try:
        course_name = request.GET.get('course_name')
        if not course_name:
            return JsonResponse({'error': 'Course name is required'}, status=400)
            
        course = Course.objects.get(name=course_name)
        return JsonResponse({
            'years': list(range(1, course.no_of_years + 1)),
            'semesters': list(range(1, course.no_of_semesters + 1))
        })
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def filter_students(request):
    filters = {
        'course': request.GET.get('course', 'all'),
        'year': request.GET.get('year', 'all'),
        'semester': request.GET.get('semester', 'all'),
        'roll_no': request.GET.get('roll_no', '')
    }

    students = Student.objects.all()
    
    if filters['course'] != 'all':
        students = students.filter(course=filters['course'])
    if filters['year'] != 'all':
        students = students.filter(year=filters['year'])
    if filters['semester'] != 'all':
        students = students.filter(semester=filters['semester'])
    if filters['roll_no']:
        students = students.filter(college_id__icontains=filters['college_id'])

    html = render_to_string('student_result_partial.html', {'students': students})
    return JsonResponse({'html': html})

@csrf_exempt
def bulk_update_students(request):
    if request.method == 'POST':
        student_ids = request.POST.getlist('student_ids[]')
        
        # Prepare update data - only include fields that have values
        update_data = {}
        fields_to_update = ['father_name',
            'course', 'year', 'semester', 
            'address', 'city', 'state', 'country'
        ]
        
        for field in fields_to_update:
            if request.POST.get(field):
                if field in ['year', 'semester']:
                    update_data[field] = int(request.POST.get(field))
                else:
                    update_data[field] = request.POST.get(field)
        
        if not update_data:
            return JsonResponse({'error': 'No fields to update'}, status=400)
            
        try:
            # Only update if we have both student IDs and data to update
            if student_ids and update_data:
                Student.objects.filter(id__in=student_ids).update(**update_data)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'No students selected or no data to update'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
@csrf_exempt
def delete_students(request):
    if request.method == 'POST':
        student_ids = request.POST.getlist('student_ids[]')
        try:
            Student.objects.filter(id__in=student_ids).delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

# for single faculty
from django.db import models
from django.contrib import messages
from django.shortcuts import render
from .models import Faculty 

def faculty_functions(request):
    context = {}

    if request.method == "POST":
        action = request.POST.get("action")

        # Add faculty
        if action == "add":
            try:
                # Auto-generate employee ID
                max_id = Faculty.objects.aggregate(max_id=models.Max('college_id'))['max_id']
                
                if max_id is None:
                    college_id = 'GK20250'  # Initial ID
                else:
                    try:
                        # Extract numeric part and increment
                        numeric_part = int(max_id[2:])  # Remove 'GK' prefix
                        college_id = f'GK{numeric_part + 1}'
                    except (ValueError, IndexError):
                        college_id = 'GK20250'  # Fallback if format is wrong
                email = request.POST.get("email")
                phone =  request.POST.get("phone")        
                # Create faculty with all required fields
                Faculty.objects.create(
                    college_id=college_id,
                    name=request.POST.get("name"),
                    father_name=request.POST.get("father_name"),
                    mother_name=request.POST.get("mother_name"),
                    email=email,
                    phone=phone,
                    other_phone_no=request.POST.get("other_phone_no"),
                    position=request.POST.get("position"),
                    gender=request.POST.get("gender"),
                    department=request.POST.get("department"),
                    qualification=request.POST.get("qualification"),
                    address=request.POST.get("address"),
                    city=request.POST.get("city"),
                    state=request.POST.get("state"),
                    state_code=request.POST.get("state_code"),
                    country=request.POST.get("country", "India"),
                    date_of_joining=request.POST.get("date_of_joining"),
                    experience=request.POST.get("experience"),
                    birthday=request.POST.get("birthday"),
                    category=request.POST.get("category"),
                    nationality=request.POST.get("nationality", "Indian"),
                    religion=request.POST.get("religion"),
                    adhar_no=request.POST.get("adhar_no"),
                    pan_no=request.POST.get("pan_no"),
                    martial_status=request.POST.get("martial_status"),
                    user_id=college_id, 
                    username=email,
                    password=phone,
                )
                messages.success(request, "Faculty added successfully!")
            except Exception as e:
                messages.error(request, f"Error adding faculty: {str(e)}")

        # View faculty
        elif action == "view":
            college_id = request.POST.get("college_id")
            try:
                faculty = Faculty.objects.get(college_id=college_id)
                context["faculty"] = faculty
            except Faculty.DoesNotExist:
                messages.error(request, "No faculty found with this ID.")
            except Exception as e:
                messages.error(request, f"Error viewing faculty: {str(e)}")

        # Delete faculty
        elif action == "delete":
            college_id = request.POST.get("college_id")
            try:
                faculty = Faculty.objects.get(college_id=college_id)
                faculty.delete()
                messages.success(request, "Faculty deleted successfully.")
            except Faculty.DoesNotExist:
                messages.error(request, "Faculty not found.")
            except Exception as e:
                messages.error(request, f"Error deleting faculty: {str(e)}")

        # Alter faculty
        elif action == "alter":
            college_id = request.POST.get("college_id")
            try:
                faculty = Faculty.objects.get(college_id=college_id)
                
                # Update all fields
                faculty.name = request.POST.get("name")
                faculty.father_name = request.POST.get("father_name")
                faculty.mother_name = request.POST.get("mother_name")
                faculty.email = request.POST.get("email")
                faculty.phone = request.POST.get("phone")
                faculty.other_phone_no = request.POST.get("other_phone_no")
                faculty.position = request.POST.get("position")
                faculty.gender = request.POST.get("gender")
                faculty.department = request.POST.get("department")
                faculty.qualification = request.POST.get("qualification")
                faculty.address = request.POST.get("address")
                faculty.city = request.POST.get("city")
                faculty.state = request.POST.get("state")
                faculty.state_code = request.POST.get("state_code")
                faculty.country = request.POST.get("country", "India")
                faculty.date_of_joining = request.POST.get("date_of_joining")
                faculty.experience = request.POST.get("experience")
                faculty.birthday = request.POST.get("birthday")
                faculty.adhar_no = request.POST.get("adhar_no")
                faculty.pan_no = request.POST.get("pan_no")
                faculty.martial_status = request.POST.get("martial_status")
                
                faculty.save()
                messages.success(request, "Faculty details updated successfully.")
            except Faculty.DoesNotExist:
                messages.error(request, "Faculty not found.")
            except Exception as e:
                messages.error(request, f"Error updating faculty: {str(e)}")

    return render(request, "faculty_page.html", context)