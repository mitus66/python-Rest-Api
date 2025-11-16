from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'quotes_app'  # Простір імен для URL-ів

urlpatterns = [
    # Загальнодоступні сторінки
    path('', views.index, name='index'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),

    # Автентифікація користувача
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Сторінки, що вимагають входу
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
]
