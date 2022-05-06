from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
import base64
import json
from .run_model import getPredict
# Create your views here.
@api_view(['POST'])
def predict(request):
    encode_text = json.loads(request.body)['fileCode']
    decode_text = base64.b64decode(encode_text)
    file_wav = open('temp.wav', 'wb')
    file_wav.write(decode_text)
    return Response({'result': "getPredict('temp.wav')"})
