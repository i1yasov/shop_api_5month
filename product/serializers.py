from re import split

from rest_framework import serializers
from .models import Category, Product, Review
from product import models

class CategorylistSeralizer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = "name".split()


class CategoryDetailSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductlistSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "title price".split()


class ProductDetailSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ReviewListSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "text".split()


class ReviewDetailSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


