# coding: utf-8

from django.contrib import admin
from django.contrib.admin.options import TabularInline

from .models import OrgMember, FeesPayment

class FeesPaymentInline(TabularInline):
    model = FeesPayment

class OrgMemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'joined', 'tel', 'typee']
    list_filter = ('typee')
    search_fields = ('user__last_name', 'user__first_name', 'user__email')
    ordering = ('user', )
    exclude = ('joined')
    inlines = (FeesPaymentInline,)

admin.site.register(OrgMember, OrgMemberAdmin)