"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import authentication.views
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),

    path('home/', blog.views.home, name='home'),
    path('ticket/create/', blog.views.ticket_create, name='ticket_create'),
    path('review/create/', blog.views.review_and_ticket_create, name='review_and_ticket_create'),
    path('review/ticket<int:ticket_id>/create/', blog.views.review_specific_ticket_create, name='review_specific_ticket_create'),
    path('posts/', blog.views.posts, name="posts"),
    path('posts/ticket<int:ticket_id>/edit/', blog.views.ticket_edit, name='ticket_edit'),
    path('posts/ticket<int:ticket_id>/delete/', blog.views.ticket_delete, name='ticket_delete'),
    path('posts/review<int:review_id>/edit/', blog.views.review_edit, name='review_edit'),
    path('posts/review<int:review_id>/delete/', blog.views.review_delete, name='review_delete'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
