import sys
import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from .models import Feedback, Rating
from .serializers import FeedbackSerializer
import torch
from django.utils import timezone
from django.utils.formats import date_format

# Initialize logging
logger = logging.getLogger(__name__)

# def get_model():
#     if 'runserver' in sys.argv or 'gunicorn' in sys.argv:
#         try:
#             tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")
#             model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2")
#             tokenizer.pad_token = tokenizer.eos_token
#             return tokenizer, model
#         except Exception as e:
#             logger.error(f"Error loading model: {e}")
#             return None, None
#     return None, None

def get_model():
    if 'runserver' in sys.argv or 'gunicorn' in sys.argv:
        try:
            model_name = "Moodyspider266/EnviroBot-Llama-3-8B"

            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
            )

            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                quantization_config=bnb_config,
                trust_remote_code=True,
                token="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"
            )
            model.config.use_cache = False

            tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, token="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")
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
        prompt =f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>{question}<|eot_id|> <|start_header_id|>user<|end_header_id|>Could you give me ideas to organize a friendly recycling competition at school?<|eot_id|><|start_header_id|>assistant<|end_header_id|><|eot_id|>"

        device = "cuda:0"
        inputs = tokenizer(prompt, return_tensors='pt', padding=True, truncation=True).to(device)
        attention_mask = inputs.attention_mask
        outputs = model.generate(inputs.input_ids, attention_mask=attention_mask, max_length=100)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return Response({'response': response.split("assistant")[-1]})
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

@api_view(['POST'])
def rate_experience(request):
    experience_rating = request.data.get('rating', None)
    
    if experience_rating is None:
        return Response({'error': 'Rating parameter is missing.'}, status=400)
    
    if experience_rating not in ['0', '1', '2']:
        return Response({'error': 'Invalid rating value. Expected 0 (poor), 1 (good), or 2 (excellent).' }, status=400)
    
    # Save rating to database
    rating = Rating.objects.create(rating=experience_rating)
    
    return Response({'message': 'Experience rating recorded successfully.'})



