from django.conf.urls import url

import django_httpolice
import example_app.views


urlpatterns = [
    url(r'^api/v1/words/$', example_app.views.words),
    url(r'^httpolice/$', django_httpolice.report_view),
]
