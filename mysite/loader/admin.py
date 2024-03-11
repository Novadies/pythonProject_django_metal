from pathlib import Path

from django.contrib import admin

from loader.models import UploadFiles


@admin.register(UploadFiles)
class Upload(admin.ModelAdmin):
    readonly_fields = ["file_to_upload", 'time', "db_record"]
    list_display = ("file_to_upload", 'time', "to_user", "db_record")
    list_display_links = ('to_user',)
    search_fields = ["file_to_upload", "to_user", "db_record"]
    date_hierarchy = 'time'
    list_per_page = 104

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.file_to_upload:
                file_path = Path(obj.file_to_upload.path)
                if file_path.exists():
                    file_path.unlink()
        queryset.delete()




