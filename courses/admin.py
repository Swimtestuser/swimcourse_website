from django.contrib import admin
from .models import Equipment, Exercise, Favorite, Subscription, SwimStyle, VideoAsset
@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("title", "swim_style", "published")
    list_filter = ("swim_style", "equipment", "published")
    search_fields = ("title", "description")
admin.site.register([Equipment, Favorite, Subscription, SwimStyle, VideoAsset])
