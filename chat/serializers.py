from rest_framework import serializers
from django.contrib.auth.models import User
from chat.models import Message,ChatRoom
class SerachSerilizer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='userprofile.full_name', read_only=True)
    profile = serializers.ImageField(source='userprofile.profile',read_only=True) 
    class Meta:
        model=User
        fields=['id','username','full_name','profile']

class InboxSerializer(serializers.ModelSerializer):
    username=serializers.SerializerMethodField()
    profile=serializers.SerializerMethodField()
    class Meta:
        model=ChatRoom
        fields=['room_id','username','profile']
    def get_username(self,obj):
        user=self.context['request'].user
        return obj.user1.username if obj.user2==user else obj.user2.username
    def get_profile(self, obj):
        user = self.context['request'].user
        target = obj.user1 if obj.user2 == user else obj.user2
        if hasattr(target, 'userprofile') and target.userprofile.profile:
            return target.userprofile.profile.url
        return None

    
class MessageSerilizer(serializers.ModelSerializer):
    sender=serializers.CharField(source='sender.username')
    class Meta:
        model=Message
        fields=['id','sender','text','timestamp']