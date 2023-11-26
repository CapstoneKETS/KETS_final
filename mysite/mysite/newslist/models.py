from django.db import models
# django models의 class는 DB의 Table이 됩니다.

class NewsListData(models.Model):
    keyword = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    link = models.URLField()

    def __str__(self):
        return self.keyword

# Create your models here.
