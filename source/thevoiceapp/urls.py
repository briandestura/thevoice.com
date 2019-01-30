"""takehome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from thevoiceapp.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'v1/auth/jwt/$', ObtainJwtToken.as_view(), name='v1.obtain-jwt-token'),

    url(r'^v1/candidate/(?P<candidate_id>\d+)/performances/$', CandidatePerformancesView.as_view(), name='v1.candidate-performances'),

    url(r'^v1/teams/$', TeamView.as_view(), name='v1.team'),
    url(r'^v1/teams/(?P<team_id>\d+)/$', TeamDetailsView.as_view(), name='v1.team-details'),
]
