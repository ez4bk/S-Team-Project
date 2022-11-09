from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=128, unique=True, db_column='user_name')
    password = models.CharField(max_length=256, db_column='password')
    user_id = models.CharField(primary_key=True, unique=True, db_column='user_id')
    # c_time = models.DateTimeField(auto_now_add=True)
    Children = models.ForeignKey(Children, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'parents'
        app_label = 'djangoProject'

class Children(models.Model):
    kids_name = models.CharField(max_length=128, db_column='kids_name')
