from django.db import models

# Create your models here.
class UserAccount(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField()

    def __str__(self):
        return self.name
    

    
class UserTasks(models.Model):
    account = models.ForeignKey(UserAccount , on_delete=models.CASCADE)
    todos = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.account.email} - Task"