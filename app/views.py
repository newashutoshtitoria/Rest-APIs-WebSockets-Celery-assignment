from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from .tasks import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
import json


# Create your views here.

# Schedule notification for every 20 seconds from the last API call time.
def schedule_notify(current_user):
    try:
        PeriodicTask.objects.all().delete()
        IntervalSchedule.objects.all().delete()

        schedule, created = IntervalSchedule.objects.get_or_create(every=20, period=IntervalSchedule.SECONDS)
        PeriodicTask.objects.create(interval=schedule, name='send_notifaications_every_20sec.',
                                    task='app.tasks.send_notification_task', args=json.dumps([str(current_user), ]))
    except Exception as e:
        return JsonResponse({'success': False, 'msg': str(e)})


# Sign-up
class CreateUserAPI(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            user = User.objects.create_user(username=username, password=password)
            user.save()
            return JsonResponse({'msg': 'User created successfully.'})

        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)})


# Sign-in
class LoginAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            user = User.objects.filter(username=username).first()
            if user.check_password(password):
                schedule_notify(username)
                return JsonResponse({'msg': 'login successfully.'})
            return JsonResponse({'error': 'User authentication failed.'})

        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)})


# Upload images, via celery task.
class UploadImageApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            current_user = request.user
            if current_user:
                name = request.data.get('name')
                image = request.FILES['image'].read()
                byte = base64.b64encode(image)
                data = {
                    'current_user': str(current_user),
                    'name': name,
                    'image': byte.decode('utf-8'),
                    "image_name": request.FILES['image'].name
                }

                upload_image_task.delay(data)

                schedule_notify(current_user)
                return JsonResponse({'msg': 'Image uploaded successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)})


# Only authenticated users and one time the user can like an image.
# Notification send to the user whose image was liked by other users.
class LikeImageApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            current_user = request.user
            if current_user:
                image = Image.objects.filter(id=request.data.get('image_id')).first()
                if image:
                    # Only one time the user can like an image.
                    if current_user in image.like.all():
                        return JsonResponse({'msg': 'You are already like this image.'})
                    image.like.add(current_user)

                    # Send Notification...
                    if image.user != current_user:
                        channel_layer = get_channel_layer()
                        async_to_sync(channel_layer.group_send)(
                            str(image.user.username),
                            {
                                'type': 'chat.message',
                                'message': f"{current_user} likes your image."
                            }
                        )

                        schedule_notify(current_user)
                    return JsonResponse({'msg': 'like successfully.'})
                return JsonResponse({'error': 'image not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)})


# Authenticated User can get the list of all the images posted by other users in a single query just by that user id.
class ViewUserImageApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            current_user = request.user
            context = dict()
            if current_user:
                images = Image.objects.filter(user_id=id).all()
                context['images'] = ImageSerializer(images, many=True, context={'current_user': str(current_user)}).data

                schedule_notify(current_user)
                return JsonResponse(context)
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)})


# When any user queries an image or image list of the other users, there should be one more field, that is liked (True or False), if the user has liked that image then this field should be True in its JSON.
class ViewImageApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            current_user = request.user
            id = request.data.get('id')
            context = dict()
            if current_user:
                images = Image.objects.filter(id__in=id).all()
                context['images'] = ImageSerializer(images, many=True, context={'current_user': str(current_user)}).data

                schedule_notify(current_user)
                return JsonResponse(context)
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)})
