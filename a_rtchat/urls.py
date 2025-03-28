from django.urls import path
from .views import *

urlpatterns = [
    path('', lambda request: redirect('chatroom', chatroom_name='public-chat'), name="home"),

    path('chat/<username>', get_or_create_chatroom, name="start-chat"),
    path('chat/room/<chatroom_name>', chat_view, name="chatroom"),
]
