from django.conf import settings
from django.db import models

class SwimStyle(models.Model):
    name = models.CharField(max_length=80, unique=True)
    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=80, unique=True)
    def __str__(self):
        return self.name

class VideoAsset(models.Model):
    title = models.CharField(max_length=200)
    private_hls_path = models.CharField(max_length=500, blank=True, help_text="Private storage key; never a public URL")
    duration_seconds = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title

class Exercise(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    swim_style = models.ForeignKey(SwimStyle, on_delete=models.PROTECT, related_name="exercises")
    equipment = models.ManyToManyField(Equipment, blank=True, related_name="exercises")
    video = models.OneToOneField(VideoAsset, on_delete=models.SET_NULL, null=True, blank=True)
    published = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exercise_favorites")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "exercise"], name="unique_user_exercise_favorite")]

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    stripe_customer_id = models.CharField(max_length=120, blank=True, db_index=True)
    stripe_subscription_id = models.CharField(max_length=120, unique=True)
    status = models.CharField(max_length=40, default="incomplete")
    current_period_end = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.user_id}: {self.status}"
