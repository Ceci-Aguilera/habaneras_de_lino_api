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
	cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE, related_name="product_variation_set")
	price = models.FloatField(default=0)
	clothing_s = models.CharField(max_length=256, default="S")
	size_of_sleeve = models.CharField(max_length=256, default="Corta")
	fit = models.CharField(max_length=256, default="Regular Fit")

	def __str__(self):
		if self.product is not None:
			return self.product.title
		else:
			return "No product can be viewed now"


class Payment(models.Model):
	ip_address = models.GenericIPAddressField()
	email = models.CharField(max_length=256, default='-1')
	stripe_charge_id = models.CharField(max_length=50)
	amount = models.FloatField(default=0.0)
	timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	def __str__(self):
		if ((self.email != "") and (self.email != '-1')):
			return self.email + " - " + self.timestamp.strftime("%b. %-d, %Y, %-I:%M %p")
		else:
			return str(self.ip_address) + " - " + self.timestamp.strftime("%b. %-d, %Y, %-I:%M %p")



class Order(models.Model):
	cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL, blank=True)
	email = models.CharField(max_length=256, default='-1')
	phone = models.CharField(max_length=256, default='-1')
	address1 = models.CharField(max_length=256, default='-1')
	address2 = models.CharField(max_length=256, default='-1')
	user_first_name = models.CharField(max_length=256, default='-1')
	user_last_name = models.CharField(max_length=256, default='-1')
	ordered_date = models.DateTimeField(auto_now_add=True, blank=True,null=True)
	ordered = models.BooleanField(default=False)
	payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		if ((self.email != "") and (self.email != '-1')):
			return self.email + '-' + self.ordered_date.strftime("%b. %-d, %Y, %-I:%M %p")
		else:
			return self.user_first_name + " " + self.user_last_name + " - " + self.ordered_date.strftime("%b. %-d, %Y, %-I:%M %p")

	def get_total_price(self):
		return self.cart.cost + self.cart.cost * 0.07
