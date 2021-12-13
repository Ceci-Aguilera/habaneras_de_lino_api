
from rest_framework import serializers
from .models import *

# ======================================================================================
class CategorySerializer(serializers.ModelSerializer):

	image = serializers.ImageField(use_url=True)

	class Meta:
		model = Category
		fields = '__all__'

class CategorySimpleSerializerFilter(serializers.ModelSerializer):

	class Meta:
		model = Category
		fields = ('title', 'id')

class CustomColorsSerializer(serializers.ModelSerializer):

	class Meta:
		model = CustomColor
		fields = '__all__'

# ======================================================================================
class ProductSerializer(serializers.ModelSerializer):
	image = serializers.ImageField(use_url=True)
	s_image = serializers.ImageField(use_url=True)
	category = CategorySerializer()
	available_colors = CustomColorsSerializer(many=True)
	description = serializers.CharField(required=False, allow_blank=True)

	class Meta:
		model = Product
		exclude = ('collection', )


class CustomCollectionSerializer(serializers.ModelSerializer):
	description = serializers.CharField(required=False, allow_blank=True)
	all_products_per_collection = ProductSerializer(source='products_per_collection_set', many=True)
	image = serializers.ImageField(use_url=True)

	class Meta:
		model = CustomCollection
		fields = '__all__'


class CustomCollectionSimpleSerializerFilter(serializers.ModelSerializer):

	class Meta:
		model = CustomCollection
		fields = ('title', 'id')


class ProductImageSimpleSerializer(serializers.ModelSerializer):

	class Meta:
		model = ProductImage
		fields = ['image', 'id', 'pk']


# ======================================================================================
class CategorySimpleSerializer(serializers.ModelSerializer):

	image = serializers.ImageField(use_url=True)
	products = ProductSerializer(source='product_set', many=True)

	class Meta:
		model = Category
		fields = ('title', 'image','id', 'products')

# ======================================================================================
class CartSimpleSerializer(serializers.ModelSerializer):

	class Meta:
		model= Cart
		fields = '__all__'
# ======================================================================================
class ProductVariationSimpleSerializer(serializers.ModelSerializer):

	class Meta:
		model = ProductVariation
		fields = ("cant", 'price', 'clothing_s', 'id', 'size_of_sleeve', 'fit', 'color')
# ======================================================================================
class ProductVariationSerializer(serializers.ModelSerializer):

	product = ProductSerializer()

	class Meta:
		model = ProductVariation
		fields = ("cant", 'price', 'id', 'product', 'clothing_s', 'size_of_sleeve', 'fit', 'color')
# ======================================================================================
class CartSerializer(serializers.ModelSerializer):

	products = ProductVariationSerializer(source='product_variation_set', many=True)

	class Meta:
		model= Cart
		fields = ('ip_address', 'cost', 'last', 'products','token')

# ======================================================================================

class PaymentSerializer(serializers.ModelSerializer):

	email = serializers.EmailField(required=False)

	class Meta:
		model = Payment
		fields = '__all__'

# ======================================================================================

class OrderSerializer(serializers.ModelSerializer):

	email = serializers.EmailField(required=False, allow_blank=True)
	cart = CartSerializer(read_only=True)
	payment = PaymentSerializer(read_only=True)
	phone = serializers.CharField(max_length=None, min_length=None, required=True, allow_blank=False)
	address2 = serializers.CharField(max_length=None, min_length=None, required=False, allow_blank=True)

	class Meta:
		model = Order
		fields = '__all__'
