
from __future__ import print_function

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from muddery.utils.model_utils import auto_generate_key, validate_object_key
from muddery.worlddata.model_base import SystemData, KEY_LENGTH, NAME_LENGTH, TYPECLASS_LENGTH


# ------------------------------------------------------------
#
# store all typeclasses
#
# ------------------------------------------------------------
class typeclasses(SystemData):
    """
    Defines all available typeclasses.

    The key is typeclass's key.
    """

    # the readable name of the typeclass
    name = models.CharField(max_length=NAME_LENGTH, unique=True)

    # the typeclass's path that related to a class
    path = models.CharField(max_length=TYPECLASS_LENGTH, blank=True)

    # The key of a typeclass category.
    # typeclass's category
    category = models.CharField(max_length=KEY_LENGTH)

    # typeclass's description (optional)
    desc = models.TextField(blank=True)

    # Can loot from objects of this type.
    can_loot = models.BooleanField(blank=True, default=False)

    class Meta:
        "Define Django meta options"
        verbose_name = "Typeclass"
        verbose_name_plural = "Typeclasses"

    def __unicode__(self):
        return self.name
        

# ------------------------------------------------------------
#
# shops
#
# ------------------------------------------------------------
class shops(models.Model):
    "Store all shops."

    # shop's key
    key = models.CharField(max_length=KEY_LENGTH, unique=True, blank=True)

    # The key of a shop typeclass.
    # Shop's typeclass.
    typeclass = models.CharField(max_length=KEY_LENGTH)

    # shop's name for display
    name = models.CharField(max_length=NAME_LENGTH)

    # shop's description for display
    desc = models.TextField(blank=True)

    # the verb to open the shop
    verb = models.CharField(max_length=NAME_LENGTH, blank=True)

    # condition of the shop
    condition = models.TextField(blank=True)

    # shop's icon resource
    icon = models.CharField(max_length=KEY_LENGTH, blank=True)

    class Meta:
        "Define Django meta options"
        verbose_name = "Shop"
        verbose_name_plural = "Shops"

    def clean(self):
        auto_generate_key(self)
        validate_object_key(self)


# ------------------------------------------------------------
#
# shop goods
#
# ------------------------------------------------------------
class shop_goods(models.Model):
    "All goods that sold in shops."

    # goods's key
    key = models.CharField(max_length=KEY_LENGTH, unique=True, blank=True)

    # the typeclass of this goods
    typeclass = models.CharField(max_length=KEY_LENGTH)

    # shop's key
    shop = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # the key of objects to sell
    goods = models.CharField(max_length=KEY_LENGTH)

    # number of shop goods
    number = models.PositiveIntegerField(blank=True, default=1)

    # the price of the goods
    price = models.PositiveIntegerField(blank=True, default=1)

    # the unit of the goods price
    unit = models.CharField(max_length=KEY_LENGTH)

    # visible condition of the goods
    condition = models.TextField(blank=True)

    class Meta:
        "Define Django meta options"
        verbose_name = "Shop Object"
        verbose_name_plural = "Shop Objects"

    def clean(self):
        auto_generate_key(self)
        validate_object_key(self)


# ------------------------------------------------------------
#
# store npc's shop
#
# ------------------------------------------------------------
class npc_shops(models.Model):
    "Store npc's shops."

    # The key of an NPC.
    # NPC's key
    npc = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # The key of a shop.
    # shop's key
    shop = models.CharField(max_length=KEY_LENGTH, db_index=True)

    class Meta:
        "Define Django meta options"
        verbose_name = "NPC Shop"
        verbose_name_plural = "NPC Shops"
        unique_together = ("npc", "shop")
