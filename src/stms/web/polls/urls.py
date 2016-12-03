from django.conf.urls import url
import django

urlpatterns = [
    url(r'js/(?P<path>.*)$', django.views.static.serve, {'document_root': './templates/js'}),
]
