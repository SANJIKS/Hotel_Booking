from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.admin import UserAdmin
from users.models import OwnerRequest
from decouple import config
# Register your models here.

User = get_user_model()

# admin.site.register(User)
admin.site.register([OwnerRequest])


class CustomAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_owner')
    list_filter = ('is_owner',)
    actions = ['approve_hotel_registration', 'reject_hotel_registration']

    def approve_hotel_registration(self, request, queryset):
        queryset.update(is_owner=True)
        subject = 'Ваша заявка одобрена'
        message = 'Здравствуйте, ваша заявка на становление владельцем одобрена. Спасибо, что выбрали наш сервис!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [obj.email for obj in queryset]
        send_mail(subject, message, from_email, recipient_list)

    def reject_hotel_registration(self, request, queryset):
        queryset.update(is_owner=False)
        subject = 'Ваша заявка одобрена'
        message = 'Мы рассмотрели вашу заявку, и вынуждены отказать вам.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [obj.email for obj in queryset]
        send_mail(subject, message, from_email, recipient_list)

    approve_hotel_registration.short_description = 'Одобрить заявки'
    reject_hotel_registration.short_description = 'Отклонить заявки'

admin.site.register(User, CustomAdmin)
