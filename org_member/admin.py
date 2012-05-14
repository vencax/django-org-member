# coding: utf-8

from django.contrib import admin
from django.contrib.admin.options import TabularInline

from .models import OrgMember, FeesPayment

class FeesPaymentInline(TabularInline):
    model = FeesPayment

class OrgMemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'joined', 'tel', 'typee', 'photo')
    list_display_links = ('first_name', 'last_name')
    list_filter = ('typee', )
    search_fields = ('user__last_name', 'user__first_name', 'user__email')
    ordering = ('user', )
    exclude = ('event_attendance', )
    inlines = (FeesPaymentInline,)

admin.site.register(OrgMember, OrgMemberAdmin)