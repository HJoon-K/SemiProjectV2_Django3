from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from join.models import Member


class AdminViews(View):
    def get(self, request):
        return render(request, 'admin.html')

    def post(self, request):
        pass

class IntroViews(View):
    def get(self, request):
        return render(request, 'intro.html')

    def post(self, request):
        pass

class HomeViews(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        pass

# 로그인 처리
class LoginViews(View):
    def post(self, request):
        form = request.POST.dict()
        # print(form)

        # select count(userid) from Member where userid = *** and passwd = ***
        # count() 와 exists()의 차이는 찾는 데이터가 존재하면 찾는 것을 멈춤
        returnPage = '/loginfail'
        isExisted = Member.objects.filter(userid=form['userid'], passwd=form['passwd']).exists()
        # count = Member.objects.filter(userid=form['userid'], passwd=form['passwd']).count()
                # print(count)

        if isExisted:    # 로그인 성공시
        # if count == 1:    # 로그인 성공시
            # 세션변수에 아이디와 id값을 저장(userinfor': abc123|1')
            user = Member.objects.get(userid=form['userid'])
            request.session['userinfo'] = form['userid'] + '|' + str(user.id)
            print(request.session['userinfo'])


            returnPage ='/'

        return redirect(returnPage)

        pass


class LogoutViews(View):
    def get(self, request):
        #세션변수들 중에서 userinfo키만 삭제
        # if request.session.get('userinfo'):
        #     del(request.session['userinfo'])

        # 세션변수의 모든 키를 삭제
        # keys = request.session.keys()
        # for key in keys:
        #     print (request.session[key])
        #     del(request.session[key])

        # 세션변수 삭제
        request.session.flush()
        return redirect('/')

# 로그인 실패시 보여줄 페이지 지정
class LoginfailViews(View):
    def get(self, request):
        return render(request, 'loginfail.html')

    def post(self, request):
        pass
