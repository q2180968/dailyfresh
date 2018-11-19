from django.db import models


# Create your models here.
class userinfo(models.Model):
    uname = models.CharField(max_length=32)
    upwd = models.CharField(max_length=50)
    uemail = models.CharField(max_length=50)
    urecvName = models.CharField(max_length=32, default='')
    uaddress = models.CharField(max_length=50, default='')
    upostid = models.CharField(max_length=7, default='')
    utelphone = models.CharField(max_length=11, default='')

    class Meta():
        db_table = 'userinfo'

    def __str__(self):
        return self.uname
