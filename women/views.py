# from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy  # в качестве главной

#  страницы мы бы хотели отобразить некоторый
# шаблон с именем index.html. Для этого, вначале
#  нам нужно импортировать встроенный в Django шаблонизатор.
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import CreateView, FormView
from women.forms import *
from women.models import Category, Women
from django.views.generic import ListView, DetailView


from django.contrib.auth.forms import UserCreationForm


from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView

# Create your views here.




class WomenHome(DataMixin, ListView):

    model = Women
    template_name = "women/index.html"
    context_object_name = "posts"
    extra_context = {"title": "Главная страница"}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items()))
        return context
 

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related("cat")


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = "women/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context["post"])
        return dict(list(context.items()) + list(c_def.items()))




def about(request):
    return render(request, "women/about.html", {"title": "Галерея"})





class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("home")
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")

        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = "women/contact.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect("home")





def about(request):
    return render(request, "women/about.html", {"menu": menu, "title": "О сайте"})

class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(
            cat__slug=self.kwargs["cat_slug"], is_published=True
        ).select_related("cat")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs["cat_slug"])
        c_def = self.get_user_context(
            title="Категория - " + str(c.name), cat_selected=c.pk
        )

        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):

    form_class = UserCreationForm
    template_name = "women/register.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = "women/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy("home")


def logout_user(request):
    logout(request)
    return redirect("login")
