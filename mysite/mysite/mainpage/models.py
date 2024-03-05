from django.db import models
'''from mysite.mysite.mysite.setVenv import setVenv
application = setVenv("mysite.mysite.mysite.settings")'''

class kwHistory(models.Model):
    keyword = models.CharField(max_length=10)
    datetime = models.IntegerField()
    rank = models.FloatField()

class kwRank(models.Model):
    keyword = models.CharField(max_length=10)
    rank = models.FloatField()