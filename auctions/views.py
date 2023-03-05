from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import *
from .forms import *
import datetime


def index(request):
    """
    A route representing the index view.
    The products are displayed here.
    """
    products = Product.objects.all().order_by('date_created')
    # print(products.values_list('id', flat=True))
    return render(request, "auctions/index.html", {
        "products": products
    })


def login_view(request):
    """
    A route representing the login view.
    """
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
    """
    A route representing the logout view
    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """
    A route representing the register view
    """
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
def categories_view(request):
    """
    A route representing the categories view.
    All categories are passed to the corresponding template which
    navigate to the list of each category.
    """
    categories_list = Categories.objects.all().order_by('name')
    return render(request, "auctions/category.html", {
        "categories": categories_list
    })


@login_required
def categories(request, category_id):
    """
    A route representing the list of each category.
    The category info is queried by category_id, then it calls to the
    reversed object 'prod_categories' to collect the product list.
    """
    category_info = Categories.objects.get(pk=category_id)
    product_list = category_info.auctions_product_prod_categories.all().order_by("date_created")

    return render(request, "auctions/index.html", {
        "category": category_info.name,
        "products": product_list
    })


@login_required
def add_comment(request, product_id):
    """
    The route representing the adding-comment view.
    """
    if request.method == "POST":
        # Collect required info
        product_detail = Product.objects.filter(pk=product_id).first()
        profile = request.user
        # Initialize a new object Comments
        pre_cmt = Comments(user=profile, 
                           product=product_detail,
                           date_added=datetime.datetime.now())
        # Integrate with the CommentForm collected by request
        new_cmt = CommentForm(request.POST, instance=pre_cmt)
        new_cmt.save()
    messages.success(request, 'Comment added.')
    return HttpResponseRedirect(reverse('listings', args=(product_id,)))


@login_required
def create_listing(request):
    """
    A route representing the listing create view.
    """
    # Get the required info
    profile = request.user
    if request.method == "POST":
        prod = Product(seller=profile,
                       date_created=datetime.date.today())
        # Integrate with the CreateListingForm collected from the request
        form = CreateListingForm(request.POST, request.FILES, instance=prod)
        # print(prod)
        # print(request.FILES)
        price = form["price_base"].value()
        # Validate the form, if it is valid then save.
        if form.is_valid():
            # Due to there are ManyToMany relationships, the save_m2m method is required
            new_prod = form.save(commit=False)
            new_prod.price_cur = price
            new_prod.save()
            form.save_m2m()
            messages.success(request, 'Your listing is created.')
        else:
            print(form.errors)
            messages.error(request, 'Invalid input!')
            return render(request, "auctions/create_listing.html", {
                "form": form
            })

    return render(request, "auctions/create_listing.html", {
        "form": CreateListingForm()
    })


@login_required
def listing_page(request, product_id):
    """
    A route representing the active listing page.
    """
    # Get required info
    try:
        product_detail = Product.objects.get(pk=product_id)
    except:
        return HttpResponse("404 Not Found!")
    profile = request.user
    bidding_list = Bidinglist.objects.filter(product_id=product_id).order_by('-bid_price')
    in_watchlist = Watchlist.objects.filter(product_id=product_id, user_id=profile.id)
    comments = Comments.objects.filter(product_id=product_id)

    # Check if there are any bids of the product. Initialize a 'firstBid' flag
    # that will be passed to the template. This flag is used to determine if the 
    # client is leading the bid.
    if bidding_list.count() != 0:
        firstBid = bidding_list.first().user.id == profile.id
    else:
        firstBid = False

    # Add a new bid
    if request.method == "POST":
        new_init_bid = Bidinglist(user=profile, product=product_detail, 
                             bid_time= datetime.date.today())
        new_bid = BidForm(request.POST, instance=new_init_bid)

        if new_bid.is_valid():
            new_price = Decimal(new_bid['bid_price'].value())
            # If the price is less than the current bid
            if new_price < product_detail.price_cur or \
                (bidding_list.count() != 0 and new_price <= bidding_list.first().bid_price):
                messages.error(request, 'Your bid must be larger than the current bid.')
                return HttpResponseRedirect(reverse('listings', args=(product_id,)))
            # Else save the new bid
            if bidding_list.count() == 0 or new_price > bidding_list.first().bid_price:
                product_detail.price_cur = new_price
                product_detail.save()
            new_bid.save()
            messages.success(request, 'Place bid successfully!')
            return HttpResponseRedirect(reverse('listings', args=(product_id,)))
        else:
            print(new_bid.errors)
            messages.error(request, 'Invalid bid!')
            return render(request, "auctions/listings.html", {
                "product": Product.objects.get(pk=product_id),
                'bidform': new_bid,
                "bids": Bidinglist.objects.filter(product_id=product_id),
                "in_watchlist": in_watchlist,
                "comments": comments,
                "comment_form": CommentForm(),
                "first_bid": firstBid
            })

    return render(request, "auctions/listings.html", {
        "product": product_detail,
        'bidform': BidForm(),
        'bids': bidding_list,
        "in_watchlist": in_watchlist,
        "comments": comments,
        "comment_form": CommentForm(),
        "first_bid": firstBid
    })


@login_required
def close_bid(request, product_id, winner_id):
    """
    A route representing bid closing navigation.
    The active product will be removed from the Product table and add to 
    the Archive_Product table
    """
    product_detail = Product.objects.get(pk=product_id)
    # If a user closes the listing without a bid
    if winner_id == 0:
        product_detail.delete()
        return HttpResponseRedirect(reverse('index'))
    winner = User.objects.get(pk=winner_id)
    categories = product_detail.category.all()

    # Initialize a new ArchiveProduct object then update it with the product
    new_archive_prod = ArchiveProduct(active_product_id=product_id,
                                      date_sold=datetime.datetime.now(),
                                      winner=winner)
    new_archive_prod.__dict__.update(product_detail.__dict__)
    new_archive_prod.save()
    new_archive_prod.category.add(*categories)
    
    # Delete the product from the active product table
    product_detail.delete()

    messages.info(request, f'Listing closed! The winner is {winner.username}\
                   (id: {winner.id})')
    return HttpResponseRedirect(reverse('archive product', args=(product_id,)))


@login_required
def archive_view(request, product_id):
    """
    A route representing the archive product view.
    """
    # Retrieve the archive product info and pass to the template
    try:
        product_detail = ArchiveProduct.objects.get(active_product_id=product_id)
    except:
        return HttpResponse("404 Not Found!")
    comments = Comments.objects.filter(product_id=product_id)

    return render(request, "auctions/archive.html", {
        "product": product_detail,
        "comments": comments
    })


@login_required
def watchlist_page(request):
    """
    A route representing the watchlist page.
    A watchlist is retrieved by filtering the Watchlist table with the user's id, then
    collect products from the Product table that correspond with the watchlist's product_id
    """
    profile = request.user
    watchlist = Watchlist.objects.filter(user_id=profile.id)
    prods = Product.objects.filter(pk__in=watchlist.values('product_id'))
    
    return render(request, "auctions/index.html", {
        "products": prods,
        "watchlist": True
    })


@login_required
def addto_watchlist(request, product_id):
    """
    A route representing the add-to watchlist navigation.
    """
    product_detail = Product.objects.get(pk=product_id)
    profile = request.user

    profile.watchlist.add(product_detail)
    messages.success(request, 'Added to your watchlist!')
    return HttpResponseRedirect(reverse('listings', args=(product_id,)))


@login_required
def delete_from_watchlist(request, product_id, user_id):
    """
    A route representing the unwatch navigation.
    """
    watchlist_record = Watchlist.objects.filter(product_id=product_id, user_id=user_id)
    watchlist_record.delete()

    messages.info(request, 'Removed from your watchlist!')
    return HttpResponseRedirect(reverse('listings', args=(product_id,)))
