from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Partner, Testimonial, PartnershipApplication, Branch, Program, ProgramRegistration, ContactMessage, CareerApplication


@admin.register(Partner)
class PartnerAdmin(ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ("name", "role", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "role", "message")


@admin.register(PartnershipApplication)
class PartnershipApplicationAdmin(ModelAdmin):
    list_display = ("school_name", "class_type", "school_email", "school_phone", "created_at")
    list_filter = ("class_type", "created_at")
    search_fields = ("school_name", "school_email", "school_phone")
    readonly_fields = ("created_at",)


@admin.register(Branch)
class BranchAdmin(ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "address")


@admin.register(Program)
class ProgramAdmin(ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "short_description")


@admin.register(ProgramRegistration)
class ProgramRegistrationAdmin(ModelAdmin):
    list_display = ("first_name", "last_name", "program", "mode", "duration", "participants", "total_price", "payment_status", "created_at")
    list_filter = ("mode", "duration", "payment_status", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone", "payment_reference")
    readonly_fields = ("created_at", "payment_reference")


@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at",)


@admin.register(CareerApplication)
class CareerApplicationAdmin(ModelAdmin):
    list_display = ("full_name", "email", "position", "created_at")
    list_filter = ("created_at",)
    search_fields = ("full_name", "email", "position")
    readonly_fields = ("created_at",)
