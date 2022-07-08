import json
import os
from datetime import datetime
from math import ceil
from uuid import uuid4

# pip install pillow
from PIL import Image

from django.core.paginator import Paginator
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.encoding import escape_uri_path
from django.views import View

from board.models import Board
from gallery.models import Gallery
from join.models import Member
from pds.models import Pds


class ListView(View):
    def get(self, request):
        galist = Gallery.objects.select_related()

        context = {'gal': galist, 'fimg': 'gendo.png'}
        return render(request, 'gallery/list.html', context)

    def post(self, request):
        pass


class ModifyView(View):
    def get(self, request):
        return render(request, 'pgallery/modify.html')

    def post(self, request):
        pass


class ViewView(View):
    def get(self, request):
        form = request.GET.dict()
        g = Gallery.objects.select_related().get(id=form['gno'])

        # 본문보기 처리시 본문내용과, 첨부한 이미지파일 정보를 넘김
        ginfo = json.loads(g.fnames)
        ginfo2 = zip(json.loads(g.fnames), json.loads(g.fsizes))
        context = {'g': g, 'ginfo': ginfo, 'ginfo2': ginfo2}
        return render(request, 'gallery/view.html', context)

    def post(self, request):
        pass


def process_image_files(fname, uuid, fpath):
    # 업로드된 생성할 이미지를 불러옴
    img = Image.open(fpath+uuid+fname)
    print(img.width, img.height)

    # 이미지 크기를 3등분해서 각 죄표 계산
    startx = int(img.width / 3)
    starty = int(img.height / 3)
    x1 = startx
    y1 = starty
    x2 = startx * 2
    y2 = starty * 2

    # 지정한 영역으로 이미지를 잘라냄
    # crop(시작x, 시작y, 끝x, 끝y)
    cropimg = img.crop((x1, y1, x2, y2))

    # 크롭한 이미지를 적당한 크기로 재조정
    resizeimg = cropimg.resize((350, 350))

    # 잘라낸 크롭 이미지를 저장함
    resizeimg.save(fpath+'thumbs/'+uuid+fname)


def process_upload_files(fnames, uuid):
    fpath = 'C:/Java/galupload/'     #첨부파일 저장위치
    names = [None, None, None, None, None]
    sizes = [None, None, None, None, None]

    for ix, f in enumerate(fnames):     # fnames에서 값(첨부파일)과 순번 처리
        names[ix] = f.name  # 첨부파일명을 순서에 따라 리스트에 저장

        fname = fpath + uuid + f.name
        with open(fname, 'wb+') as dest:    # 지정한 파일을 바이너리 형식으로 오픈
            for chunk in f.chunks():    # 파일을 일정한 크기의 조각으로 나눔
                dest.write(chunk)
        # 업로드된 파일의 용량을 알아내 size에 저장(단위는 KB)
        fsize = os.path.getsize(fname)

        # sizes[ix] = fsize #(단위는 B)
        sizes[ix] = f'{fsize/1024:,.1f}'  #(비로소 단위는 KB)
        
    # 업로드된 첫번째 이미지의 썸네일 생성
    process_image_files(names[0], uuid, fpath)
    return names, sizes


class WriteView(View):
    def get(self, request):
        userid = request.session.get('userinfo').split('|')[0]

        context = {'userid': userid}
        return render(request, 'gallery/write.html', context)

    def post(self, request):
        form = request.POST.dict()      # 폼에서 텍스트데이터를 가져옴
        images = request.FILES.getlist('attach')     # 폼에서 파일데이터들을 가져옴
        uuid = datetime.now().strftime('%Y%m%d%H%M%S')
        # uuid2 = uuid4().hex     # 유니크한 문자열 생성 (16진수)

        # 임시폴더에 저장된 업로드 파일들을 지정한 위치에 저장
        # 단, 파일 저장시 'uuid + 파일명' 형식 사용
        images, fsizes = process_upload_files(images, uuid)

        g = Gallery(title=form['title'], contents=form['contents'],
                member=Member.objects.get(userid=form['userid']),
                fnames=json.dumps(images),
                fsizes=json.dumps(fsizes),
                uuid=uuid)
        g.save()

        return redirect('/gallery/list')

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
        fpath = 'c:/Java/galupload/' + p.uuid   # 삭제할 파일의 경로 정의

        #
        if request.session.get('userinfo').split('|')[0] ==  p.member.userid:
            for fn in json.loads(p.fnames):
                if fn:
                    rmvOne = fpath + fn
                    os.remove(rmvOne)   # 지정한 경로상의 파일 삭제

        # 테이블상의 게시글 삭제
        Pds.objects.filter(id=form['pno']).delete()

        return redirect('/gallery/list')


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