from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Element(models.Model):

    id = models.CharField(
        primary_key=True,
        max_length=50,
        verbose_name='ID',
        blank=False
    )
  
    device_name = models.CharField(
        max_length=50,
        verbose_name='Device Name',
        blank=False
    )
    average_before_normalization = models.FloatField(
        verbose_name='Average Before Normalization',
        blank=False
    )
    average_after_normalization = models.FloatField(
        verbose_name='Average After Normalization',
        blank=False
    )

    data_size = models.IntegerField(
        verbose_name='Data Size',
        blank=False
    )

    raw_data = models.JSONField(null=False)
    
    def save(self,*args, **kwargs):
        super(Element, self).save(*args, **kwargs)

    def __str__(self):
        return self.device_name

    class Meta:
        verbose_name_plural = 'Elements'
        