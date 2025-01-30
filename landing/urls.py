from django.urls import path
from landing.views import Index
from django.contrib.auth.views import LogoutView  # Import the LogoutView

urlpatterns = [
    path('', Index.as_view(), name='index'),  # Your existing index path
    path('logout/', LogoutView.as_view(), name='logout'),  # Add the logout path
]
