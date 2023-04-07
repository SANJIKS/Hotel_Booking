from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation_email(user_email, hotel_name, room_number, check_in, check_out, total_cost):
    subject = 'Ваша комната забронирована'
    message = f'Здравствуйте, вы успешно забронировали комнату {room_number} отеля {hotel_name}, с {check_in} по {check_out}. Сумма оплаты: {total_cost} сом. Спасибо что выбрали наш сервис!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
