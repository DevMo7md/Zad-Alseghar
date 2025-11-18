from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Prophet, Video, PDF
from .serializers import ProphetSerializer, VideoSerializer, PDFSerializer
# Create your views here.

class ProphetList(APIView):

    def get(self, request):
        prophets = Prophet.objects.all().order_by('name')

        name = request.query_params.get('name')
        age = request.query_params.get('age')
        info = request.query_params.get('info')

        if name:
            prophets = prophets.filter(name__icontains=name)

        if age:
            prophets = prophets.filter(age=age)
        
        if info:
            prophets = prophets.filter(info=info)


        paginator = PageNumberPagination()
        pagenated_data = paginator.paginate_queryset(prophets, request)
        serializer = ProphetSerializer(pagenated_data, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        serializer = ProphetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ProphetDetail(APIView):

    def get_object(self, pk):
        return get_object_or_404(Prophet, pk=pk)

    def get(self, request, pk):
        prophet = self.get_object(pk)
        serializer = ProphetSerializer(prophet)
        return Response(serializer.data)

    def put(self, request, pk):
        prophet = self.get_object(pk)
        serializer = ProphetSerializer(prophet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        prophet = self.get_object(pk)
        serializer = ProphetSerializer(prophet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        prophet = self.get_object(pk)
        prophet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VideoViewSet(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    pagination_class = PageNumberPagination

class PdfViewSet(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = PDF.objects.all()
    serializer_class = PDFSerializer
    pagination_class = PageNumberPagination

