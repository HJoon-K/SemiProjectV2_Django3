from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
import requests


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
            return redirect('/join/joinme')
        else:
            error = '자동가입방지 인증이 실패했습니다! 다시 시도하세요!'

        context = {'form': form, 'error': error}
        return render(request, 'join/checkme.html', context)

class JoinmeViews(View):
    def get(self, request):
        return render(request, 'join/joinme.html')

    def post(self, request):
        pass


class JoinokViews(View):
    def get(self, request):
        return render(request, 'join/joinok.html')

    def post(self, request):
        pass
