from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

import json
from datetime import datetime
from random import randint

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework.views import APIView

from .models import *
from .serializers import *

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY




class CustomCollectionListView(ListAPIView):
	authentication_classes = []
	serializer_class = CustomCollectionSerializer
	model = CustomCollection
	queryset = CustomCollection.objects.all()

	def get_serializer_context(self):
		context = super(CustomCollectionListView, self).get_serializer_context()
		context.update({"request": self.request})
		return context





class ProductImagesView(APIView):
	authentication_classes = []

	def get(self, request, id, format=None):
		images = ProductImage.objects.filter(product__id = id)
		images_serializer = ProductImageSimpleSerializer(images, many=True, context={"request":request}).data
		return Response ({"Images": images_serializer}, status=status.HTTP_200_OK)





class CategoryListView(ListAPIView):
	authentication_classes = []
	serializer_class = CategorySimpleSerializer
	model = Category
	queryset = Category.objects.all()

	def get_serializer_context(self):
		context = super(CategoryListView, self).get_serializer_context()
		context.update({"request": self.request})
		return context





class CategoryMenListView(APIView):
	authentication_classes = []
	def get(self, request, format=None):
		info_to_serialize = Category.objects.filter(product_set__extra_tag='MEN').distinct()
		men_category = CategorySimpleSerializer(info_to_serialize, many=True, context={"request":request}).data
		return Response({"Categories": men_category}, status=status.HTTP_200_OK)




class CategoryWomenListView(ListAPIView):
	authentication_classes = []

	def get(self, request, format=None):
		info_to_serialize = Category.objects.filter(product_set__extra_tag='WOMEN').distinct()
		women_category = CategorySimpleSerializer(info_to_serialize, many=True, context={"request":request}).data
		return Response({"Categories": women_category}, status=status.HTTP_200_OK)





class CategoryDetailView(RetrieveAPIView):
	authentication_classes = []
	serializer_class = CategorySimpleSerializer
	model = Category
	lookup_field = 'id'
	queryset = Category.objects.all()

	def get_serializer_context(self):
		context = super(CategoryDetailView, self).get_serializer_context()
		context.update({"request": self.request})
		return context





class CustomCollectionDetailView(RetrieveAPIView):
	authentication_classes = []
	serializer_class = CustomCollectionSerializer
	model = CustomCollection
	lookup_field = 'id'
	queryset = CustomCollection.objects.all()

	def get_serializer_context(self):
		context = super(CustomCollectionDetailView, self).get_serializer_context()
		context.update({"request": self.request})
		return context






class CustomCollectionMenListView(APIView):
	authentication_classes = []
	def get(self, request, format=None):
		info_to_serialize = CustomCollection.objects.filter(products_per_collection_set__extra_tag='MEN').distinct()
		men_collection = CustomCollectionSerializer(info_to_serialize, many=True, context={"request":request}).data
		return Response({"Collections": men_collection}, status=status.HTTP_200_OK)





class CustomCollectionWomenListView(ListAPIView):
	authentication_classes = []

	def get(self, request, format=None):
		info_to_serialize = CustomCollection.objects.filter(products_per_collection_set__extra_tag='WOMEN').distinct()
		women_collection = CustomCollectionSerializer(info_to_serialize, many=True, context={"request":request}).data
		return Response({"Collections": women_collection}, status=status.HTTP_200_OK)





class ProductListView(ListAPIView):
	authentication_classes = []
	serializer_class = ProductSerializer
	model = Product
	queryset = Product.objects.all()

	def get_serializer_context(self):
		context = super(ProductListView, self).get_serializer_context()
		context.update({"request": self.request})
		return context






class ProductDetailView(RetrieveAPIView):
	authentication_classes = []
	serializer_class = ProductSerializer
	model = Product
	lookup_field = 'id'
	queryset = Product.objects.all()

	def get_serializer_context(self):
		context = super(ProductDetailView, self).get_serializer_context()
		context.update({"request": self.request})
		return context






class CategoryTitleDetailView(APIView):
	authentication_classes = []
	serializer_class = CustomCollectionSerializer
	model = CustomCollection

	def get(self,request, *args, **kwargs):
		title = kwargs['title']
		category = Category.objects.all().get(title=title)
		category_serializer = CategorySerializer(category, context={"request": request}).data
		products = Product.objects.filter(category=category)
		products_serializer = ProductSerializer(products, many=True, context={"request": request}).data
		return Response({"Category": category_serializer, 'Products': products_serializer}, status=status.HTTP_200_OK)



class CategoryTitleWomenDetailView(APIView):
	authentication_classes = []
	serializer_class = CustomCollectionSerializer
	model = CustomCollection

	def get(self,request, *args, **kwargs):
		title = kwargs['title']
		category = Category.objects.all().get(title=title)
		category_serializer = CategorySerializer(category, context={"request": request}).data
		products = Product.objects.filter(category=category, extra_tag="WOMEN")
		products_serializer = ProductSerializer(products, many=True, context={"request": request}).data
		return Response({"Category": category_serializer, 'Products': products_serializer}, status=status.HTTP_200_OK)





class CategoryTitleMenDetailView(APIView):
	authentication_classes = []
	serializer_class = CustomCollectionSerializer
	model = CustomCollection

	def get(self,request, *args, **kwargs):
		title = kwargs['title']
		category = Category.objects.all().get(title=title)
		category_serializer = CategorySerializer(category, context={"request": request}).data
		products = Product.objects.filter(category=category, extra_tag="MEN")
		products_serializer = ProductSerializer(products, many=True, context={"request": request}).data
		return Response({"Category": category_serializer, 'Products': products_serializer}, status=status.HTTP_200_OK)




class CategoryTitleKidsDetailView(APIView):
	authentication_classes = []
	serializer_class = CustomCollectionSerializer
	model = CustomCollection

	def get(self,request, *args, **kwargs):
		title = kwargs['title']
		category = Category.objects.all().get(title=title)
		category_serializer = CategorySerializer(category, context={"request": request}).data
		products = Product.objects.filter(category=category, extra_tag="KIDS")
		products_serializer = ProductSerializer(products, many=True, context={"request": request}).data
		return Response({"Category": category_serializer, 'Products': products_serializer}, status=status.HTTP_200_OK)






class CustomCollectionTitleDetailView(APIView):
	authentication_classes = []
	serializer_class = CustomCollectionSerializer
	model = CustomCollection

	def get(self,request, *args, **kwargs):
		title = kwargs['title']
		collection = CustomCollection.objects.all().get(title=title)
		collection_serializer = CustomCollectionSerializer(collection, context={"request": request}).data
		return Response({"Collection": collection_serializer}, status=status.HTTP_200_OK)






class ProductsPerExtraTag(APIView):

	def get(self, request, format=None):

		women = dict()
		info_to_serialize = Category.objects.filter(product_set__extra_tag='WOMEN').distinct().only("title", "id")
		women['category'] = CategorySimpleSerializerFilter(info_to_serialize, many=True, context={"request":request}).data
		info_to_serialize = CustomCollection.objects.filter(products_per_collection_set__extra_tag='WOMEN').distinct().only("title", "id")
		women['collection'] = CustomCollectionSimpleSerializerFilter(info_to_serialize, many=True, context={"request":request}).data

		men = dict()
		info_to_serialize = Category.objects.filter(product_set__extra_tag='MEN').distinct().only("title", "id")
		men['category'] = CategorySimpleSerializerFilter(info_to_serialize, many=True, context={"request":request}).data
		info_to_serialize = CustomCollection.objects.filter(products_per_collection_set__extra_tag='MEN').distinct().only("title", "id")
		men['collection'] = CustomCollectionSimpleSerializerFilter(info_to_serialize, many=True, context={"request":request}).data

		kids = dict()
		info_to_serialize = Category.objects.filter(product_set__extra_tag='KIDS').distinct().only("title", "id")
		kids['category'] = CategorySimpleSerializerFilter(info_to_serialize, many=True, context={"request":request}).data
		info_to_serialize = CustomCollection.objects.filter(products_per_collection_set__extra_tag='KIDS').distinct().only("title", "id")
		kids['collection'] = CustomCollectionSimpleSerializerFilter(info_to_serialize, many=True, context={"request":request}).data

		return Response({"women": women, "men":men, "kids":kids}, status=status.HTTP_200_OK)






class CartView(APIView):

	# Retrieve cart
	def get(self, request, token, format=None):
		data = request.data

		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

		if x_forwarded_for:
			ipaddress = x_forwarded_for.split(',')[-1].strip()
		else:
			ipaddress = request.META.get('REMOTE_ADDR')

		try:
			cart = Cart.objects.get(ip_address = ipaddress, last=True, token = token)
			if Coupon.objects.filter(cart=cart).first() != None:
				coupon = Coupon.objects.get(cart=cart)
				coupon_serializer = CouponSerializer(coupon, context={"request": request}).data
			else:
				coupon = None
				coupon_serializer = None

			cart = CartSerializer(cart, context={"request": request}).data
			return Response({"Cart": cart, "Coupon": coupon_serializer}, status=status.HTTP_200_OK)
		except:
			return Response({"Cart":"Error", Coupon: "None"}, status=status.HTTP_400_BAD_REQUEST)

	# Add product to the cart
	def post(self, request, format=None, token=None):
		data = request.data


		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

		if x_forwarded_for:
			ipaddress = x_forwarded_for.split(',')[-1].strip()
		else:
			ipaddress = request.META.get('REMOTE_ADDR')

		try:
			cart = Cart.objects.get(ip_address = ipaddress, last=True, token=token)
		except:
			token = urlsafe_base64_encode(force_bytes(randint(1,999999)))
			cart = Cart(ip_address = ipaddress, cost = 0, last = True, token=token)
			cart.save()

		product_serializer = ProductVariationSimpleSerializer(data=data, context={"request": request})
		if product_serializer.is_valid():
			
			product = product_serializer.save()
			original_product = Product.objects.get(id = data['original_product_id'])
			product.product = original_product
			product.cart = None
			product.save()

			try:
				cart_product = ProductVariation.objects.get(product = product.product, cart = cart, cart__last=True)
				if (cart_product.clothing_s == product.clothing_s) and (cart_product.size_of_sleeve == product.size_of_sleeve) and (cart_product.fit == product.fit):
					cart_product.cant += product.cant
					cart_product.product.amount_sold += product.cant
					cart_product.price += product.price
					cart_product.save()
					cart.cost += product.price
					cart.save()
					product.delete()
				else:
					cart.cost += product.price
					cart.save()
					product.cart = cart
					product.product.amount_sold += product.cant
					product.save()

			except:
				cart.cost += product.price
				cart.save()
				product.cart = cart
				product.save()

			if Coupon.objects.filter(cart=cart).first() != None:
				coupon = Coupon.objects.get(cart=cart)
				coupon_serializer = CouponSerializer(coupon, context={"request": request}).data
			else:
				coupon = None
				coupon_serializer = None

			cart = CartSerializer(cart, context={"request": request}).data

			return Response({"Cart":cart, "Coupon": coupon_serializer}, status=status.HTTP_200_OK)

		else:
			return Response({"Cart": "Error", "Coupon": None}, status=status.HTTP_400_BAD_REQUEST)


	# Delete cart
	def delete(self, request, token, format=None):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

		if x_forwarded_for:
			ipaddress = x_forwarded_for.split(',')[-1].strip()
		else:
			ipaddress = request.META.get('REMOTE_ADDR')

		try:
			cart = Cart.objects.get(ip_address = ipaddress, last=True, token=token)
			products_from_cart = ProductVariation.objects.filter(cart__id=cart.id)
			for product_from_cart in products_from_cart:
				product_from_cart.product.amount_sold -= product_from_cart.cant
			cart.delete()

			return Response({"Cart": None, "Coupon": None}, status=status.HTTP_200_OK)
		except:
			return Response({"Cart": None}, status=status.HTTP_400_BAD_REQUEST)









class AddCoupon(APIView):

	# Retrieve cart and add Coupon
	def post(self, request, token, format=None):
		data = request.data

		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

		if x_forwarded_for:
			ipaddress = x_forwarded_for.split(',')[-1].strip()
		else:
			ipaddress = request.META.get('REMOTE_ADDR')

		try:
			cart = Cart.objects.get(ip_address = ipaddress, last=True, token = token)

			user_email = data['user_email']
			code = data['code']
			if Coupon.objects.filter(user_email = user_email, code=code, taken=False).first() != None:
				coupon = Coupon.objects.get(user_email = user_email, code=code, taken=False)
				coupon.taken=True
				coupon.cart = cart
				coupon = coupon.save()
				coupon_serializer = CouponSerializer(coupon, context={"request": request}).data
				cart = CartSerializer(cart, context={"request": request}).data
				return Response({"Message": "Success", "Cart": cart, "Coupon": coupon_serializer},
								status=status.HTTP_200_OK)
			else:
				cart = CartSerializer(cart, context={"request": request}).data
				return Response({"Message": "Success", "Cart": cart, "Coupon": None}, status=status.HTTP_200_OK)
		except:
			return Response({"Message": "Success", "Cart": None}, status=status.HTTP_400_BAD_REQUEST)















class ProductVariationListView(ListAPIView):
	authentication_classes = []
	serializer_class = ProductVariationSerializer
	model = ProductVariation
	queryset = ProductVariation.objects.all()

	def get_serializer_context(self):
		context = super(ProductVariationListView, self).get_serializer_context()
		context.update({"request": self.request})
		return context




class ProductVariationView(APIView):

	# Retrieve product variation using id
	def get(self, request, id, format=None):
		product = ProductVariation.objects.get(id = id)
		product = ProductVariationSerializer(product, context={"request":request}).data
		return Response({"Product": product}, status=status.HTTP_200_OK)

	# Update product variation
	def post(self, request, id, format=None):
		data = request.data
		original_product = ProductVariation.objects.get(id=id)
		original_price = original_product.price
		product = ProductVariationSimpleSerializer(original_product, data=data, context={"request":request}, partial=True)
		if product.is_valid():
			product = product.save()
			cart = product.cart
			cart.cost = cart.cost + (product.price - original_price)
			cart.save()

			if Coupon.objects.filter(cart=cart).first() != None:
				coupon = Coupon.objects.get(cart=cart)
				coupon_serializer = CouponSerializer(coupon, context={"request": request}).data
			else:
				coupon = None
				coupon_serializer = None

			cart = CartSerializer(cart, context={"request": request}).data
			return Response({"Cart": cart, "Coupon": coupon_serializer}, status=status.HTTP_200_OK)
		else:
			return Response({"Cart": None, "Coupon": None}, status=status.HTTP_400_BAD_REQUEST)


	# delete product from cart
	def delete(self, request, id, format=None):
		product = ProductVariation.objects.get(id = id)
		cart = product.cart
		product.product.amount_sold -= product.cant
		cart.cost = cart.cost - product.price
		cart.save()
		product.save()
		product.delete()
		if Coupon.objects.filter(cart=cart).first() != None:
			coupon = Coupon.objects.get(cart=cart)
			coupon_serializer = CouponSerializer(coupon, context={"request": request}).data
		else:
			coupon = None
			coupon_serializer = None
		cart = CartSerializer(cart, context={"request": request}).data
		return Response({"Cart": cart, "Coupon": coupon_serializer}, status=status.HTTP_200_OK)







class CheckoutView(APIView):

	def post(self, request, cart_token, format=None):

		try:
			x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

			if x_forwarded_for:
				ipaddress = x_forwarded_for.split(',')[-1].strip()
			else:
				ipaddress = request.META.get('REMOTE_ADDR')
			
			cart = Cart.objects.get(ip_address = ipaddress, last=True, token=cart_token)
			order = Order.objects.create(cart=cart)

			order_serializer = OrderSerializer(order, data=request.data['order'], partial=True, context={"request":request})

			order_serializer.is_valid(raise_exception=True)
			order = order_serializer.save()

			card_num = request.data['card_num']
			exp_month = request.data['exp_month']
			exp_year = request.data['exp_year']
			cvc = request.data['cvc']

			token = stripe.Token.create(
				card={
					"number": card_num,
					"exp_month": int(exp_month),
					"exp_year": int(exp_year),
					"cvc": cvc
				},
			)

			amount = int(order.get_total_price())


			if Coupon.objects.filter(cart=cart).first() != None:
				coupon = Coupon.objects.get(cart=cart)
				items_in_cart = ProductVariation.objects.filter(cart=cart).values('cant')
				amount_of_items = 0
				for item in items_in_cart:
					amount_of_items += item['cant']
				if amount_of_items >= coupon.how_many_items:
					if coupon.discount_type == "POR CIENTO":
						amount = amount - (amount * coupon.discount)
					else:
						amount = amount - (coupon.discount)

			amount = int((amount + (amount * 0.07)) * 100)

			charge = stripe.Charge.create(
				amount=amount,
				currency="usd",
				source=token
			)


			stripe_charge_id = charge['id']
			amount = amount/100
			payment = Payment(email = order.email, ip_address=order.cart.ip_address, stripe_charge_id=stripe_charge_id, amount=amount)
			payment.save()
			order.ordered = True
			order.payment = payment
			order.save()
			cart.last = False
			cart.save()

			return Response({"Result": "Success"}, status=status.HTTP_200_OK)


		except stripe.error.CardError as e:
			return Response({"Result":"Error with card during payment"}, status=status.HTTP_400_BAD_REQUEST)

		except stripe.error.RateLimitError as e:
			return Response({"Result":"Rate Limit error during payment"}, status=status.HTTP_400_BAD_REQUEST)

		except stripe.error.InvalidRequestError as e:
			return Response({"Result":"Invalid request error during payment"}, status=status.HTTP_400_BAD_REQUEST)

		except stripe.error.AuthenticationError as e:
			return Response({"Result":"Authentication error during payment"}, status=status.HTTP_400_BAD_REQUEST)

		except stripe.error.APIConnectionError as e:
			return Response({"Result":"API connection error during payment"}, status=status.HTTP_400_BAD_REQUEST)

		except stripe.error.StripeError as e:
			return Response({"Result":"Something went wrong during payment"}, status=status.HTTP_400_BAD_REQUEST)

		except:
			return Response({"Result":"Error during payment"}, status=status.HTTP_400_BAD_REQUEST)


class ShippingInfoView(APIView):

	def post(self, request, cart_token, format=None):

		try:
			x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

			if x_forwarded_for:
				ipaddress = x_forwarded_for.split(',')[-1].strip()
			else:
				ipaddress = request.META.get('REMOTE_ADDR')

			cart = Cart.objects.get(ip_address=ipaddress, last=True, token=cart_token)


			try:
				order = Order.objects.get(cart=cart)
				order_serializer = OrderSerializer(order, data=request.data['order'], partial=True,
												   context={"request": request})

				order_serializer.is_valid(raise_exception=True)
				order = order_serializer.save()
				return Response({"Result": "Success"}, status=status.HTTP_200_OK)
			except:

				order = Order.objects.create(cart=cart)


				order_serializer = OrderSerializer(order, data=request.data['order'], partial=True,
												   context={"request": request})

				order_serializer.is_valid(raise_exception=True)
				order = order_serializer.save()
				return Response({"Result": "Success"}, status=status.HTTP_200_OK)

		except:
			return Response({"Result":"Error during payment"}, status=status.HTTP_400_BAD_REQUEST)





class OderCheckoutPaypalView(APIView):

	def post(self, request, cart_token, format=None):


		try:
			x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

			if x_forwarded_for:
				ipaddress = x_forwarded_for.split(',')[-1].strip()
			else:
				ipaddress = request.META.get('REMOTE_ADDR')

			cart = Cart.objects.get(ip_address=ipaddress, last=True, token=cart_token)
			order = Order.objects.get(cart=cart)
			stripe_charge_id = request.data['online_payment_id']
			amount = float(request.data['amount'])
			if not order.email:
				order.email="None"
				order.save()
			payment = Payment(email=order.email, ip_address=order.cart.ip_address, stripe_charge_id=stripe_charge_id,
							  amount=amount)

			payment.save()
			order.ordered = True
			order.payment = payment
			order.save()
			cart.last = False
			cart.save()
			return Response({"Result": "Success"}, status=status.HTTP_200_OK)

		except:
			return Response({"Result":"Error during payment"}, status=status.HTTP_400_BAD_REQUEST)