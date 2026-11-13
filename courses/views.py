from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Equipment, Exercise, Favorite, SwimStyle

def register(request):
    if request.user.is_authenticated:
        return redirect("exercise_list")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("exercise_list")
    return render(request, "registration/register.html", {"form": form})

@login_required
def exercise_list(request):
    exercises = Exercise.objects.filter(published=True).select_related("swim_style").prefetch_related("equipment")
    style = request.GET.get("style", "")
    equipment = request.GET.get("equipment", "")
    if style.isdigit():
        exercises = exercises.filter(swim_style_id=int(style))
    if equipment.isdigit():
        exercises = exercises.filter(equipment__id=int(equipment))
    exercises = exercises.distinct()
    favorite_ids = set(Favorite.objects.filter(user=request.user).values_list("exercise_id", flat=True))
    return render(request, "courses/list.html", {
        "exercises": exercises, "styles": SwimStyle.objects.all(), "equipment_options": Equipment.objects.all(),
        "selected_style": style, "selected_equipment": equipment, "favorite_ids": favorite_ids,
    })

@login_required
def favorites(request):
    exercises = Exercise.objects.filter(published=True, favorited_by__user=request.user).select_related("swim_style")
    return render(request, "courses/favorites.html", {"exercises": exercises})

@login_required
@require_POST
def toggle_favorite(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk, published=True)
    favorite, created = Favorite.objects.get_or_create(user=request.user, exercise=exercise)
    if not created:
        favorite.delete()
    return redirect(request.POST.get("next") if request.POST.get("next", "").startswith("/") and not request.POST.get("next", "").startswith("//") else "exercise_list")
