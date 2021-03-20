from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from queryapi.views import QuestionView

urlpatterns = [
   # URL from Login View
   url('questions',    QuestionView.as_view(), name='questions'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
