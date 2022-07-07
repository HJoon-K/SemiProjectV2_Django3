import json
import os
from datetime import datetime
from math import ceil
from uuid import uuid4

from django.core.paginator import Paginator
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.encoding import escape_uri_path
from django.views import View

from board.models import Board
from join.models import Member
from pds.models import Pds


class ListView(View):
    def get(self, request):
        pdslist = Pds.objects.select_related()

        context = {'pds': pdslist}
        return render(request, 'pds/list.html', context)

    def post(self, request):
        pass


class ModifyView(View):
    def get(self, request):
        return render(request, 'pds/modify.html')

    def post(self, request):
        pass


class ViewView(View):
    def get(self, request):
        form = request.GET.dict()
        p = Pds.objects.select_related().get(id=form['pno'])

        #  문자열 형태로 저장되어 있는 fnames를
        # json의 loads함수로 원래의 자료형으로 되돌림
        # 또한 template으로 보낼 값이 여러개인 경우
        # zip 함수로 묶어서 넘기면 편함
        context = {'p': p, 'finfo': zip(json.loads(p.fnames),range(5),
                                        json.loads(p.fsizes), json.loads(p.fdowns))}
        return render(request, 'pds/view.html', context)

    def post(self, request):
        pass


def process_upload_files(fnames, uuid1):
    fpath = 'C:/Java/pdsupload/'     #첨부파일 저장위치
    names = [None, None, None, None, None]
    sizes = [None, None, None, None, None]

    for ix, f in enumerate(fnames):     # fnames에서 값(첨부파일)과 순번 처리
        names[ix] = f.name  # 첨부파일명을 순서에 따라 리스트에 저장

        # 업로드시 원본파일명 : abc123.txt
        # 업로드완료시 최종파일명 : 20220706094640abc123.txt
        # 지정한 위치에 저장시 전체파일명 : c:/Java/pdsupload/20220706094640abc123.txt
        fname = fpath + uuid1 + f.name
        with open(fname, 'wb+') as dest:    # 지정한 파일을 바이너리 형식으로 오픈
            for chunk in f.chunks():    # 파일을 일정한 크기의 조각으로 나눔
                dest.write(chunk)
        # 업로드된 파일의 용량을 알아내 size에 저장(단위는 KB)
        fsize = os.path.getsize(fname)

        # sizes[ix] = fsize #(단위는 B)
        sizes[ix] = f'{fsize/1024:,.1f}'  #(비로소 단위는 KB)
    return names, sizes


class WriteView(View):
    def get(self, request):
        userid = request.session.get('userinfo').split('|')[0]

        context = {'userid': userid}
        return render(request, 'pds/write.html', context)

    def post(self, request):
        form = request.POST.dict()      # 폼에서 텍스트데이터를 가져옴
        fnames = request.FILES.getlist('fname')     # 폼에서 파일데이터들을 가져옴
        uuid1 = datetime.now().strftime('%Y%m%d%H%M%S')
        # uuid2 = uuid4().hex     # 유니크한 문자열 생성 (16진수)

        print(form)
        print(fnames)
        print(uuid1)
        # print(uuid2)

        # 임시폴더에 저장된 업로드 파일들을 지정한 위치에 저장
        # 단, 파일 저장시 'uuid + 파일명' 형식 사용
        fnames, fsizes = process_upload_files(fnames, uuid1)

        p = Pds(title=form['title'], contents=form['contents'],
                member=Member.objects.get(userid=form['userid']),
                fnames=json.dumps(fnames),
                fsizes=json.dumps(fsizes),
                fdowns=json.dumps([0,0,0,0,0]),
                uuid=uuid1)
        p.save()

        return redirect('/pds/list')

class RemoveView(View):
    # 첨부파일 삭제시 글작성자와 로그인 사용자 일치여부 검사
    # Django가 지원하지 않는 템플릿 필터를 사용하려면 사용자 정의 템플릿 필터를 작성해야 함
    # 1. 필터/태그를 작성할 앱이 있는 디렉토리에서
    #   templatetags라는 폴더 생성
    # 2. 필터/태그의 기능을 수행하는 소스(.py) 작성
    # 3. 필터/태그의 기능을 실행하려는 html 소스상에서
    # {% load 필터명 %} 이라는 코드를 작성함
    # 4. 서버를 재시작해야 필터/태그 사용가능함
    # https://docs.djangoproject.com/ko/3.2/howto/custom-template-tags/

    def get(self, request):
        form = request.GET.dict()

        # 게시글 알아냄
        p = Pds.objects.get(id=form['pno'])


        # 첨부파일 삭제
        fpath = 'c:/Java/pdsupload/' + p.uuid   # 삭제할 파일의 경로 정의

        #
        if request.session.get('userinfo').split('|')[0] ==  p.member.userid:
            for fn in json.loads(p.fnames):
                if fn:
                    rmvOne = fpath + fn
                    os.remove(rmvOne)   # 지정한 경로상의 파일 삭제

        # 테이블상의 게시글 삭제
        Pds.objects.filter(id=form['pno']).delete()

        return redirect('/pds/list')


class PdownView(View):
    def get(self, request):
        fpath ='C:/Java/pdsupload/'
        form = request.GET.dict()

        # pno를 이용해서 다운로드할 파일이 있는 게시글을 알아냄
        p = Pds.objects.get(id=form['pno'])

        # 다운로드할 파일명을 알아냄
        odr = int(form['odr'])
        fname = json.loads(p.fnames)[odr]

        # 다운로드할 파일의 실제 경로 생성
        fpath = fpath + p.uuid + fname
        print(fpath)

        # 다운수 증가
        # 다운수를 수정하기 위해 다운수를 역직렬화해서 가져옴
        fdowns = json.loads(p.fdowns)
        fdowns[odr] = fdowns[odr] + 1

        # 수정된 다운수는 다시 직렬화해서 테이블에 저장
        Pds.objects.filter(id=form['pno']).update(fdowns=json.dumps(fdowns))

        # 실제 경로상의 파일을 바이너리 형식으로 읽어서
        # 클라이언트로 전송
        with open(fpath, 'rb+') as f:
            # 클라이언트로 전송할 파일의 종류(MIME TYPE)를 unknown으로 설정
            # ==> 브라우저 처리하지 않고 바로 다운로드하도록 처리
            # 이미지 : image/png, image/jpeg, image/gif
            # html  : text/html
            # 멀티미디어 : video/mp4, audio/mp3
            response = HttpResponse(f.read(), content_type='application/unknown')

            response['Content-Disposition'] = f'attachment; filename={escape_uri_path(fname)}'

        return response