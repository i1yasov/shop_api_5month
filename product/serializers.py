from rest_framework import serializers
from .models import Category, Product, Review

class CategorylistSeralizer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    class Meta:
        model=Category
        fields = "name products_count".split()

    def get_products_count(self, obj):
        return obj.products.count()


class CategoryDetailSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ReviewListSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "text stars".split()


class ReviewDetailSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ProductlistSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "title price".split()


class ProductDetailSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductReviewSerializer(serializers.ModelSerializer):
    category = CategorylistSeralizer(read_only=True)
    reviews = ReviewListSeralizer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "title price reviews category rating".split()

    def get_rating(self, obj):
        reviews = obj.reviews.all()

        if not reviews:
            return 0

        return sum(r.stars for r in reviews) / reviews.count()
