from django.contrib import admin, messages

from .models import *


class Whattafuu_Filter(admin.SimpleListFilter):
    title = "Какой-то фильтр"
    parameter_name = "steel"

    def lookups(self, request, model_admin):
        return [
            ("long", "Длинная"),
            ("small", "Короткая"),
        ]

    def queryset(
        self, request, queryset
    ):  # собственно фильтр. Можно добавлять больше двух значений
        if self.value() == "long":
            return queryset.filter(steel=True)
        elif self.value() == "small":
            return queryset.filter(steel=False)


@admin.register(Metal_info)
class Metal_infoAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]
    list_display = ("steel", "steel_info", "metals_class", "count_letters")
    list_display_links = "steel", "count_letters"
    list_per_page = 218
    actions = ["something"]
    search_fields = [
        "steel",
        "metals_class__steel_class",
    ]  # metals_class внешний ключ, необходимо указать поле явно
    list_filter = [Whattafuu_Filter, "metals_class__steel_class"]
    # prepopulated_fields = {"slug": ("steel_info",)} для создание слага в админ панели, корректность не известна
    filter_horizontal = ["metalsearch"]
    save_on_top = True

    @admin.display(
        description="Количество именованных элементов в названии", ordering="steel"
    )  # сортировка только по существующему в бд
    def count_letters(self, metal_info):  # добавление столбца, отсутствующего в бд
        letters_count = 0
        for char in metal_info.steel:
            if char.isalpha():
                letters_count += 1
        return letters_count

    @admin.action(
        description="Что-то там сделать"
    )  # добавление кастомного метода для строк в бд
    def something(self, request, queryset):
        pass
        # count = queryset.update()
        # self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)


admin.site.register(Metal)
admin.site.register(Metal_2)


@admin.register(Metal_class)
class Metal_classAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]
    list_display = ("id", "steel_class")
    list_editable = ("steel_class",)


@admin.register(MetalSearch)
class MetalSearchAdmin(admin.ModelAdmin):
    readonly_fields = ["slug", "date"]
    list_display = ("id", "date")
    list_display_links = ("id", "date")
    ordering = ["date"]


admin.site.register(Metal_request)

# admin.site.register(SearchQuery)
