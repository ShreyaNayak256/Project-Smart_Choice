"""DSCI_551_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from project import views
# import settings
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('firebase/<str:bounds>',views.get_firebase_data,name = "firebase_data"),
    path('select-platform/<str:platform>',views.select_platform,name="select_platform"),
    path('results/<str:platform>/<str:service>',views.get_results,name = "result"),
    path('results-filter-rating/<str:platform>/<str:service>/<int:start>/<int:end>',views.filter_rating,name = "filter_rating"),
    path('results-filter-genre/<str:platform>/<str:service>/<str:genre>',views.filter_genre,name = "filter_genre"),
    path('results-filter-year/<str:platform>/<str:service>/<int:year>',views.filter_year,name = "filter_year"),
    path('functions/',views.functions,name = "functions"),
    path('get-file-structure',views.get_file_structure,name = "get_file_sructure"),
    path('run-command/<str:db>/<str:com>/<str:args>',views.run_command,name="run_command"),
    # path('')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
