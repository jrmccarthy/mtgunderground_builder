"""mtgstone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from __future__ import print_function
from django.conf.urls import url
from django.contrib import admin
import endpoints

# TODO: Build Regex fo the various URLs here to make real urlconf
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', endpoints.IndexView.as_view()),
    url(r'^deck/(?P<deck_blob>[0-9a-zA-Z]*)', endpoints.DeckView.as_view()),
    url(r'^builder/(?P<deck_blob>[0-9a-zA-Z]*)', endpoints.BuilderView.as_view()),
    url(r'^query_test/', endpoints.QueryTestView.as_view()),
]
