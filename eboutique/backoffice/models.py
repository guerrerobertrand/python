from django.db import models
from django.utils import timezone


PRODUCT_STATUS = (
    (0, 'Offline'),
    (1, 'Online'),
    (2, 'Out of stock')
)

class Product(models.Model):
    """
    Produit : prix, code, etc.
    """

    class Meta:
        verbose_name = "Produit"

    name          = models.CharField(max_length=100)
    code          = models.CharField(max_length=10, null=True, blank=True, unique=True)
    price_ht      = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Prix unitaire HT")
    price_ttc     = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Prix unitaire TTC")
    status        = models.SmallIntegerField(choices=PRODUCT_STATUS, default=0)
    date_creation =  models.DateTimeField(default=timezone.now(),blank=True, verbose_name="Date création")

    def __unicode__(self):
        return u"{0} [{1}]".format(self.name, self.code)

class ProductItem(models.Model):
    """
    Déclinaison de produit déterminée par des attributs comme la couleur, etc.
    """

    class Meta:
        verbose_name = "Déclinaison Produit"

    product     = models.ForeignKey('Product', related_name="product_item")
    code        = models.CharField(max_length=10, null=True, blank=True, unique=True)
    code_ean13  = models.CharField(max_length=13)
    attributes  = models.ManyToManyField("ProductAttributeValue", related_name="product_item", null=True, blank=True)

    def __unicode__(self):
        return u"{0} [{1}]".format(self.product.name, self.code)

class ProductAttribute(models.Model):
    """
    Attributs produit
    """

    class Meta:
        verbose_name = "Attribut"

    name =  models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class ProductAttributeValue(models.Model):
    """
    Valeurs des attributs
    """

    class Meta:
        verbose_name = "Valeur attribut"
        ordering = ['position']

    value              = models.CharField(max_length=100)
    product_attribute  = models.ForeignKey('ProductAttribute', verbose_name="Unité")
    position           = models.PositiveSmallIntegerField("Position", null=True, blank=True)

    def __unicode__(self):
        return u"{0} [{1}]".format(self.value, self.product_attribute)