
from rest_framework import serializers
from .models import *

# ======================================================================================
class CategorySimpleSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Category
        fields = ('title', 'image','id')
# ======================================================================================
class ProductSerializer(serializers.ModelSerializer):
	image = serializers.ImageField(use_url=True)

	class Meta:
		model = Product
		fields = '__all__'
# ======================================================================================
class CategorySerializer(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=True)
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = '__all__'
# ======================================================================================
class CartSimpleSerializer(serializers.ModelSerializer):

	class Meta:
		model= Cart
		fields = '__all__'
# ======================================================================================
class ProductVariationSimpleSerializer(serializers.ModelSerializer):

	class Meta:
		model = ProductVariation
		fields = ("cant", 'price', 'clothing_s', 'id')
# ======================================================================================
class ProductVariationSerializer(serializers.ModelSerializer):

	product = ProductSerializer()

	class Meta:
		model = ProductVariation
		fields = ("cant", 'price', 'id', 'product', 'clothing_s')
# ======================================================================================
class CartSerializer(serializers.ModelSerializer):

	products = ProductVariationSerializer(source='product_variation_set', many=True)

	class Meta:
		model= Cart
		fields = ('ip_address', 'cost', 'last', 'products')
