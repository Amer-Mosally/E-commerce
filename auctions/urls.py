from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .import views
from .views import *
  

urlpatterns = [
    path('', index.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new/", newListing.as_view(), name="new_listing"),
    path("auctions/edit/<int:pk>", edit.as_view(), name="Edit_list"),
    path("auctions/delete/<int:pk>", delete.as_view(), name="Delete_list"),
    path("auctions/<int:pk>/comment", CommentView.as_view(), name="add_comment"),
    path("category/<str:cats>/>", category, name="Category"),
    path("auctions/watchlist.html", views.watchlist, name="watchlist"),
    path("auctions/bid/<int:listing_id>", views.detail, name="DetailView"),
    path("auctions/close/<str:listing>", views.close, name="close"),


    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
