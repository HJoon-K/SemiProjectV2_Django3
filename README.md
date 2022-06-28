# Django 프로젝트 생성 순서
1. 앱 생성하기 (ctrl + alt + R)
    * startapp home
    * startapp join
    * startapp board
    * startapp pds
    * startapp gallery

2 프로젝트 설정 (settings.py)
   * INSTALLED_APPS
     + 'home.apps.HomeConfig',
   * TEMPLATES
     + 'DIRS': [BASE_DIR / 'templates']
   * LANGUAGE_CODE
     + LANGUAGE_CODE = 'ko-kr'   
   * TIME_ZONE
     + TIME_ZONE = 'Asia/Seoul'
   * USE_TZ
     + USE_TZ = False
   * STATIC
     + STATICFILES_DIRS = [BASE_DIR / 'static']
   * ALLOEWD_HOSTS
   * DATABSES

3. 데이터베이스 초기화 (ctrl + alt + R)
    * migrate

4. 앱과 관련된 urls 설정 (urls.py)
    * path('/home/admin', admin.site.urls))
    * path('', include('home.urls'))
    * path('', include('join.urls'))
    * path('', include('board.urls'))
    * path('', include('pds.urls'))
    * path('', include('gallery.urls'))

5. home 앱과 관련된 urls 설정(home/urls.py)
    * path('', views.HomeViews.as_view(), name='index'),
    * path('intro/', views.IntroViews.as_view(), name='index'),
    * path('admin/', views.AdminViews.as_view(), name='index'),

6. home 앱과 관련된 views 설정 (home/views.py)
   
7. template 설정
    * layouts - base, header, footer, modal
    * 각 앱과 관련된  웹 페이지

8. static 설정
    * css, js, imgs
    * bootstarp5

9. join 앱과 관련된 urls 설정(join/urls.py)
    * path('agree/', views.AgreeViews.as_view(), name='agree'),
    * path('checkme/', views.CheckmeViews.as_view(), name='checkme'),
    * path('joinme/', views.JoinmeViews.as_view(), name='joinme'),
    * path('joinok/', views.JoinokViews.as_view(), name='joinok'),

10. join 앱과 관련된 views 설정 (join/views.py)