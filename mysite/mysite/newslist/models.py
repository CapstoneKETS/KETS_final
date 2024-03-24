from django.db import models
# django models의 class는 DB의 Table이 됩니다.
from mainpage.models import newsData

class newsList(models.Model):
    newsData = models.ForeignKey(newsData, on_delete=models.CASCADE)

    def __str__(self):
        return self.keyword

# Create your models here.
