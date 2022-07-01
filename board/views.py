from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from board.models import Board
from join.models import Member
from django.db.models import F

class ListView(View):
    def get(self, request):
        bdlist = Board.objects.select_related()

        context = {'bds': bdlist}
        return render(request, 'board/list.html', context)

    def post(self, request):
        pass


class ModifyView(View):
    def get(self, request):
        return render(request, 'board/modify.html')
    def post(self, request):
        pass


class ViewView(View):
    def get(self, request):
        form = request.GET.dict()

        # 조회수 증가
        Board.objects.filter(id=form['bno']).update(views=F('views') + 1)

        # select * from board join member
        # on b.member = m.id where where id = *
        bd = Board.objects.select_related().get(id=form['bno'])

        context = {'bd': bd}
        return render(request, 'board/view.html', context)


class WriteView(View):
    def get(self, request):
        return render(request, 'board/write.html')

    def post(self, request):
        pass


class RemoveView(View):
    def get(self, request):
        return render(request, 'board/remove.html')

    def post(self, request):
        pass


# board 테이블 데이터 초기화 (1000개)
class SetupView(View):
    def get(self, request):
        for i in range(350):
            # insert into board (title, Member, contents) value (*, *, *)
            b = Board( title = '워크크래프트 고블린',
                        member = Member.objects.get(id=1),   # abc123
                       contents='시간은 금이라구, 친구')
            b.save()

            b = Board( title = '스탠포드대 스티브 잡스',
                        member = Member.objects.get(id=2),   # 987xyz
                       contents='스테이 헝그리 스테이 풀리시')
            b.save()

            b = Board( title = '무명',
                        member = Member.objects.get(id=3),   # 4i5j6k
                       contents='만약, 당신이 실패했다면, 도전했다는 증거다')
            b.save()

        return redirect('/')