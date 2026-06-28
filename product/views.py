from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import *


@api_view(["GET"])
def review_detail_api_view(request, id):
    try:
         review = Review.objects.get(id=id)
    except Review.DoesNotExist:
         return Response(data={'error':'review not found!! '},
                        status=status.HTTP_404_NOT_FOUND)
    list_    = ReviewDetailSeralizer(review, many=False).data
    return Response(data=list_)


@api_view(["GET"])
def review_list_api_view(request):
    reviews = Review.objects.all()
    list_ = ReviewListSeralizer(reviews, many=True).data
    return Response(data=list_)


@api_view(["GET"])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(
            data={"error":"product not found!! "},
            status=status.HTTP_404_NOT_FOUND
        )
    list_ = ProductDetailSeralizer(product, many=False).data
    return Response(data=list_)


@api_view(["GET"])
def product_list_api_view(request):
    products = Product.objects.all()
    list_ = ProductlistSeralizer(products, many=True).data
    return Response(data=list_)


@api_view(["GET"])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(
            data={"error":"category not found!! "},
            status=status.HTTP_404_NOT_FOUND
        )
    list_ = CategoryDetailSeralizer(category, many=False).data
    return Response(data=list_)


@api_view(["GET"])
def category_list_api_view(request):
    category = Category.objects.all()
    list_ = CategorylistSeralizer(category, many=True).data
    return Response(data=list_)


@api_view(["GET"])
def product_reviews_api_view(request):
    products = Product.objects.select_related("category").prefetch_related( "reviews")

    serializer = ProductReviewSerializer(products, many=True)
    return Response(serializer.data)
