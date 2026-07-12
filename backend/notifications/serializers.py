from rest_framework import serializers
from .models import Notification, NotificationRead
from authentication.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source='created_by', read_only=True)
    is_read = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = '__all__'
        
    def get_is_read(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return NotificationRead.objects.filter(notification=obj, user=user).exists()
        return False

class NotificationCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
