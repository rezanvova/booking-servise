import smtplib

from pydantic import EmailStr

from app.config import setting
from app.tasks.celeryy import celery
from PIL import Image
from pathlib import Path
from app.tasks.email_temp import create_booking_confirmation_template


@celery.task
def process_pic(path:str):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized = im.resize((1000,500))
    im_resized_small = im.resize((200,100))
    im_resized.save(f"app/static/images/resized_1000_500_{im_path.name}")
    im_resized_small.save(f"app/static/images/resized_200_100_{im_path.name}")


@celery.task()
def send_booking_conf_email(
        booking:dict,
        email_to:EmailStr
):

    email_to= "rez.volodya@yandex.by"
    msg_content = create_booking_confirmation_template(booking,email_to)
    with smtplib.SMTP_SSL(setting.SMTP_HOST,setting.SMTP_PORT) as server:
        server.login(setting.SMTP_USER,setting.SMTP_PASS)
        server.send_message(msg_content)