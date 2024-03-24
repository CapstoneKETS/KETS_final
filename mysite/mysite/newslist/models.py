from django.db import models
from mainpage.models import newsData

class NewsListData(models.Model):
    newslistData = models.ForeignKey(newsData, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.newslistData)

