from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import *


@api_view(["GET", "PUT", "DELETE"])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error':'review not found!! '},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ReviewDetailSeralizer(review)
        return Response(serializer.data)

    elif request.method == "DELETE":
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PUT":
        serializer = ReviewValidationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        review.stars = serializer.validated_data.get("stars")
        review.text = serializer.validated_data.get("text")
        review.product_id = serializer.validated_data.get("product_id")

        review.save()

        return Response(
            ReviewDetailSeralizer(review).data,
            status=status.HTTP_200_OK
        )


@api_view(["GET", "POST"])
def review_list_api_view(request):
    if request.method == "GET":
        reviews = Review.objects.all()
        list_ = ReviewListSeralizer(reviews, many=True).data
        return Response(data=list_)
    elif request.method == "POST":
        serializer = ReviewValidationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        stars = serializer.validated_data.get("stars")
        text = serializer.validated_data.get("text")
        product_id = serializer.validated_data.get("product_id")

        review = Review.objects.create(
            stars = stars,
            text=text,
            product_id=product_id
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=ReviewDetailSeralizer(review).data
        )


@api_view(["GET", "PUT", "DELETE"])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(
            data={"error":"product not found!! "},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = ProductDetailSeralizer(product)
        return Response(serializer.data)

    elif request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PUT":
        serializer = ProductValidationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        product.title = serializer.validated_data.get("title")
        product.description = serializer.validated_data.get("description")
        product.price = serializer.validated_data.get("price")  # type: ignore
        product.category_id = serializer.validated_data.get("category_id")  # type: ignore

        product.save()

        return Response(status=status.HTTP_201_CREATED)


@api_view(["GET", "POST"])
def product_list_api_view(request):

    if request.method == "GET":
        products = Product.objects.all()
        list_ = ProductlistSeralizer(products, many=True).data
        return Response(data=list_)

    elif request.method == "POST":

        serializer = ProductValidationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        title = serializer.validated_data.get("title")
        description = serializer.validated_data.get("description")
        price = serializer.validated_data.get("price")
        category_id = serializer.validated_data.get("category_id")

        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category_id
        )
        return Response(
            status=status.HTTP_201_CREATED,
            data=ProductDetailSeralizer(product).data
        )


@api_view(["GET", "PUT", "DELETE"])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(
            data={"error":"category not found!! "},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == "GET":
        serializer = CategoryDetailSeralizer(category)
        return Response(serializer.data)

    elif request.method == "DELETE":
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PUT":
        serializer = CategoryValidationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        category.name = serializer.validated_data.get("name")

        category.save()
        return Response(status=status.HTTP_201_CREATED)

@api_view(["GET", "POST"])
def category_list_api_view(request):
    if request.method == "GET":
        category = Category.objects.all()
        list_ = CategorylistSeralizer(category, many=True).data
        return Response(data=list_)

    elif request.method == "POST":
        serializer = CategoryValidationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        name = serializer.validated_data.get("name")

        category = Category.objects.create(
            name = name
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data = CategoryDetailSeralizer(category).data
        )


@api_view(["GET"])
def product_reviews_api_view(request):
    products = Product.objects.select_related("category").prefetch_related( "reviews")

    serializer = ProductReviewSerializer(products, many=True)
    return Response(serializer.data)
