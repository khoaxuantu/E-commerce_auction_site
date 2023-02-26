from django.contrib.auth.models import AbstractUser
from django.db import models


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/images/user_<id>/<filename>
    return 'images/user_{0}/{1}'.format(instance.seller.id, filename)


class Categories(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.id}: {self.name}"


class AbstractProduct(models.Model):
    """
    An abstract class implementing the product's detail information.
    """
    prod_name = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    price_base = models.DecimalField(max_digits=19, decimal_places=4)
    price_cur = models.DecimalField(max_digits=19, decimal_places=4)
    seller = models.ForeignKey("User", on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_prod_selling")
    image_path = models.ImageField(upload_to=user_directory_path, blank=False, verbose_name="Image path")
    description = models.TextField(blank=True)

    category = models.ManyToManyField(Categories, related_name="%(app_label)s_%(class)s_prod_categories", blank=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.seller.id}_{self.seller.username}_{self.prod_name}"
    

class Product(AbstractProduct):
    """
    A product class that is used as active products,
    """
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Product._meta.fields]
    

class ArchiveProduct(AbstractProduct):
    """
    A class implementing the detail information of the archive product
    which is inactive (i.e has been sold). It inherits the fields of
    the Product class.
    """
    winner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="win_prod", blank=True, null=True)
    date_sold = models.DateTimeField(auto_now_add=True)
    active_product_id = models.BigIntegerField()

    class Meta():
        db_table = "auctions_archive_product"


class User(AbstractUser):
    """
    A class implementing the user's detail information.

    Allmost the fields are inherited by the AbstractUser class, except
    watchlist, comments and bidings which are created to connect the many-to-many 
    relationship with Product.
    """
    watchlist = models.ManyToManyField(Product, through='Watchlist', related_name="prod_watchlist")
    comments = models.ManyToManyField(Product, through='Comments', related_name="prod_cmt")
    bidings = models.ManyToManyField(Product, through='Bidinglist', related_name="prod_biding")

    def __str__(self) -> str:
        return f"{self.id}_{self.username}_{self.email}"


class Bidinglist(models.Model):
    """
    An extra field on the many-to-many relationship between User and Product,
    representing the user's biding list.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid_set")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prod_bid_set")
    bid_price = models.DecimalField(max_digits=19, decimal_places=4, default=None)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user}: -- {self.product}"


class Watchlist(models.Model):
    """
    An extra field on the many-to-many relationship between User and Product,
    representing the watchlist.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watch_set")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prod_watch_set")

    def __str__(self) -> str:
        return f"{self.user}: -- {self.product}"


class Comments(models.Model):
    """
    An extra field on the many-to-many relationship between User and Product,
    representing the comments.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_cmt_set")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prod_cmt_set")
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} <{self.id}> {self.product}"