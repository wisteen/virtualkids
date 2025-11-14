"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('robots.txt', TemplateView.as_view(template_name='../static/robots.txt', content_type='text/plain')),
    path('sitemap.xml', TemplateView.as_view(template_name='sitemap.xml', content_type='application/xml')),
    path('about/', views.about, name='about'),
    path('partnership/', views.partnership, name='partnership'),
    path('programs/', views.programs, name='programs'),
    path('programs/<int:program_id>/register/', views.program_register, name='program_register'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('contact/', views.contact, name='contact'),
    path('careers/', views.careers, name='careers'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Custom error handlers
handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'
