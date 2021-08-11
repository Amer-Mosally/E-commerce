from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required 
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import *
from .forms import  PostForm,CommentForm



class index(ListView):
    model = Listing
    template_name = 'index.html'
    ordering = ['-id']

class newListing(CreateView):
    model = Listing
    template_name = 'auctions/createListing.html'
    #fields = '__all__'         # insted of "form_class" we can controll the fields
    #fields = ('item','category','description','starting_bid','image')
    form_class = PostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class edit(UpdateView):
    model = Listing
    template_name = 'auctions/edit.html'
    form_class = PostForm

class delete(DeleteView):
    model = Listing
    template_name = 'auctions/delete.html'
    success_url = reverse_lazy('index')

class CommentView(CreateView):
    model = Comment

    template_name = 'auctions/Comment.html'
    form_class = CommentForm
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

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
            register.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def category(request, cats):
    category_posts = Listing.objects.filter(category=cats)
    return render(request, "auctions/category.html", {'cats':cats, 'category_posts':category_posts}) #{'cats':cats ::: to pass the variable 

@login_required
def watchlist(request):
    user = User.objects.get(username=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": user.watchlist.all()
    })

@login_required
def detail(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    l = Listing.objects.filter(id = listing_id).first()
    b = Bid.objects.filter(auction = l)
    highest_bid = l.price
    winner = ''

    if request.method == "POST":
        user = User.objects.get(username=request.user)
        if request.POST.get("button") == "Watchlist": 
            if user.watchlist.filter(listing= listing):
                user.watchlist.filter(listing=listing).delete()
            else:
                watchlist = Watchlist()
                watchlist.user = user
                watchlist.listing = listing
                watchlist.save()
            return HttpResponseRedirect(reverse('DetailView', args=(listing.id,)))
    if b is not None:
        for bid in b:
            if bid.price > highest_bid:
                highest_bid = bid.price
                winner = request.user
                   
    if request.method == 'POST' or request.method == 'GET':
        value = request.POST.get('bid_price', None)
        user = request.user
        listing = Listing.objects.filter(id = listing_id).first()
        if value is not None:
            if int(value) < highest_bid:
                return HttpResponseRedirect(reverse('DetailView', args = [listing_id]))
            b = Bid.objects.create(price = int(value), user = user, auction = listing)
            b.save()
            bs = Bid.objects.filter(auction = listing).exclude(price = value)
            bs.delete()
            return HttpResponseRedirect(reverse('DetailView', args = [listing_id]))
        
    return render(request, "auctions/details.html", {
        "listing": l,
        "highest_bid": highest_bid,
        "winner": winner,
    })


@login_required
def close(request, listing):
    list = Listing.objects.filter(id = listing).first()
    bid = Bid.objects.filter(auction = list).first()
    
    if list.owner == request.user and not bid is None:
        list.closed = True
        list.winner = bid.user
        list.save()
        return HttpResponseRedirect(reverse('index'))
    elif list.owner == request.user and bid is None:
        list.closed = True
        list.winner = bid.user
        list.save()
        return HttpResponseRedirect(reverse('index'))