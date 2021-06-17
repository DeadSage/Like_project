from django.contrib import admin
from .models import Bb, Rubric
from django.db.models import F


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
    radio_fields = {'rubric': admin.VERTICAL}
    actions = ('discount',)

    def discount(self, request, queryset):
        f = F('price')
        for rec in queryset:
            rec.price = f / 2
            rec.save()
        self.message_user(request, 'Действие выполнено')

    discount.short_description = 'Уменьшить цену вдвое'

    fieldsets = (
        (None, {
            'fields': (('title', 'rubric'), 'content'),
            'classes': ('wide',),
        }),
        ('Дополнительные сведения', {
            'fields': ('price',),
            'description': 'Параметры, необязательные для указания.',
        })
    )

    def get_fields(self, request, obj=None):
        f = ['title', 'content', 'price']
        if not obj:
            f.append('rubric')
        return f


class BbInline(admin.StackedInline):
    model = Bb

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 3
        else:
            return 10


class RubricAdmin(admin.ModelAdmin):
    inlines = [BbInline]


admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric, RubricAdmin)
