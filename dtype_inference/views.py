from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})


@api_view(['POST'])
def upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        # Process the uploaded file
        # For example, save it to a temporary location
        with open('uploaded_file.txt', 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        return Response({'message': 'File uploaded successfully'}, status=200)
    else:
        return Response({'error': 'No file provided'}, status=400)
