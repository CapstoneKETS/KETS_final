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

class newsData(models.Model):
    title = models.CharField(max_length=50)
    reporter = models.CharField(max_length=10)
    company = models.CharField(max_length=10)
    datetime = models.CharField(max_length=10)
    summary = models.TextField(default=' ')
    url = models.URLField(null=True)
    keywords = models.CharField(max_length=100, null=True)