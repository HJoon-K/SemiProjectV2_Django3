from django.shortcuts import render, redirect

# Create your views here.
from django.views import View


class ListView(View):
    def get(self, request):
        return render(request, 'gallery/list.html')

    def post(self, request):
        pass


class ModifyView(View):
    def get(self, request):
        return render(request, 'gallery/modify.html')

    def post(self, request):
        pass


class ViewView(View):
    def get(self, request):
        return render(request, 'gallery/view.html')

    def post(self, request):
        pass


class WriteView(View):
    def get(self, request):
        return render(request, 'gallery/Write.html')

    def post(self, request):
        pass


class RemoveView(View):
    def get(self, request):
        return render(request, 'gallery/remove.html')

    def post(self, request):
        pass