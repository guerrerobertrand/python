#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
from django.test import TestCase

# Create your tests here.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eboutique.settings")

from django.db import models
from backoffice.models import *

# Création d'un attribut
product_attribute = ProductAttribute(name="couleur")
product_attribute.save()

# Création des valeurs des attributs
attribute1 = ProductAttributeValue(value="bleu", product_attribute=product_attribute, position=0)
attribute1.save()

attribute2 = ProductAttributeValue(value="jaune", product_attribute=product_attribute, position=0)
attribute2.save()

attribute2 = ProductAttributeValue(value="brun", product_attribute=product_attribute, position=0)
attribute2.save()

# Création du produit
product = Product(name="Tshirt", code="54065", price_ht=25, price_ttc=30)
product.save()

# Création d'une déclinaison de produit
product_item = ProductItem(product=product, code="5046", code_ean13="a1")
product_item.save()
product_item.attributes.add(attribute1)
product_item.attributes.add(attribute1)
product_item.save()