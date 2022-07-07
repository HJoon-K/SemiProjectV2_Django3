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


# 댓글 : reply
# 답글 : comment
class Comment(models.Model):
    id = models.AutoField(primary_key=True)  # 댓글 고유번호
    cno = models.IntegerField()             # 답글 고유번호
    board = models.ForeignKey(Board, on_delete=models.DO_NOTHING) # 본문글 번호
    member = models.ForeignKey(Member, on_delete=models.DO_NOTHING) # 작성자 번호
    comments = models.TextField()
    regdate = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'comment'
        ordering = ['cno']
