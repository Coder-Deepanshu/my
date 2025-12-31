from django.contrib import admin
from django.urls import path
from newapp import views
from django.conf import settings
from django.conf.urls.static import static
# from .views import ProductListView, ProductDetailView

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
    path('login/', views.login_view, name='login'),
    path('verify_collegeID/', views.verify_collegeID, name='verify_collegeID'),
    path('verify_otp/', views.verify_otp_view, name='verify_otp'),
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
    path('submitFee/', views.submitFee, name= 'submitFee'),
  
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
    
    # for other features
    path('Dashboard-Student/Fine-Management/', views.studentFine, name='studentFine'),
    path('Dashboard-Student/Notice-Management/', views.studentSendNotice, name='studentSendNotice'),
    path('Dashboard-Student/Notes-Management/', views.studentNotes, name='studentNotes'),
    path('Dashboard-Student/Chat-Management/', views.chatHistory, name='chatHistory'), 
    path('Dashboard-Student/Course-Management/', views.studentCourseDetailView, name='studentCourseDetailView'), 
    path('Dashboard-Student/Assignment-Management/', views.studentAssignment, name='studentAssignment'),
    path('Dashboard-Student/Schedule-Management/', views.studentSchedule, name='studentSchedule'),
    path('Dashboard-Student/Result-Management/', views.studentResultView, name='studentResultView'),
    
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
    

   
    path('demo2/', views.demo2, name='demo2'),
    # for bulk Management
    # 1}..For students
    path('semester&year/',views.semester_and_year,name='semester_and_year'),
    path('SelectedEditData/', views.SelectedEditData, name='SelectedEditData'),
    path('EditSelectedSubmit/', views.EditSelectedSubmit, name='EditSelectedSubmit'),
    path('Dashboard/Admin/BulkManagement/Students/',views.BulkStudentManagement, name='bulkStudentManagement'),

    # for subject creation
    path('Dashboard/Admin/Subject/Creations/', views.subjectCreation, name='subjectCreation'),
    # for content Creation
    path('Dashboard/Admin/Subject/Content/Creations/', views.contentCreation, name='contentCreation'),
    path('SubjectFilter/',views.subjectFilter,name='subjectFilter'),

    path('Hi/', views.friendship_proposal, name='friendship_proposal'),
    path('save-decision/', views.save_decision, name='save_decision'),
    path('save-contact-decision/', views.save_contact_decision, name='save_contact_decision'),
    path('save-contact/', views.save_contact, name='save_contact'),

    # For Faculty and Admin Management System:
    path("0e170d030d451e46590d131d1e111b4e621c1a061505170e661d460d13451e1d0244621c0700181f16074b4266", lambda request : views.check_wifi_ip(request,"Faculty"), name="check_wifi"),
    path('1117171e150c6b0b45001c18141a0a4e4f61490b0d1c010c59630a071c18521a0665456149160b111b0d484a4130/', views.college_pin_checking, name='college_pin_checking'),
    path('06161632061e1e65410001450900034d5a4105661d1e154968646707134514060e67596410131d/', views.scan_qr_Code, name='scan_qr_Code'),
    
    # Admin views (optional)
    path('view-proposals/', views.view_proposals, name='view_proposals'),
    path('proposal/<int:proposal_id>/', views.proposal_detail, name='proposal_detail'),

    path('Birthday/', views.upload_photo, name='upload_photo'),
    path('display/', views.display_greeting, name='display_greeting'),

    path('0615180043014744650f/', views.login1, name='login1'),
    path('0c06161804584442650f1c0e1f10/', views.download_photo, name='download_photo'),

]


from django.conf import settings
from django.conf.urls.static import static

# Sirf development mode me media serve karne ke liye
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)