from django.db import models

class PostOffice(models.Model):
    ma_buu_cuc = models.CharField(max_length=255, null=True, blank=True)
    khu = models.CharField(max_length=255, null=True, blank=True)
    pic = models.CharField(max_length=255, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'post_offices'
