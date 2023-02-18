from celery import shared_task
from .models import *
import PIL.Image as Images
import io
import base64
import os
from django.core.files import File
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@shared_task()
def upload_image_task(data):
    name = data['name']
    current_user = User.objects.filter(username=data['current_user']).first()

    byte_data = data['image'].encode(encoding='utf-8')
    b = base64.b64decode(byte_data)
    img = Images.open(io.BytesIO(b))
    img.save(data['image_name'], format=img.format)

    with open(data['image_name'], 'rb') as file:
        picture = File(file)

        Image.objects.create(user=current_user, name=name, image=picture)

    os.remove(data['image_name'])

    return 'image uploaded successfully'

@shared_task()
def send_notification_task(*args):
    # Send Notification....
    group = args[0]
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group,
        {
            'type': 'chat.message',
            'message': "This notification is scheduled for every 10 seconds."
        }
    )
    return 'notification sent'
