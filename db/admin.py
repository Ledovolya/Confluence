from django.contrib import admin
import db.models

admin.site.register(db.models.components)
admin.site.register(db.models.Bug)
# Register your models here.
