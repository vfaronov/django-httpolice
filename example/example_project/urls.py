from django.conf.urls import url

import django_httpolice
import example_app.views


urlpatterns = [
    url(r'^api/v1/greet/$', example_app.views.greet),
    url(r'^api/v1/stream-greeting/$', example_app.views.stream_greeting),
    url(r'^httpolice/$', django_httpolice.report_view),
]
