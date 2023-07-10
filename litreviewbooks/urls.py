"""
URL configuration for litreviewbooks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import bookreview.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        LoginView.as_view(
            template_name="authentication/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", authentication.views.signup_page, name="signup"),
    path("home/", bookreview.views.home, name="home"),
    path("ticket/create/", bookreview.views.create_ticket, name="ticket_create"),
    path(
        "ticket/<int:tickets_pk>/edit/",
        bookreview.views.edit_ticket,
        name="ticket_edit",
    ),
    path(
        "ticket/<int:tickets_pk>/delete/",
        bookreview.views.delete_ticket,
        name="ticket_delete",
    ),
    path("review/create/", bookreview.views.create_review, name="review_create"),
    path(
        "review/<int:review_pk>/edit/", bookreview.views.edit_review, name="review_edit"
    ),
    path(
        "review/<int:review_pk>/delete/",
        bookreview.views.delete_review,
        name="review_delete",
    ),
    path(
        "review/create-as-response/<int:tickets_pk>",
        bookreview.views.create_review_as_response,
        name="review_create_as_response",
    ),
    path("my-posts/", bookreview.views.my_posts, name="my_posts"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
