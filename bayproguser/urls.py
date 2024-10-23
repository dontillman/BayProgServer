from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup', views.signup, name='signup'),
    path('edit', views.edit, name='edit'),    

    #path('login', views.login, name='login'),
    # path('login', auth_views.LoginView.as_view(template_name='accounts/login.html')),
    #path('user/<int:id>', views.user, name='user'),
]

