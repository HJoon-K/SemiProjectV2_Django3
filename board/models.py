from datetime import datetime

from django.db import models

# Create your models here.

from join.models import Member


class Board(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    member = models.ForeignKey(Member, on_delete=models.DO_NOTHING)
    regdate = models.DateTimeField(default=datetime.now)
    thumbup = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    contents = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'board'
        ordering = ['-id']