from rest_framework.serializers import ModelSerializer, StringRelatedField
from api.models import Customer, Category, Product, Cart, Orders
from django.contrib.auth.models import User


class UserDeserializer(ModelSerializer):
    def create(self, validated_data):
        User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('username', 'password', 'is_staff')


class CustomerDeserializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['user_id']


class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AddCategoryDeserializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    category_id = StringRelatedField(read_only=True, many=False)

    class Meta:
        model = Product
        fields = '__all__'


class AddProductDeserializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class AddToCartDeserializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartListSerializer(ModelSerializer):
    customer_id = StringRelatedField(read_only=True, many=False)
    product_id = StringRelatedField(read_only=True, many=False)

    class Meta:
        model = Cart
        fields = '__all__'


class OrdersSerializer(ModelSerializer):
    customer_id = StringRelatedField(read_only=True, many=False)
    product_id = StringRelatedField(read_only=True, many=False)

    class Meta:
        model = Orders
        fields = '__all__'