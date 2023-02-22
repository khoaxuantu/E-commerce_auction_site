from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="create listing"),
    path("listings/<int:product_id>", views.listing_page, name="listings"),
    path("category/<int:category_id>", views.catgories, name="category"),
    path("addtowatchlist/<int:product_id>", views.addto_watchlist, name="add to watchlist"),
    path("unwatch/<int:product_id>/<int:user_id>", views.delete_from_watchlist, name="unwatch")
]
