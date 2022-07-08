"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from .rest_serializer import UserList, UserDetails, GroupList, PostList, PostDetails

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('blog/', include('blog.urls')),
]

#Add URL maps to redirect the base URL to our application
urlpatterns += [
    path('', RedirectView.as_view(url='/blog/', permanent=True)),
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

# Use static() to add url mapping to serve static files during development (only)
urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Setup the URLs and include login URLs for the browsable API.
urlpatterns += [
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/', UserList.as_view()),
    path('users/<pk>/', UserDetails.as_view()),
    path('groups/', GroupList.as_view()),
    path('posts/', PostList.as_view()),
    path('posts/<pk>/', PostDetails.as_view()),
]