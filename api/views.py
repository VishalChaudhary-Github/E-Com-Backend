from rest_framework.views import APIView
from api.models import Customer, Category, Product, Cart, Orders
from api.serializers import (ProductSerializer, UserDeserializer, AddCategoryDeserializer, CategoryListSerializer,
                             AddProductDeserializer, CustomerDeserializer, CustomerSerializer, AddToCartDeserializer,
                             CartListSerializer, OrdersSerializer)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        deserialize = UserDeserializer(data=data)
        if deserialize.is_valid(raise_exception=True):
            deserialize.create(deserialize.validated_data)
            return Response(status=status.HTTP_201_CREATED)


class CreateCustomerView(APIView):
    def post(self, request):
        data = request.data
        data['user_id'] = request.user.id
        deserialize = CustomerDeserializer(data=data)
        if deserialize.is_valid(raise_exception=True):
            deserialize.create(deserialize.validated_data)
            return Response(status=status.HTTP_201_CREATED)


class CustomerView(APIView):
    def get(self, request):
        try:
            obj = request.user.customer
        except Exception as e:
            return Response(data={"error": f'{e}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serialize = CustomerSerializer(instance=obj)
            return Response(data=serialize.data)


class UpdateCustomerView(APIView):
    def put(self, request):
        try:
            obj = request.user.customer
        except Exception as e:
            return Response(data={"error": f'{e}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            data = request.data
            Customer.objects.filter(id=obj.pk).update(**data)
            obj = Customer.objects.get(id=obj.pk)
            serialize = CustomerSerializer(instance=obj)
            return Response(serialize.data)


class AccountDeactivateView(APIView):
    def delete(self, request):
        try:
            obj = request.user.customer
        except Exception as e:
            return Response(data={"error": f'{e}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            usr = User.objects.get(id=request.user.pk)
            usr.is_active = False
            usr.save()
            return Response(data={"message": "Account Deactivated"}, status=status.HTTP_200_OK)


class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        if 'username' not in data:
            return Response(data={"message": "Provide Username"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            obj = User.objects.get(username=data['username'])
        except Exception as e:
            return Response(data={"error": f'{e}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            obj.is_active = True
            obj.save()
            return Response(data={"message": "Account Activated"}, status=status.HTTP_200_OK)


class CategoryListView(APIView, PageNumberPagination):
    page_size = 3
    page_query_param = 'pg'
    def get(self, request):
        qs = Category.objects.all()
        result = self.paginate_queryset(qs, request, view=self)
        serialize = CategoryListSerializer(instance=result, many=True)
        return self.get_paginated_response(data=serialize.data)


class AddCategoryView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = request.data
        deserialize = AddCategoryDeserializer(data=data)
        if deserialize.is_valid(raise_exception=True):
            deserialize.create(deserialize.validated_data)
            return Response(status=status.HTTP_201_CREATED)


class DeleteCategoryView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, category_id):
        try:
            obj = Category.objects.get(id=category_id)
        except Exception as e:
            return Response(data={"error": f'{e}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            obj.delete()
            return Response(status=status.HTTP_200_OK)


class ProductListView(APIView, PageNumberPagination):
    page_size = 2
    page_query_param = 'pg'

    def get(self, request):
        qs = Product.objects.all()
        result = self.paginate_queryset(qs, request, view=self)
        serialize = ProductSerializer(instance=result, many=True)
        return self.get_paginated_response(data=serialize.data)


class AddProductView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = request.data
        deserialize = AddProductDeserializer(data=data)
        if deserialize.is_valid(raise_exception=True):
            deserialize.create(deserialize.validated_data)
            return Response(status=status.HTTP_201_CREATED)


class UpdateProductView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, product_id):
        try:
            obj = Product.objects.get(id=product_id)
        except Exception as e:
            return Response(data={"error": f'{e}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            obj.save()
            data = request.data
            Product.objects.filter(id=product_id).update(**data)
            return Response(status=status.HTTP_200_OK)


class DeleteProductView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, product_id):
        try:
            obj = Product.objects.get(id=product_id)
        except Exception as e:
            return Response(data={"error": f'{e}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            obj.delete()
            return Response(status=status.HTTP_200_OK)


class AddToCartView(APIView):
    def post(self, request):
        data = request.data
        data['customer_id'] = request.user.customer.pk
        deserialize = AddToCartDeserializer(data=data)
        if deserialize.is_valid(raise_exception=True):
            deserialize.create(deserialize.validated_data)
            return Response(status=status.HTTP_201_CREATED)


class ListCartView(APIView):
    def get(self, request):
        qs = Cart.objects.filter(customer_id=request.user.customer.pk)
        serialize = CartListSerializer(instance=qs, many=True)
        return Response(data=serialize.data)


class RemoveFromCartView(APIView):
    def post(self, request, product_id):
        try:
            obj = Cart.objects.get(customer_id=request.user.customer.pk, product_id=product_id)
        except Exception as e:
            return Response(data={"error": f'{e}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            obj.delete()
            return Response(status=status.HTTP_200_OK)


class PlaceOrderView(APIView):
    def post(self, request):
        qs1 = Cart.objects.filter(customer_id=request.user.customer.pk)
        for obj in qs1:
            subtotal = obj.quantity * obj.product_id.price
            Orders.objects.create(customer_id=obj.customer_id, product_id=obj.product_id, quantity=obj.quantity,
                                  subtotal=subtotal)

        qs1.delete()
        qs2 = Orders.objects.filter(customer_id=request.user.customer.pk)
        serializer = OrdersSerializer(instance=qs2, many=True)
        return Response(data=serializer.data)