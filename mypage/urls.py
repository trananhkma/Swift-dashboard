from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'mypage.views.home'),
    url(r'^performance/$', 'mypage.views.performance'),
    url(r'^instances/$', 'mypage.views.instances'),
    url(r'^containers/$', 'mypage.views.containerss'),
    url(r'^containers/', 'mypage.views.objects'),
    #url(r'^results/$', 'mypage.views.search_for_something', name='search_for_something'),
    url(r'^admin/', include(admin.site.urls)),
]