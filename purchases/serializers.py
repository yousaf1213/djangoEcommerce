from rest_framework import serializers
from .models import Product, User, Order, Vendor, Product_holders_List


class ProductSerializer(serializers.ModelSerializer):
    product = Product.objects.all()

    class Meta:
        model = Product
        fields = "__all__"


class VendorSerializer(serializers.ModelSerializer):
    vendor = Vendor.objects.all()

    class Meta:
        model = Vendor
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    user = User.objects.all()

    class Meta:
        model = User
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"


class ProductHolderList(serializers.ModelSerializer):
    vendor = VendorSerializer()
    product = ProductSerializer()

    class Meta:
        model = Product_holders_List
        fields = "__all__"
