from django.db import models
from datetime import datetime

# Create your models here. A model maps to a database table.
# django field reference: https://docs.djangoproject.com/en/3.0/ref/models/fields/

class TutorialCategory(models.Model):
    tutorial_category = models.CharField(max_length=200)
    category_summary = models.CharField(max_length=200)
    category_slug = models.CharField(max_length=200) # a slug is place for a url
    
    class Meta: # Anthing that is not a field name is metadata, and goes here
        verbose_name_plural = "Categories" # This sets the name that appears in admin module
    
    def __str__(self):
        return self.tutorial_category


class TutorialSeries(models.Model):
    tutorial_series = models.CharField(max_length=200)
    tutorial_category = models.ForeignKey(TutorialCategory,
                                          default=1, # required in case of deletion of a Category
                                          verbose_name="Category",
                                          on_delete=models.SET_DEFAULT)
    series_summary = models.CharField(max_length=200)
    
    class Meta:
        verbose_name_plural = "Series"
    
    def __str__(self):
        return self.tutorial_series


class Tutorial(models.Model): # Tutorial inherits from the class models.Model
    
    # Create columns for the Tutorial table
    # A primary key is created by default, although we could set it to be one of the fields
    # below if we wanted to.
    tutorial_title = models.CharField(max_length=200) # used for short strings, e.g. categories
    tutorial_content = models.TextField() # used for longer text
    tutorial_published = models.DateTimeField("date published", default=datetime.now())
    tutorial_series = models.ForeignKey(TutorialSeries,
                                          default=1, # required in case of deletion of a Series
                                          verbose_name="Series",
                                          on_delete=models.SET_DEFAULT)
    tutorial_slug = models.CharField(max_length=200,
                                     default=1) # required as we already have some tutorial instances!
    
    def __str__(self):
        return self.tutorial_title # This is what gets return when we print the instance

    
    