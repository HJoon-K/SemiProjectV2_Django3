from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core import serializers

# Create your views here.
from django.views import View
import requests

from join.models import Zipcode, Member


class AgreeViews(View):
    def get(self, request):
        return render(request, 'join/agree-1.html')

    def post(self, request):
        pass


class CheckmeViews(View):
    def get(self, request):
        return render(request, 'join/checkme.html')

    def post(self, request):
        # captcha 사용시 클라이언트가 생성한 키와
        # 서버에 설정해둔 (비밀)키등을
        # google의 siteverify에서 비교해서 인증에 성공하면
        # joinme로 redirect 하고 그렇지 않으면 다시 checkme로 return함
        SECRET_kEY = '6LdV86YgAAAAAMh2Og_DTWlXAnPhbsVNEUywlgTt'
        VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'

        form = request.POST.dict()

        # 질의를 위한 질의문자열을 작성
        # ?secret=비밀키&response=클라이언트응답키
        params = {'secret': SECRET_kEY, 'response': form['g-recaptcha']}

        # 구글에 recaptcha 인증사이트에 키들을 질의문자열로 보내
        # 올바른 키인지 확인하고 결과를 json으로 받아옴
        # requests.get(URL, 질의문자열)
        result = requests.get(VERIFY_URL, params).json()

        if result['success']:
            # 인증성공시 이름과 전화번호를
            tokens = { 'name': form['name'], 'phone': form['phone']}

            # 쿠키 설정없이 페이지만 전환
            # return redirect('/join/joinme')

            # 쿠키 설정하고 페이지로로 전환
            res = redirect('/join/joinme')
            # dict 객체를 쿠키에 저장해 둠(유지시간 10분)
            # 응답객체.set_cookie(키, 값, 유지시간)
            res.set_cookie('tokens', tokens, max_age=60*10)
            return res

        else:
            error = '자동가입방지 인증이 실패했습니다! 다시 시도하세요!'

        context = {'form': form, 'error': error}
        return render(request, 'join/checkme.html', context)

class JoinmeViews(View):
    def get(self, request):
        # 쿠기에 저장된 객체를 불러올려면 request.COOKIES.get(이름)
        cookie = request.COOKIES.get('tokens')
        print(cookie)
        # cookie = '{}'

        return render(request, 'join/joinme.html', eval(cookie))

    def post(self, request):
        pass


class JoinokViews(View):
    def get(self, request):
        return render(request, 'join/joinok.html')

    def post(self, request):
        pass

class ZipcodeViews(View):
    def get(self, request):
        form = request.GET.dict()

        # select * from zipcode where dong = 동이름
        # 테이블모델명.objects.get(조건) : 1개의 결과값만 처리
        # result = Zipcode.objects.get(dong='사당동')
        # print(result.zipcode)   # 속성명으로 값 출력

        # 테이블모델명.objects.filter(조건) : 1개이상 결과값 처리
        result = Zipcode.objects.filter(dong=form['dong'])
        # print(result.value())

        #조회결과를 JSON객체로 생성
        json_data = serializers.serialize('json', result)
        # print(json_data, form['dong'])

        # 생성된 JSON객체를 HTTP 응답객체로 전송
        return HttpResponse(json_data, content_type='application/json')

    def post(self, request):
        pass


class UseridViews(View):
    def get(self, request):
        # /join/userid?=***
        # 응답 메세지 => { 'result': 0 또는 1 }
        form = request.GET.dict()

        result = Member.objects.filter(userid=form['userid'])
        print(result.value())

        json_data = serializers.serialize('json', result)
        return HttpResponse(json_data, content_type='application/json')

    def post(self, request):
        pass