import os

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dtype_inference.infer_file import load_data, infer_and_convert_data_types, get_column_dtype


@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})


@api_view(['POST'])
def upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        if not uploaded_file.name.endswith(('.csv', '.xlsx', '.xls')):
            return Response({'error': 'Invalid file format. Only .csv, .xlsx, or .xls files are allowed.'}, status=400)
        if uploaded_file.size / (1024 * 1024) > 200:
            return Response({'error': 'The file is too large. Limit file size to 200MB, or use the API.'}, status=400)
        df = load_data(uploaded_file)
        if df.empty:
            return Response({'error': 'The file is empty.'}, status=400)
        converted_df = infer_and_convert_data_types(df)
        return Response({
            'message': 'File uploaded successfully',
            'df': df.fillna(''),
            'df_dtype': get_column_dtype(df),
            'converted_df': converted_df.fillna(''),
            'converted_df_dtype': get_column_dtype(converted_df)
        }, status=200)
    else:
        return Response({'error': 'No file provided'}, status=400)
