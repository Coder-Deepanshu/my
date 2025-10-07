from django.contrib import admin
from django.urls import path
from newapp import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (
   
    DepartmentUpdateView, DepartmentDeleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # urls for Home
    path('', views.home, name='home'),
    path('Feature/', views.feature, name='feature'),
    path('Success-Stories/', views.success_stories, name='success_stories'),
    path('Contact-Details/', views.contact, name='contact'),
    path('Course-Details/', views.pricing, name='pricing'),
    path('Demo-Book/', views.demo, name='demo'),
    path('Enroll/', views.enroll, name='enroll'),
    path('Home/Enroll/', views.new_enroll, name='new_enroll'),
    path('Home/Login-In/', views.login_view, name='login'),
    path('Log-Out/', views.logout_view, name='logoutdoor'),

    # urls for dashboards
    path('Admin/Dashboard/', views.dashboard_view, name='dashboard'),
    path('Faculty/Dashboard/', views.dashboard1, name='dashboard1'),
    path('Student/Dashboard/', views.dashboard2, name='dashboard2'), 

    # urls for student/faculty/admin functions
    path("Dashboard-Admin/Student-Management/", views.student_functions, name="student_function"),
    path("Dashboard-Admin/Faculty-Management/", views.faculty_functions, name="faculty_functions"),
    path("Dashboard-SuperAdmin/Admin-Management/", views.admin_functions, name="admin_functions"),

    # urls for Main
    path("Dashboard/Profile/", views.profile_details, name="profile_details"),
    path('profile_upload/', views.profile_upload, name='profile_upload'),# for profile upload in profile
    path("Dashboard/ID-Card", views.id_card, name="id_card"),
    path('Login-In/Forgot-Password/', views.forget_password, name='forgot_password'),

    # for id card
    path('admin-adding-page/', views.admin_adding_page, name='admin_adding_page'),
    path('admin-card/', views.admin_card, name='admin_card'),
    
    # for attendance management 
    # # # for student attendance management
    path('save_attendance/', views.save_attendance, name='save_attendance'),
    path('Dashboard-Student/Attendance-Management/', views.student_attendance_view, name='student_attendance_view'),
    path('get-student-attendance/', views.get_student_attendance, name='get_student_attendance'),
    
    # Fee Management URLs
    path('Student-Dashboard/Fee-Managment/<str:college_id>/<str:number>/', views.student_fees_view, name='student_fees_view'),
    path('Admin-Dashboard/Student/Fee-Payment/',views.feePayment, name='feePayment'),
    path('Admin-Dashboard/Student/Fee-Detail/<str:college_id>/<str:number>/',views.student_fees_view, name='feeDetail'),
    path('payNow/', views.payNow, name='payNow'),
  
# for chatting management between faculty and student
    path('chat_home/', views.chat_home, name='chat_home'),
    path('create_chat_room/', views.create_chat_room, name='create_chat_room'),

    # for send message and gwt messages
    path('send_message/', views.send_message, name='send_message'),
    path('get_messages/<int:room_id>/', views.get_messages, name='get_messages'),
    # for sending info about faculty
    path('Student/Dashboard/Chat-Faculty', views.get_faculty_details, name='get_faculty_details'),
    path('faculty_filtering/', views.faculty_filtering, name='faculty_filtering'),
    path('toggle_follow/', views.toggle_follow, name='toggle_follow'),
    # for sending info about student
    path('faculty/students/', views.faculty_student_list, name='faculty_student_list'),
    path('delete_chat/<int:room_id>/', views.delete_chat, name='delete_chat'),

# for creating department/positions/courses
    path('Admin-Dashboard/Department-Creation/',views.department_creation,name='department_creation'),
    path('Admin-Dashboard/Course-Creation/',views.course_creation,name='course_creation'),
    path('Admin-Dashboard/Staff-Positions-Creation/',views.position_creation,name='position_creation'),
    path('Send-Batch/', views.sendBatch, name='sendBatch'),
    path('Create-Fees-Structure/',views.createFeeStructure, name='createFeeStructure'),
    path('Fetch-Filter-Batch/',views.fetchBatch, name='fetchBatch'),
    path('Delete-Structure/<str:structure_id>/',views.deleteStructure, name='deleteStructure'),

    
# for getting student details on faculty/admin/studentportal 
    path('Faculty-Dashboard/Student-Attendance-Management/',lambda request: views.course_details(request,"faculty_filtering.html"),name='studentAttendance_management'),
    path('Faculty-Dashboard/Faculty-Student-Chat/',lambda request: views.course_details(request,"chat/page2.html"),name='facultyStudent_chat'),
   
    path('Admin-Dashboard/Student-Fee-Structure-Management',lambda request: views.course_details(request,"feeStructureCreation.html"),name='studentFeeStructureManagement'),
    path('get-courses-details/', views.get_courses_details, name='getCourseDetails'),
    path('Faculty-Dashboard/Filtered-Student-Attendance-Management', lambda request: views.filtered_students(request, "student/student_table.html"), name='filteredStudents'),
    path('Faculty-Dashboard/Filtered-Student-Chat-Management', lambda request: views.filtered_students(request, "chat/student_list_partial.html"), name='filteredFollowedStudents'),

# for Bulk Actions
    # for student bulk management
    path('Admin-Dashboard/Student-Bulk-Management',lambda request: views.course_details(request,"bulkActions/student/studentActions.html"),name='studentBulkManagement'),
    path('Dashboard-Admin/BulkAction-Student-Management',lambda request : views.filtered_students(request,"bulkActions/student/studentFilterResult.html"), name='bulkStudentFiltering'),
    path('get-student-details/', views.get_student_details, name='get_student_details'),
    path('update-student/', views.update_student, name='update_student'),
    path('bulk-update-students/', views.bulk_update_students, name='bulk_update_students'),
    path('delete-student/', views.delete_student, name='delete_student'),
    path('bulk-delete-students/', views.bulk_delete_students, name='bulk_delete_students'),
    path('export-students/', views.export_students, name='export_students'),
    
    # for other features
    path('Dashboard-Student/Fine-Management/', views.studentFine, name='studentFine'),
    path('Dashboard-Student/Notice-Management/', views.studentSendNotice, name='studentSendNotice'),
    path('Dashboard-Student/Notes-Management/', views.studentNotes, name='studentNotes'),
    path('Dashboard-Student/Chat-Management/', views.chatHistory, name='chatHistory'), 
    
    # for history feature
    path('Dashboard-Admin/Student-History-Management', lambda request : views.historySender(request,"Student"), name='studentHistoryManagement'),
    path('Dashboard-Admin/Faculty-History-Management', lambda request : views.historySender(request,"Faculty"), name='facultyHistoryManagement'),
    path('Dashboard-Admin/Admin-History-Management', lambda request : views.historySender(request,"Admin"), name='adminHistoryManagement'),
    path('Get-Details/<str:college_id>/',views.get_updatedToDetails,name="get_updatedToDetails"),
    path('Get-History/<str:college_id>/',views.getHistory,name="getHistory"),
    path('Delete-History/<str:college_id>/',views.deleteHistory,name="deleteHistory"),
    
    # for document uploading feature
    path('Dashboard-Student/Document-Management', lambda request : views.document(request,"Student"), name='studentDocumentManagement'),
    path('Dashboard-Faculty/Document-Management', lambda request : views.document(request,"Faculty"), name='facultyDocumentManagement'),
    path('Dashboard-Admin/Document-Management', lambda request : views.document(request,"Admin"), name='adminDocumentManagement'),
    path('Dashboard-Admin/Get-Documents/', views.getDocuments, name='getDocuments'),
    path('Dashboard-Admin/View-Documents/<str:college_id>/<str:documentid>/',views.viewDocuments,name='viewDocuments'),
    

 
    
    
    # ajax practise urls
    path("get-data1/", views.get_data_fetch, name="get_fetch"),
    path("students/", views.students_list, name="students_list"),
    path("students/<int:roll_no>/", views.student_detail, name="student_detail"),
    path("students/delete_bulk/", views.delete_students, name="delete_students"),
]


from django.conf import settings
from django.conf.urls.static import static

# Sirf development mode me media serve karne ke liye
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)