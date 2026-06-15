from django.urls import path
from JobPortal.views import *

urlpatterns = [
    path('register-page/', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),

    path('', dashboard_page, name='dashboard_page'),
    path('profile-view/', profile_view, name='profile_view'),
    path('update-profile-view/', update_profile_view, name='update_profile_view'),

    path('browse-job/', browse_job, name='browse_job'),
    path('job-detail/<str:id>/', job_detail_view, name='job_detail_view'),
    path('post-job-view/', post_job_view, name='post_job_view'),
    path('update-post-job-view/<str:id>/' , update_post_job_view, name= 'update_post_job_view'),
    path('delete-post-job-view/<str:id>/' , delete_post_job_view, name= 'delete_post_job_view'),

    path('apply-job/<str:id>/',apply_job_view,name='apply_job_view'),
    path('my-application/',my_application,name='my_application'),
    

    path('candidate-list/<str:id>/',candidate_list_view,name='candidate_list_view'),
    ]
