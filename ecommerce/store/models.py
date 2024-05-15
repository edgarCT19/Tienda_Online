from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)  # Hacer el nombre opcional
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # Campo adicional para el número de teléfono
    
    def __str__(self):
        return self.name if self.name else self.email
 
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    mark = models.CharField(max_length=100, null=True)
    price = models.FloatField()
    quantity = models.IntegerField(null=True)
    oferta = models.BooleanField(default=False, null=True, blank=False)
    description = models.TextField(max_length=1000, null=True)
    qualityuno = models.CharField(max_length=200, null=True)
    qualitydos = models.CharField(max_length=200, null=True)
    qualitytres = models.CharField(max_length=200, null=True)
    qualitycuatro = models.CharField(max_length=200, null=True)
    qualitycinco = models.CharField(max_length=200, null=True)
    qualityseis = models.CharField(max_length=200, null=True)
    qualitysiete = models.CharField(max_length=200, null=True)
    qualityocho = models.CharField(max_length=200, null=True)
    qualitynueve = models.CharField(max_length=200, null=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    SECTION_CHOICES = [
    ('MEMORIAS', 'MEMORIAS'),
    ('ALMACENAMIENTO', 'ALMACENAMIENTO'),
    ('PROCESADORES', 'PROCESADORES'),
    ('GABINETES', 'GABINETES'),
    ('MOUSES', 'MOUSES'),
    ('VENTILADORES', 'VENTILADORES'),
    ('MONITORES', 'MONITORES'),
    ('TECLADOS', 'TECLADOS'),
    ('TECLADOS GAMER', 'TECLADOS GAMER'),
    ('TARJETAS GRÁFICAS', 'TARJETAS GRÁFICAS'),
    ('TARJETAS MADRES', 'TARJETAS MADRES'),
    ('TARJETAS DE RED', 'TARJETAS DE RED'),
    # Agrega más opciones según sea necesario
    ]
    section = models.CharField(max_length=200, choices=SECTION_CHOICES, null=True)
    image = models.ImageField(null=True, blank=False)
    imageuno = models.ImageField(null=True, blank=False)
    imagedos = models.ImageField(null=True, blank=False)
    imagetres = models.ImageField(null=True, blank=False)
    imagecuatro = models.ImageField(null=True, blank=False)
    imagecinco = models.ImageField(null=True, blank=False)
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    @property
    def imageunoURL(self):
        try:
            url = self.imageuno.url
        except:
            url = ''
        return url
    
    @property
    def imagedosURL(self):
        try:
            url = self.imagedos.url
        except:
            url = ''
        return url
    
    @property
    def imagetresURL(self):
        try:
            url = self.imagetres.url
        except:
            url = ''
        return url
    
    @property
    def imagecuatroURL(self):
        try:
            url = self.imagecuatro.url
        except:
            url = ''
        return url
    
    @property
    def imagecincoURL(self):
        try:
            url = self.imagecinco.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if not i.product.digital:
                shipping = True
        return shipping

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Order History for {self.user.username}"
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
    
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)