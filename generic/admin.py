from django.contrib import admin
from .models import FooterData, Specialization, Clinic

admin.site.site_header = "Trust Clinic"
admin.site.index_title = "Adminsitration"
admin.site.site_title = "T.C."


class SpecializationAdmin(admin.ModelAdmin):
    model = Specialization
    search_fields = ('name',)
    list_display = ('name',)
    ordering = ('name',)


class ClinicAdmin(admin.ModelAdmin):
    model = Clinic
    search_fields = ('name', 'address', 'specializations')
    list_display = ('name', 'address', 'phone')
    ordering = ('name',)
    fieldsets = (
        ('Core Information', {
            'fields': ('name', 'address', 'phone')
        }),
        ('Clinic Schedule', {
            'fields': ('start_time', 'end_time', 'extra_details')
        }),
        ('Clinic Specializations', {
            'fields': ('specializations',)
        }),
        ('Description & Picture', {
            'fields': ('description', 'picture')
        })
    )


class FooterDataAdmin(admin.ModelAdmin):
    model = FooterData

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(FooterData, FooterDataAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Clinic, ClinicAdmin)
