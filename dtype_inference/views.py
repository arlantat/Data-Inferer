from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dtype_inference.infer_file import load_data, infer_and_convert_data_types


@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})


@api_view(['POST'])
def upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        if not uploaded_file.name.endswith(('.csv', '.xlsx', '.xls')):
            return Response({'error': 'Invalid file format. Only .csv, .xlsx, or .xls files are allowed.'}, status=400)
        df = load_data(uploaded_file)
        converted_df = infer_and_convert_data_types(df)
        return Response({
            'message': 'File uploaded successfully',
            'df': df.fillna(''),
            'converted_df': converted_df.fillna('')
        }, status=200)
    else:
        return Response({'error': 'No file provided'}, status=400)
