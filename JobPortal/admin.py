from django.contrib import admin
from JobPortal.models import *

admin.site.register([
    User,
    RecruiterProfileModel,
    SeekerProfileModel,
    JobPostModel,
    CategoryModel,
    ApplyJobModel,
    
])

