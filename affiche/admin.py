from dal import autocomplete
from django.contrib import admin
from grappelli import models as grappelli_models
from .forms import PerformanceCreativesForm, PerformanceConductorForm, PerformancePerformersForm
from .models import MainImages, Performers, Performance, Creatives, Conductor, Backstage, PerformanceFiles, Row, Seat, \
    Ticket, PerformancePerformers, PerformanceCreatives, PerformanceConductor


class CreativesAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']


class PerformersAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']


class BackstageAdmin(admin.ModelAdmin):
    search_fields = ['title']
    ordering = ['title']
    list_display = ["id", "title", "performance"]


class ConductorsAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']


class PerformancePerformersInline(admin.TabularInline):
    model = PerformancePerformers
    form = PerformancePerformersForm
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'performer':
            kwargs['queryset'] = Performers.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    verbose_name_plural = 'Исполнители'


class PerformanceCreativesInline(admin.TabularInline):
    model = PerformanceCreatives
    form = PerformanceCreativesForm
    extra = 0
    verbose_name_plural = 'Постановщики'


class PerformanceConductorInline(admin.TabularInline):
    model = PerformanceConductor
    form = PerformanceConductorForm
    extra = 0
    verbose_name_plural = 'Дирижер'


class PerformanceAdmin(admin.ModelAdmin):
    inlines = [
        PerformancePerformersInline,
        PerformanceConductorInline,
        PerformanceCreativesInline,
    ]
    list_display = ["title", "datetime1", "datetime2"]


admin.site.register(MainImages)
admin.site.register(Creatives, CreativesAdmin)
admin.site.register(Conductor, ConductorsAdmin)
admin.site.register(Backstage, BackstageAdmin)
admin.site.register(PerformanceFiles)
admin.site.register(Row)
admin.site.register(Seat)
admin.site.register(Ticket)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Performers, PerformersAdmin)
