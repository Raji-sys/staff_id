from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Staff, VerificationLog

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['staff_id', 'get_full_name', 'department', 'status', 'qr_code_link', 'print_card_link']
    list_filter = ['status', 'department', 'date_joined']
    search_fields = ['staff_id', 'first_name', 'last_name', 'email']
    readonly_fields = ['uuid', 'created_at', 'updated_at', 'qr_code_preview']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('staff_id', 'first_name', 'last_name', 'email', 'phone', 'photo')
        }),
        ('Employment Details', {
            'fields': ('department', 'position', 'date_joined', 'date_expiry', 'status')
        }),
        ('System Information', {
            'fields': ('uuid', 'created_at', 'updated_at', 'qr_code_preview'),
            'classes': ('collapse',)
        }),
    )
    
    def qr_code_link(self, obj):
        url = reverse('staff:verify', kwargs={'uuid': obj.uuid})
        return format_html('<a href="{}" target="_blank">View QR</a>', url)
    qr_code_link.short_description = 'QR Code'
    
    def print_card_link(self, obj):
        url = reverse('staff:print_card', kwargs={'uuid': obj.uuid})
        return format_html('<a href="{}" target="_blank">Print Card</a>', url)
    print_card_link.short_description = 'Print'
    
    def qr_code_preview(self, obj):
        url = reverse('staff:verify', kwargs={'uuid': obj.uuid})
        return format_html('<img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={}" />', url)
    qr_code_preview.short_description = 'QR Code Preview'

@admin.register(VerificationLog)
class VerificationLogAdmin(admin.ModelAdmin):
    list_display = ['staff', 'ip_address', 'verified_by','verified_at']
    list_filter = ['verified_at','verified_by',]
    search_fields = ['staff__staff_id', 'staff__first_name', 'staff__last_name', 'ip_address','verified_by',]
    readonly_fields = ['staff', 'ip_address', 'user_agent', 'verified_at','verified_by',]
    
    def has_add_permission(self, request):
        return False