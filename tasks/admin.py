from django.contrib import admin
from tasks.models import UserAccount , UserTasks
# Register your models here.
admin.site.register(UserAccount)
admin.site.register(UserTasks)