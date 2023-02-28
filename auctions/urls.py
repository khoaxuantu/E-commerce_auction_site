from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("accounts/register/", views.register, name="register"),
    path("category", views.categories_view, name="category view"),
    path("category/<int:category_id>", views.categories, name="category"),
    path("comment/<int:product_id>", views.add_comment, name="comment"),
    path("listings/create", views.create_listing, name="create listing"),
    path("listings/<int:product_id>", views.listing_page, name="listings"),
    path("listings/close/<int:product_id>/<int:winner_id>", views.close_bid, name="close bid"),
    path("listings/archive/<int:product_id>", views.archive_view, name="archive product"),
    path("watchlist", views.watchlist_page, name="watchlist"),
    path("watchlist/add/<int:product_id>", views.addto_watchlist, name="add to watchlist"),
    path("watchlist/unwatch/<int:product_id>/<int:user_id>", views.delete_from_watchlist, name="unwatch"),
]
