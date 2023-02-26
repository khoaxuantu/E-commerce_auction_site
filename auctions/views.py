from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import *
from .forms import *
import datetime


def index(request):
    products = Product.objects.all().order_by('date_created')
    # print(products.values_list('id', flat=True))
    return render(request, "auctions/index.html", {
        "products": products
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    profile = request.user
    if request.method == "POST":
        prod = Product(seller=profile,
                       date_created=datetime.date.today())
        form = CreateListingForm(request.POST, request.FILES, instance=prod)
        # print(prod)
        print(request.FILES)
        price = form["price_base"].value()
        if form.is_valid():
            new_prod = form.save(commit=False)
            new_prod.price_cur = price
            new_prod.save()
            form.save_m2m()
        else:
            print(form.errors)
            return render(request, "auctions/create_listing.html", {
                "form": form
            })

    return render(request, "auctions/create_listing.html", {
        "form": CreateListingForm()
    })

@login_required
def listing_page(request, product_id):
    product_detail = Product.objects.get(pk=product_id)
    profile = request.user
    bidding_list = Bidinglist.objects.filter(product_id=product_id).order_by('-bid_price')
    in_watchlist = Watchlist.objects.filter(product_id=product_id, user_id=profile.id)
    comments = Comments.objects.filter(product_id=product_id, user=profile)

    if request.method == "POST":
        new_init_bid = Bidinglist(user=profile, product=product_detail, 
                             bid_time= datetime.date.today())
        new_bid = BidForm(request.POST, instance=new_init_bid)

        if new_bid.is_valid():
            new_price = Decimal(new_bid['bid_price'].value())
            if bidding_list.count() == 0 or new_price > bidding_list.first().bid_price:
                product_detail.price_cur = new_price
                product_detail.save()
            new_bid.save()
            return HttpResponseRedirect(reverse('listings', args=(product_id,)))
        else:
            print(new_bid.errors)
            return render(request, "auctions/listings.html", {
                "product": product_detail,
                'bidform': new_bid,
                "bid_count": Bidinglist.objects.filter(product_id=product_id).count(),
                "in_watchlist": in_watchlist,
                "comments": comments,
                "comment_form": CommentForm()
            })

    return render(request, "auctions/listings.html", {
        "product": product_detail,
        'bidform': BidForm(),
        'bid_count': bidding_list.count(),
        "in_watchlist": in_watchlist,
        "comments": comments,
        "comment_form": CommentForm()
    })

@login_required
def watchlist_page(request):
    profile = request.user
    watchlist = Watchlist.objects.filter(user_id=profile.id)
    prods = Product.objects.filter(pk__in=watchlist.values('product_id'))
    
    return render(request, "auctions/index.html", {
        "products": prods,
        "watchlist": True
    })


@login_required
def addto_watchlist(request, product_id):
    product_detail = Product.objects.get(pk=product_id)
    profile = request.user

    profile.watchlist.add(product_detail)

    return HttpResponseRedirect(reverse('listings', args=(product_id,)))


@login_required
def delete_from_watchlist(request, product_id, user_id):
    watchlist_record = Watchlist.objects.filter(product_id=product_id, user_id=user_id)
    watchlist_record.delete()

    return HttpResponseRedirect(reverse('listings', args=(product_id,)))


@login_required
def categories(request, category_id):
    category_info = Categories.objects.get(pk=category_id)
    product_list = category_info.prod_categories.all().order_by("date_created")

    return render(request, "auctions/index.html", {
        "category": category_info.name,
        "products": product_list
    })


def categories_view(request):
    categories_list = Categories.objects.all().order_by('name')
    return render(request, "auctions/category.html", {
        "categories": categories_list
    })


@login_required
def add_comment(request, product_id):

    if request.method == "POST":
        product_detail = Product.objects.filter(pk=product_id).first()
        profile = request.user
        pre_cmt = Comments(user=profile, 
                           product=product_detail,
                           date_added=datetime.datetime.now())
        new_cmt = CommentForm(request.POST, instance=pre_cmt)
        new_cmt.save()

    return HttpResponseRedirect(reverse('listings', args=(product_id,)))