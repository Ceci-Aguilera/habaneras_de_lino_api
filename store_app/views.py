from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

import json
from datetime import datetime

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework.views import APIView

from .models import *
from .serializers import *

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY







class CategoryListView(ListAPIView):
    authentication_classes = []
    serializer_class = CategorySimpleSerializer
    model = Category
    queryset = Category.objects.all()


class CategoryDetailView(RetrieveAPIView):
    authentication_classes = []
    serializer_class = CategorySerializer
    model = Category
    lookup_field = 'id'
    queryset = Category.objects.all()

class ProductListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    model = Product
    queryset = Product.objects.all()


class ProductDetailView(RetrieveAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    model = Product
    lookup_field = 'id'
    queryset = Product.objects.all()


class CartView(APIView):

	def get(self, request, format=None):
		data = request.data

		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

		if x_forwarded_for:
			ipaddress = x_forwarded_for.split(',')[-1].strip()
		else:
			ipaddress = request.META.get('REMOTE_ADDR')

		try:
			cart = Cart.objects.get(ip_address = ipaddress, last=True)
			cart = CartSerializer(cart, context={"request": request}).data
			return Response({"Cart": cart}, status=status.HTTP_200_OK)
		except:
			return Response({"Cart":"Error"}, status=status.HTTP_400_BAD_REQUEST)


	def post(self, request, format=None):
		data = request.data


		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

		if x_forwarded_for:
			ipaddress = x_forwarded_for.split(',')[-1].strip()
		else:
			ipaddress = request.META.get('REMOTE_ADDR')

		try:
			cart = Cart.objects.get(ip_address = ipaddress, last=True)
		except:
			cart = Cart(ip_address = ipaddress, cost = 0, last = True)

		product_serializer = ProductVariationSimpleSerializer(data=data, context={"request": request})
		if product_serializer.is_valid():
			
			product = product_serializer.save()
			original_product = Product.objects.get(id = data['original_product_id'])
			product.product = original_product
			product.cart = None
			product.save()

			cart.cost += product.price
			cart.save()
			product.cart = cart
			product.save()
			cart = CartSerializer(cart, context={"request": request}).data

			return Response({"Cart":cart}, status=status.HTTP_200_OK)

		else:
			return Response({"Cart": "Error"}, status=status.HTTP_400_BAD_REQUEST)



class ProductVariationListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductVariationSerializer
    model = ProductVariation
    queryset = ProductVariation.objects.all()



class ProductVariationView(APIView):

	def get(self, request, id, format=None):
		product = ProductVariation.objects.get(id = id)
		product = ProductVariationSerializer(product, context={"request":request}).data
		return Response({"Product": product}, status=status.HTTP_200_OK)

	def post(self, request, id, format=None):
		data = request.data
		original_product = ProductVariation.objects.get(id=id)
		product = ProductVariationSimpleSerializer(original_product, data=data, context={"request":request}, partial=True)
		if product.is_valid():
			product = product.save()
			return Response({"Product": "Successfuly updated"}, status=status.HTTP_200_OK)
		else:
			print(product.errors)
			return Response({"Product": product.errors}, status=status.HTTP_400_BAD_REQUEST)


	def delete(self, request, id, format=None):
		product = ProductVariation.objects.get(id = id)
		cart = product.cart
		cart = CartSerializer(cart, context={"request": request}).data
		product.delete()
		return Response({"Cart": cart}, status=status.HTTP_200_OK)
