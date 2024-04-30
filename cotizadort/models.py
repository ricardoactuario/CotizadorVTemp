from django.db import models

# Create your models here.

class TR1(models.Model):
    Age = models.IntegerField()
    t10 = models.DecimalField(max_digits=30, decimal_places=25)
    t15 = models.DecimalField(max_digits=30, decimal_places=25)
    t20 = models.DecimalField(max_digits=30, decimal_places=25)
    t25 = models.DecimalField(max_digits=30, decimal_places=25)
    t30 = models.DecimalField(max_digits=30, decimal_places=25)
    