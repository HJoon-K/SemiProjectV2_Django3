from django.shortcuts import render

# Create your views here.
from django.views import View


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