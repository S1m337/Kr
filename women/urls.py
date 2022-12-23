from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path("",(WomenHome.as_view()), name="home"),  # главная страница
    path("about/", about, name="about"),
    path("addpage/", AddPage.as_view(), name="add_page"),
    path("contact/", ContactFormView.as_view(), name="contact"),
    path("login/", LoginUser.as_view(), name="login"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("post/<slug:post_slug>/", ShowPost.as_view(), name="post"),
    path("category/<slug:cat_slug>/", WomenCategory.as_view(), name="category"),
    path("logout/", logout_user, name="logout"),
    # связать  функции представления всех страниц с соответствующим URL-адресом
    
]
