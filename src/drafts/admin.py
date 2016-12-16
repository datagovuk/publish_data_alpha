from django.contrib import admin

from drafts.models import Dataset, Datafile


class DatafileInline(admin.TabularInline):
    model = Datafile


class DatasetAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [DatafileInline]


admin.site.register(Dataset, DatasetAdmin)
