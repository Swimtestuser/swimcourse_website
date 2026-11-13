from django.contrib import admin
from django.urls import path, include
from courses import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("", views.exercise_list, name="exercise_list"),
    path("favorites/", views.favorites, name="favorites"),
    path("favorites/<int:pk>/toggle/", views.toggle_favorite, name="toggle_favorite"),
]
