from django.urls import path
from .views import SendMessage

urlpatterns = [
    path("sending_message/", SendMessage.as_view()),
]
