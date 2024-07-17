from rest_framework.response import Response
from rest_framework.decorators import api_view
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from .models import Feedback
from .serializers import FeedbackSerializer

# Load the tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained("bilalRahib/TinyLLama-NSFW-Chatbot")
model = AutoModelForCausalLM.from_pretrained("bilalRahib/TinyLLama-NSFW-Chatbot")

@api_view(['POST'])
def chat(request):
    question = request.data.get('question', '')
    inputs = tokenizer.encode(question, return_tensors='pt')
    outputs = model.generate(inputs, max_length=100)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return Response({'response': response})

@api_view(['POST'])
def submit_feedback(request):
    if request.method == 'POST':
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Feedback submitted successfully"}, status=201)
        return Response(serializer.errors, status=400)

