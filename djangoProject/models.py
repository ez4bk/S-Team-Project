from django.db import models


class Children(models.Model):
    kids_name = models.CharField(max_length=128, db_column='kids_name')
    time_limit = models.IntegerField(max_length=11, db_column='time_limit')
    parent_id = models.CharField(max_length=320, db_column='parent_id')
    icon_image = models.CharField(max_length=128, db_column='icon_image')

    class Meta:
        db_table = 'kids'
        app_label = 'djangoProject'


class User(models.Model):
    user_name = models.CharField(max_length=128, unique=True, db_column='user_name')
    password = models.CharField(max_length=256, db_column='password')
    user_id = models.CharField(primary_key=True, unique=True, db_column='user_id')

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'parents'
        app_label = 'djangoProject'
