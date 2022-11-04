from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=128, unique=True, db_column='user_name')
    password = models.CharField(max_length=256, db_column='password')
    user_id = models.CharField(primary_key=True, unique=True, db_column='user_id')
    # c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'parents'
        app_label = 'djangoProject'

