# urls.py

from django.urls import path
from . import views
from .views import index, chambres, show_chambre
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('chambres', views.chambres, name='chambres'),
    path('chambre/<int:chambre_id>/', views.show_chambre, name='show_chambre'),
    path('create_reservation/<int:chambre_id>', views.create_reservation, name='create_reservation'),
    path('confirm_reservation/<int:chambre_id>', views.confirm_reservation, name='confirm_reservation'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    # Route pour afficher ggmap.html
    path('ggmap.html', views.ggmap_view, name='ggmap'),
]
