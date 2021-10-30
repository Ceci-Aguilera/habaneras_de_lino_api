from django.db import models

# Create your models here.

class Product(models.Model):
	title = models.CharField(max_length=256, default='')
	price = models.FloatField(default=0.0)
	image = models.ImageField(upload_to='uploads/products/')

	def __str__(self):
		return self.title


class Category(models.Model):
	title = models.CharField(max_length=256, default='')
	products = models.ManyToManyField(Product, blank=True)
	image = models.ImageField(upload_to='uploads/categories/', blank=True)

	class Meta:
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.title


class Cart(models.Model):
	ip_address = models.GenericIPAddressField()
	cost = models.FloatField(default=0)
	last = models.BooleanField(default=False)

	def __str__(self):
		return self.ip_address

class ProductVariation(models.Model):
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	cant = models.IntegerField(default=1)
	cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL, related_name="product_variation_set")
	price = models.FloatField(default=0)
	clothing_s = models.CharField(max_length=256, default="S")

	def __str__(self):
		if self.product is not None:
			return self.product.title
		else:
			return "No product can be viewed now"

