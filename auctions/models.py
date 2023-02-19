from django.contrib.auth.models import AbstractUser
from django.db import models


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/images/user_<id>/<filename>
    return 'images/user_{0}/{1}'.format(instance.seller, filename)


class Categories(models.Model):
    name = models.CharField(max_length=64)


class Product(models.Model):
    """
    A class implementing the product's detail information.
    """
    prod_name = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    price_base = models.PositiveIntegerField()
    price_cur = models.PositiveIntegerField()
    bids = models.PositiveIntegerField()
    seller = models.ForeignKey("User", on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to=user_directory_path, blank=False, verbose_name="Image path")
    description = models.TextField(blank=True)

    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.seller.id}_{self.seller.username}_{self.prod_name}"
    

class User(AbstractUser):
    """
    A class implementing the user's detail information.

    Allmost the fields are inherited by the AbstractUser class, except
    auc_list and watchlist which are used to connect the many-to-many 
    relationship with Product.
    """
    watchlist = models.ManyToManyField(Product, through='Watchlist', related_name="prod_watchlist")
    comments = models.ManyToManyField(Product, through='Comments', related_name="prod_cmt")

    def __str__(self) -> str:
        return f"{self.id}_{self.username}_{self.email}"


class Watchlist(models.Model):
    """
    An extra field on the many-to-many relationship beappnametween User and Product,
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