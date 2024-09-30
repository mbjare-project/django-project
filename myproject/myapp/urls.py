from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('market-overview/', views.market_overview, name='market_overview'),
    path('stock-screener/', views.stock_screener, name='stock_screener'),
    path('portfolio-tracker/', views.portfolio_tracker, name='portfolio_tracker'),
    path('news/', views.news, name='news'),
    path('nifty_50/', views.nifty_50_view, name='nifty_50'),
    path('nifty-bank/', views.nifty_bank_view, name='nifty_bank'),
    path('upload/', views.upload_post, name='upload_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
      # Include your app's URLs
]
