from django.contrib import admin
from django.urls import path, include
from newapp import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('student', views.StudentAPI, basename='student')
router.register('staff', views.StaffAPI, basename='staff')
router.register('department', views.DepartmentAPI, basename='department')
router.register('course', views.CourseAPI, basename='course')
router.register('position', views.PositionAPI, basename='position')
router.register('subject', views.subjectCreation, basename='subject')
router.register('labs', views.LabAPI, basename='labs')
router.register('lecture', views.lectureAPI, basename='lecture')
router.register('schedule', views.scheduleAPI, basename='schedule')
router.register('feeStructure', views.FeeStructureAPI, basename="feeStructure")
router.register(r'login', views.login, basename="login")
router.register(r'common', views.Common, basename="common")
router.register(r'dashboard', views.Dashboard, basename="dashboard")

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include(router.urls)),  # <-- DRF router URLs include karo
    # urls for Home
    path('home/', views.home, name='home'),
    path('feature/', views.feature, name='feature'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('courses/', views.course, name='courses'),
    path('enroll/', views.enroll, name='enroll'),
      
    # for other features
    path('Dashboard-Student/Fine-Management/', views.studentFine, name='studentFine'),
    path('Dashboard-Student/Notice-Management/', views.studentSendNotice, name='studentSendNotice'),
    path('Dashboard-Student/Notes-Management/', views.studentNotes, name='studentNotes'),
    path('Dashboard-Student/Chat-Management/', views.chatHistory, name='chatHistory'), 
    
# FOR STUDENT ASSIGNMENT 
    path('55061715190a454266024843041a0a6565430a010a30641b68464616063366101d59665a0b011833/', views.studentAssignment, name='studentAssignment'),
    path('Faculty/Dashboard/Student/Assignment/', views.faculty_student_assignment, name="faculty_student_assignment"),
    path('Dashboard-Student/Schedule-Management/', views.studentSchedule, name='studentSchedule'),
    path('Dashboard-Student/Result-Management/', views.studentResultView, name='studentResultView'),
        
]


from django.conf import settings
from django.conf.urls.static import static

# Sirf development mode me media serve karne ke liye
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)