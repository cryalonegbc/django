from rest_framework import serializers
from .models import Car, News, Advertisement, Sale, Comment

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

    def validate_year(self, value):
        if value < 1886:  # Первый год производства автомобилей
            raise serializers.ValidationError("Please enter a valid manufacturing year.")
        return value

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

    def validate_sale_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Sale price must be greater than zero.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, data):
        prohibited_words = ["bad", "inappropriate", "spam"]
        for word in prohibited_words:
            if word in data['text'].lower():
                raise serializers.ValidationError(f"Comment cannot contain the word '{word}'.")
        return data