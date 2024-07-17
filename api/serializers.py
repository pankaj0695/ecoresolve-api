from rest_framework import serializers
from .models import Feedback

class ChatSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000)

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'