from rest_framework import serializers
from .models import *


class ImageSerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField('get_check_like')

    class Meta:
        model = Image
        fields = ['user', 'name', 'image', 'liked']
        # fields = '__all__'

    def get_check_like(self, obj):
        user = User.objects.filter(username=self.context['current_user']).first()
        likes = obj.like.all()
        if user in likes:
            return True
        return False

