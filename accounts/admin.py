from django.contrib import admin
from .models import AudioFile
# Register your models here.
@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')