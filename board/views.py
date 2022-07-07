from math import ceil
from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from board.models import Board, Comment
from join.models import Member
from django.db.models import F

class ListView(View):
    def get(self, request, perPage=25):
        form = request.GET.dict()
        qry = ''

        # 검색유형이 제목, 작성자, 본문이라면면
        if request.GET.get('fkey') is not None and request.GET.get('ftype') is not None:
            if form['ftype'] == 'title':
                bdlist = Board.objects.select_related().filter(title=form['fkey'])
            elif form['ftype'] == 'userid':
                bdlist = Board.objects.select_related().filter(member__userid=form['fkey'])
            elif form['ftype'] == 'contents':
                bdlist = Board.objects.select_related().filter(contents__contains=form['fkey'])

            # get으로 전송죈 키와 값을 인코딩해서 질의문자열로 변환
            qry = urlencode({'ftype': form['ftype'], 'fkey': form['fkey']})
            # print(qry)
        else:
            # 검색어와 검색대상이 없는 경우
            bdlist = Board.objects.select_related()


        # 페이징 기타처리
        # 총페이지수 = 전체게시물수 /페이지당 게시물수
        pages = ceil(bdlist.count() / perPage)

        # 페이징 처리 1
        # paginator = Paginator(객체, 분할갯수)
        # 전체 Board 데이터를 페이지당 25개씩 나눠 페이별로 저장
        # paginator = Paginator(bdlist, perPage)
        # paginator = Paginator(bdlist, per_page=25)
        #
        # # 질의문자열 중 cpage가 존재한다면
        # if request.GET.get('cpage') is not None:
        #     # cpage를 이용해서 해당 페이지의 데이터를 가져옴
        #     bdlist = paginator.get_page(form['cpage'])
        # else:
        #     bdlist = paginator.get_page(1)

        # 페이징 처리 2
        # select id, title, userid, regdate, views from board
        # limit ?, 25
        # 1page : limit 0, 25 (시작위치, 가져올 갯수)
        # 2page : limit 25, 25
        # 3page : limit 50, 25
        # Npage : limit 25(n-1), 25
        # 식 : 25 * (n -1)
        cpage = 1
        if request.GET.get('cpage') is not None: cpage = form['cpage']

        start = (int(cpage) - 1) * perPage
        end = start + perPage
        bdlist = bdlist[start:end]

        # cpage 1: 1 2 3 4 5 6 7 8 9 10
        # cpage 10: 1 2 3 4 5 6 7 8 9 10
        # cpage 11: 11 12 13 14 15 16 17 18 19 20
        # cpage 20: 11 12 13 14 15 16 17 18 19 20
        stpgn = int((int(cpage) - 1) / 10) * 10 + 1

        context = {'bds': bdlist, 'pages': pages, 'range': range(stpgn, stpgn+10), 'qry': qry}
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

        # select * from comment join board join member
        # where borad = 본문글번호 order by cno
        cmt = Comment.objects.select_related().filter(board__id=form['bno']).order_by('cno', 'id')

        lgnusr = ''
        if request.session.get('userinfo') is not None:
            lgnusr = request.session['userinfo'].split('|')[0]

        context = {'bd': bd, 'cmt': cmt, 'lgnusr': lgnusr}
        # print(cmt['regdate'])
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


class CmntView(View):
    def post(self, request):
        form = request.POST.dict()

        # 댓글의 가장 최근 id값을 알아냄
        id = Comment.objects.latest('id').id

        c = Comment(cno=id+1,
                    board=Board.objects.get(id=form['bno']),
                    member=Member.objects.get(userid=form['userid']),
                    comments=form['comments'])
        c.save()

        return redirect('/board/view?bno=' + form['bno'])