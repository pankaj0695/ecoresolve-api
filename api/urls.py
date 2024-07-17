from django.urls import path
from .views import chat, submit_feedback

urlpatterns = [
    path('chat/', chat, name='chat'),
    path('feedback/', submit_feedback, name='submit_feedback')
]
