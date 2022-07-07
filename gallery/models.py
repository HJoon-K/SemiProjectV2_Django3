from datetime import datetime
from django.db import models

# Create your models here.
from join.models import Member


class Gallery(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    member = models.ForeignKey(Member, on_delete=models.DO_NOTHING)
    regdate = models.DateTimeField(default=datetime.now)
    thumbup = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    contents = models.TextField(null=False, blank=False)
    uuid = models.CharField(max_length=15, default='')      # 년월일시분초: 20220705130353
    fnames = models.CharField(max_length=256, null=True)    # 각 파일명은 리스트로 저장
    fsizes = models.CharField(max_length=256, null=True)    # 각 파일명은 리스트로 저장


    class Meta:
        db_table = 'gallery'
        ordering = ['-id']