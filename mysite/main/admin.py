from django.contrib import admin
from .models import Tutorial, TutorialCategory, TutorialSeries
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.

class TutorialAdmin(admin.ModelAdmin):
    
    fieldsets = [
            ("Metadata", {"fields":["tutorial_title", "tutorial_series", "tutorial_slug", "tutorial_published"]}),
            ("Content", {"fields":["tutorial_content"]})
        ]
    
    formfield_overrides = {
            models.TextField: {"widget": TinyMCE()}
        }

admin.site.register(TutorialCategory)
admin.site.register(TutorialSeries)
admin.site.register(Tutorial, TutorialAdmin)

