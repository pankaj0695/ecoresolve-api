import sys
import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view
from transformers import AutoTokenizer, AutoModelForCausalLM
from .models import Feedback
from .serializers import FeedbackSerializer
import torch
from django.utils import timezone
from django.utils.formats import date_format

# Initialize logging
logger = logging.getLogger(__name__)

def get_model():
    if 'runserver' in sys.argv or 'gunicorn' in sys.argv:
        try:
            tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")
            model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2")
            tokenizer.pad_token = tokenizer.eos_token
            return tokenizer, model
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return None, None
    return None, None

@api_view(['POST'])
def chat(request):
    question = request.data.get('question', '')
    if not question:
        return Response({'error': 'Question is required'}, status=400)

    tokenizer, model = get_model()
    if not tokenizer or not model:
        return Response({'error': 'Model not available'}, status=500)

    try:
        inputs = tokenizer(question, return_tensors='pt', padding=True, truncation=True)
        attention_mask = inputs.attention_mask

        outputs = model.generate(inputs.input_ids, attention_mask=attention_mask, max_length=100)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return Response({'response': response})
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return Response({'error': 'Error generating response'}, status=500)

@api_view(['POST'])
def submit_feedback(request):
    if request.method == 'POST':
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Feedback submitted successfully"}, status=201)
        logger.error(f"Validation error: {serializer.errors}")
        return Response(serializer.errors, status=400)
