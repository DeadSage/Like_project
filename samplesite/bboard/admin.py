from django.contrib import admin
from .models import Bb, Rubric


class PriceListFilter(admin.SimpleListFilter):
    title = 'Категория цен'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('low', 'Низкая цена '),
            ('medium', 'Средняя цена'),
            ('high', 'Высокая цена'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(price__lt=500)
        if self.value() == 'medium':
            return queryset.filter(price__gte=500,
                                   price__lte=5000)
        if self.value() == 'high':
            return queryset.filter(price__gt=5000)


class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'rubric')
    list_display_links = ('title', 'content')
    list_filter = (PriceListFilter,)
    search_fields = ('title', 'content',)
    date_hierarchy = 'published'
    empty_value_display = '----'


admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric)
