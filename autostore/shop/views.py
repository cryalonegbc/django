from django.shortcuts import render
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from .pagination import CarsPagination
from .models import Car, News, Advertisement, Sale, Comment
from .serializers import CarSerializer, NewsSerializer, AdvertisementSerializer, SaleSerializer, CommentSerializer
from django.contrib.auth.models import User

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    pagination_class = CarsPagination

    filter_backends = [SearchFilter]
    search_fields = ['brand', 'model']

    @action(detail=False, methods=['get'])
    def filter_cars(self, request):
        brand = self.request.query_params.get('brand')
        target_year = self.request.query_params.get('year')
        target_price = self.request.query_params.get('price')

        if brand and target_price and target_year:
            condition = Q(brand=brand) & ~Q(year__gt=target_year) | Q(brand=brand) & ~Q(price__gt=target_price)
            

        filtered_cars = Car.objects.filter(condition)
        serializer = CarSerializer(filtered_cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        car = self.get_object()
        user_id = request.query_params.get('user_id')
        text = request.data.get('text', '')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь с указанным id не найден.'}, status=status.HTTP_404_NOT_FOUND)
        comment = Comment.objects.create(user=user, text=text, car=car)

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
  

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    @action(detail=False, methods=['get'])
    def filter_comments(self, request):
        user_id = self.request.query_params.get('user')

        if user_id:
            comments = Comment.objects.filter(
            Q(user_id=user_id) & (Q(car__isnull=False) | Q(advertisement__isnull=False)) & ~Q(news__isnull=False)
            )
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
